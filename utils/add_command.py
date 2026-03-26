from .voicing_answer import run_voice
import speech_recognition

from core.models import AppCommand

recognizer = speech_recognition.Recognizer()

def get_voice(source) -> str | None:
    try:
        audio = recognizer.listen(source, phrase_time_limit = 5)
        text = recognizer.recognize_google(audio, language="uk-UA").strip()
        print(f"Асистент почув: {text}")
        return text
    except:
        return None

def add_command(source):
    run_voice('Щоб додати команду скажіть ключове слово')
    
    keyword = get_voice(source)

    if keyword:
        run_voice(f'Ваше слово: {keyword}. Підтвердити?')

        accept = get_voice(source)

        if 'підтвердити' in accept.lower() or 'так' in accept.lower():
            run_voice("Скажіть назву файлу додатка")

            app_name = get_voice(source)
            
            if app_name:
                run_voice(f"Назва додатку {app_name}. Підтвердити?")

                name_accept = get_voice(source)

                if 'підтвердити' in name_accept.lower() or 'так' in name_accept.lower():
                    AppCommand.objects.create(name= app_name, keyword= keyword)
                    run_voice("Команду успішно додано")

                else:
                    run_voice("Невдалося підтвердити")
            else:
                run_voice("Назву не розпізнано")
        else:
            run_voice("Невдалося підтвердити")
    else: 
        run_voice('Я не почула слово, спробуйте ще раз')