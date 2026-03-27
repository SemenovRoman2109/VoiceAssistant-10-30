from django.core.management.base import BaseCommand
import speech_recognition, platform, os, subprocess, webbrowser, pyautogui

from utils.voicing_answer import run_voice  
from core.models import AppCommand, VoiceAnswer, WebSite, AppGroup
from utils.find_path import find_path
from utils.add_command import add_command

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if kwargs.get("command") == "help":
            self.help()
            return
        
        self.run = True
        self.stdout.write(self.style.SUCCESS("Асистент запущений..."))

        recognizer = speech_recognition.Recognizer()
        microphone = speech_recognition.Microphone()

        with microphone as source:
            self.stdout.write("Почекайте, налаштовую фоновий шум...")
            recognizer.adjust_for_ambient_noise(source= source)
            self.stdout.write(self.style.SUCCESS("Слухаю вас..."))

            while self.run:
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
        if "допомога" in text.lower():
            self.help()
        elif "зупинись" in text.lower():
            self.run = False
        elif "додати команду" in text.lower():
            add_command(source= source)
        elif "відкрий сайт" in text.lower():
            sites = []
            for site in WebSite.objects.all():
                if site.name.lower() in text.lower():
                    sites.append(site)
            
            if not sites:
                run_voice('Я не знайшла такий сайт')
            elif len(sites) == 1:
                run_voice(f'Відкриваю сайт {sites[0].name}')
                webbrowser.open(sites[0].url)
            else:
                run_voice('Відкриваю всі сайти')
                for site in sites:
                    webbrowser.open(site.url)
            
        elif "відкрий" in text.lower() or "закрий" in text.lower():
            all_commnds = AppCommand.objects.all()
            list_apps = []

            for command in all_commnds:
                if command.keyword.lower() in text.lower():
                    list_apps.append(command)
            
            if "групу" in text.lower():
                groups = AppGroup.objects.all()
                for group in groups:
                    if group.name.lower() in text.lower():
                        list_apps.extend(group.apps.all())
                    
            if list_apps:
                if len(list_apps) > 1:
                    if "відкрий" in text.lower():
                        run_voice("Відкриваю програми")
                    else:
                        run_voice("Закриваю програми")
                
                for user_app in list_apps:
                    if user_app.path:
                        if "відкрий" in text.lower():
                            if len(list_apps) == 1: run_voice(f"Відкриваю {user_app.name}")
                            self.open_app(path_app = user_app.path)
                        else:
                            if len(list_apps) == 1: run_voice(f"Закриваю {user_app.name}")
                            self.close_app(app_name= os.path.basename(user_app.path))
                    else:
                        if len(list_apps) == 1: run_voice(f"Шукаю {user_app.name}")
                        path = find_path(filename = user_app.name)
                        if path:
                            if len(list_apps) == 1: run_voice(f"Знайшла {user_app.name}")
                            if "відкрий" in text.lower():
                                self.open_app(path_app = path)
                            else: 
                                self.close_app(app_name= os.path.basename(user_app.path))
                            user_app.path = path
                            user_app.save()
                        else:
                            if len(list_apps) == 1: run_voice("Я не знайшла шлях до цієї програми") 
            else:
                run_voice("Я не знайшла такої програми")
        
        elif "збільшити гучність" in text.lower():
            pyautogui.press("volumeup", 5)
        elif "зменшити гучність" in text.lower():
            pyautogui.press("volumedown", 5)
        else:
            answers = VoiceAnswer.objects.all()

            for answer in answers:
                if answer.request.lower() in text.lower():
                    run_voice(answer.response)
                    break
    
    # python manage.py команда аргумент1 
    def add_arguments(self, parser):

        parser.add_argument(
            "command",
            nargs="?",
            type=str
        )

    def close_app(self, app_name: str):
        try:
            system = platform.system()
            if system == "Windows":
                subprocess.run(
                    args = ["taskkill", "/IM", app_name, "/F"],
                    stdout= subprocess.DEVNULL,
                    stderr= subprocess.DEVNULL
                )
            else: 
                subprocess.run(args= ["pkill", app_name])
        except Exception as error:
            self.stdout.write(self.style.WARNING(f"Помилка закриття: {error}"))

            
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
        self.stdout.write("Список можливих дій: \n\n • Додати команду \n • Закрий 'Назва додатку'\n • Відкрий 'Назва додатку'\n • Відкрий/Закрий групу 'Назва групи'\n • Відкрий сайт 'Назва сайту'\n • Збільшити гучність \n • Зменшити гучність \n • Зупинись \n\nСписок додатків: ")
        for app_command in AppCommand.objects.all():
            self.stdout.write(f" • Ключове слово - {app_command.keyword}, Назва додатку - {app_command.name}")
        self.stdout.write("\nГолосові запити:")
        for voice_answer in VoiceAnswer.objects.all():
            self.stdout.write(f' • {voice_answer.request}')
        self.stdout.write("\nСписок сайтів:")
        for site in WebSite.objects.all():
            self.stdout.write(f' • {site.name}, url - {site.url}')
