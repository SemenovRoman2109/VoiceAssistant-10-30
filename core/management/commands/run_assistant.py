from django.core.management.base import BaseCommand
import speech_recognition, platform, os, subprocess

from utils.voicing_answer import run_voice  
from core.models import AppCommand, VoiceAnswer
from utils.find_path import find_path
from utils.add_command import add_command

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Асистент запущений..."))

        recognizer = speech_recognition.Recognizer()
        microphone = speech_recognition.Microphone()

        with microphone as source:
            self.stdout.write("Почекайте, налаштовую фоновий шум...")
            recognizer.adjust_for_ambient_noise(source= source)
            self.stdout.write(self.style.SUCCESS("Слухаю вас..."))

            while True:
                try:
                    audio = recognizer.listen(source= source, phrase_time_limit= 5)
                    text = recognizer.recognize_google(audio, language="uk-UA")
                    self.stdout.write(f"Ви сказали: {text}")
                    self.doing_task(text=text, source= source)
                except speech_recognition.UnknownValueError:
                    continue
                except Exception as error:
                    self.stdout.write(self.style.WARNING(f"Помилка!\n{error}"))

    def doing_task(self, text: str, source: speech_recognition.Microphone):
        # "Відкрий браузер"
        if "допомога" in text.lower():
            self.help()
        if "додати команду" in text.lower():
            add_command(source= source)
        if "відкрий" in text.lower():
            all_commnds = AppCommand.objects.all()
            user_app = None

            for command in all_commnds:
                if command.keyword.lower() in text.lower():
                    user_app = command
                    break
            if user_app:
                if user_app.path:
                    run_voice(f"Відкриваю {user_app.name}")
                    self.open_app(path_app = user_app.path)
                else:
                    run_voice(f"Шукаю {user_app.name}")
                    path = find_path(filename = user_app.name)
                    if path:
                        run_voice(f"Знайшла {user_app.name}")
                        self.open_app(path_app = path)
                        user_app.path = path
                        user_app.save()
                    else:
                        run_voice("Я не знайшла шлях до цієї програми")
            else:
                run_voice("Я не знайшла такої програми")

        else:
            answers = VoiceAnswer.objects.all()

            for answer in answers:
                if answer.request.lower() in text.lower():
                    run_voice(answer.response)
                    break

    def open_app(self, path_app: str):
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(filepath=path_app)
            elif system == "Darwin":
                subprocess.Popen(args = ["open", path_app])
            else:
                subprocess.Popen(args=[path_app])
        except Exception as error:
            self.stdout.write(self.style.WARNING(f"Помилка запуску: {error}"))
                
    def help(self):
        self.stdout.write("Список можливих дій: \n\n • Додати команду \n • Відкрий 'Назва додатку' \n\nСписок додатків: ")
        for app_command in AppCommand.objects.all():
            self.stdout.write(f" • Ключове слово - {app_command.keyword}, Назва додатку - {app_command.name}")
        self.stdout.write("\nГолосові запити:")
        for voice_answer in VoiceAnswer.objects.all():
            self.stdout.write(f' • {voice_answer.request}')