from django.core.management.base import BaseCommand
import speech_recognition
from utils.voicing_answer import run_voice  

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
                    run_voice(text)
                except speech_recognition.UnknownValueError:
                    continue
                except Exception as error:
                    self.stdout.write(self.style.WARNING(f"Помилка!\n{error}"))