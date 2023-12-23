import webbrowser
from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
import pyttsx3  # синтез речи (Text-To-Speech)
import wave  # создание и чтение аудиофайлов формата wav
import json  # работа с json-файлами и json-строками
import os  # работа с файловой системой
import datetime
from num2words import num2words
from bs4 import BeautifulSoup
import requests
import pvporcupine
from pvrecorder import PvRecorder


class VoiceAssistant:
    """
    Настройки голосового ассистента, включающие имя, пол, язык речи
    """
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""


def setup_assistant_voice():
    """
    Установка голоса по умолчанию (индекс может меняться в
    зависимости от настроек операционной системы)
    """
    voices = ttsEngine.getProperty("voices")

    if assistant.speech_language == "en":
        assistant.recognition_language = "en-US"
        if assistant.sex == "female":
            # Microsoft Zira Desktop - English (United States)
            ttsEngine.setProperty("voice", voices[1].id)
        else:
            # Microsoft David Desktop - English (United States)
            ttsEngine.setProperty("voice", voices[2].id)
    else:
        assistant.recognition_language = "ru-RU"
        # Microsoft Irina Desktop - Russian
        ttsEngine.setProperty("voice", voices[0].id)


def play_voice_assistant_speech(text_to_speech):
    """
    Проигрывание речи ответов голосового ассистента (без сохранения аудио)
    :param text_to_speech: текст, который нужно преобразовать в речь
    """
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


def record_and_recognize_audio(*args: tuple):
    """
    Запись и распознавание аудио
    """
    with microphone:
        recognized_data = ""

        # регулирование уровня окружающего шума
        recognizer.adjust_for_ambient_noise(microphone, duration=1)

        try:
            print("Слушаю...")
            #play_voice_assistant_speech("Слушаю...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print("Can you check if your microphone is on, please?")
            return

        # использование online-распознавания через Google
        # (высокое качество распознавания)
        try:
            print("Распознаю вашу речь...")
            #play_voice_assistant_speech("Распознаю вашу речь...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        # в случае проблем с доступом в Интернет происходит
        # попытка использовать offline-распознавание через Vosk
        except speech_recognition.RequestError:
            print("Trying to use offline recognition...")
            recognized_data = use_offline_recognition()

        return recognized_data


def use_offline_recognition():
    """
    Переключение на оффлайн-распознавание речи
    :return: распознанная фраза
    """
    recognized_data = ""
    try:
        # проверка наличия модели на нужном языке в каталоге приложения
        if not os.path.exists("models/vosk-model-small-ru-0.22"):
            print("Please download the model from:\n"
                  "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            exit(1)

        # анализ записанного в микрофон аудио (чтобы избежать повторов фразы)
        wave_audio_file = wave.open("microphone-results.wav", "rb")
        model = Model("models/vosk-model-small-ru-0.22")
        offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()

                # получение данных распознанного текста из JSON-строки
                # (чтобы можно было выдать по ней ответ)
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]
    except:
        print("Sorry, speech service is unavailable. Try again later")

    return recognized_data



def execute_command_with_name(command_name: str, *args: list):
    """
    Выполнение заданной пользователем команды с дополнительными аргументами
    :param command_name: название команды
    :param args: аргументы, которые будут переданы в функцию
    :return:
    """
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
            return True
        else:
            pass

def search_for_video_on_youtube(*args: tuple):
    """
    Поиск видео на YouTube с автоматическим открытием ссылки на список результатов
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    search_term = " ".join(args[0])
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)

    # для мультиязычных голосовых ассистентов лучше создать
    # отдельный класс, который будет брать перевод из JSON-файла
    play_voice_assistant_speech("Вот какие видео я нашла по запросу " + search_term + "на ютубе")

def search_in_internet(*args: tuple):
    """
    Поиск в интернете с автоматическим открытием ссылки на список результатов
    :param args: фраза поискового запроса
    """
    if not args[0]: return
    search_term = " ".join(args[0])
    url = "https://yandex.ru/search/?clid=2358536&text=" + search_term
    webbrowser.get().open(url)

    # для мультиязычных голосовых ассистентов лучше создать
    # отдельный класс, который будет брать перевод из JSON-файла
    play_voice_assistant_speech("Вот что я нашла по запросу " + search_term + "в интернете")

def play_greetings(*args: tuple):
    """
    Приветствие
    """
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        play_voice_assistant_speech("Доброе утро!")

    elif hour >= 12 and hour < 18:
        play_voice_assistant_speech("Добрый день!")

    else:
        play_voice_assistant_speech("Добрый вечер!")

    #play_voice_assistant_speech("Привет!")

def play_dela(*args: tuple):
    """
    Разговор
    """

    play_voice_assistant_speech("У меня все замечательно! Как у вас дела?")
    voice_input = record_and_recognize_audio()
    if "плохо" in voice_input:
        play_voice_assistant_speech("Что случилось?")
    else:
        play_voice_assistant_speech("Рада слышать!")

def play_farewell_and_quit(*args: tuple):
    """
    Прощание
    """
    play_voice_assistant_speech("Досвидания")
    exit()

def ctime(*args: tuple):
    now = datetime.datetime.now()
    text = "Сейчас " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang='ru')
    play_voice_assistant_speech(text)

def help(*args: tuple):
    text = "Я умею: ..."
    text += "произносить текущее время ..."
    text += "искать что-то в интернете  ..."
    text += "искать видео в youtube ..."
    text += "открывать такие приложения, как Photoshop, браузер, игры ..."
    text += "открывать сайт расписания нужной вам группы ..."
    text += "озвучивать текущую погоду ..."
    play_voice_assistant_speech(text)

def openExe(*args: tuple):
    y = 0
    while y == 0:
        play_voice_assistant_speech("Какое приложение открыть?")
        voice_input = record_and_recognize_audio()

        if "photoshop" in voice_input:
            play_voice_assistant_speech("Открываю!")
            codePath = "C:\\Program Files\\Adobe\\Adobe Photoshop 2022\\Photoshop.exe"
            os.startfile(codePath)
            y += 1
        if "игру" in voice_input:
            play_voice_assistant_speech("Открываю!")
            codePath = "C:\\Games\\Keep Talking and Nobody Explodes v1.9.24\\ktane.exe"
            os.startfile(codePath)
            y += 1
        if "браузер" in voice_input:
            play_voice_assistant_speech("Открываю!")
            codePath = "C:\\Users\\demge\\AppData\\Local\\Programs\\Opera GX\\launcher.exe"
            os.startfile(codePath)
            y += 1


def theBest(*args: tuple):
    text = "Погребной Александр Владимирович"
    play_voice_assistant_speech(text)


def play_rasp(*args: tuple):
    """
    Разговор
    """
    x = 0
    while x == 0:
        try:
            play_voice_assistant_speech("Расписание какой группы вы хотите открыть?")
            voice_input = record_and_recognize_audio()
            if "8201" in voice_input:
                gr = '37030'
                x = 1
            elif "8202" in voice_input:
                gr = '37031'
                x = 1
            elif "8203" in voice_input:
                gr = '37032'
                x = 1

        except UnboundLocalError:
            pass
        except TypeError:
            pass

    play_voice_assistant_speech("Расписание на какую неделю вы хотите открыть?")
    voice_input = record_and_recognize_audio()
    print(voice_input)
    if "текущую" in voice_input:
        week_number = datetime.datetime.today().isocalendar()[1] + 18
        print(week_number)
        url = 'https://rasp.tpu.ru/gruppa_' + gr + '/2022/' + str(week_number) + '/view.html'
        webbrowser.get().open(url)
        play_voice_assistant_speech("Открываю расписание на " + voice_input + "неделю")
    else:
        week_number = datetime.datetime.today().isocalendar()[1] + 18
        url = 'https://rasp.tpu.ru/gruppa_' + gr + '/2022/' + str(week_number) + '/view.html'
        webbrowser.get().open(url)
        play_voice_assistant_speech("Открываю расписание на " + voice_input + "неделю")


def search_weather(*args: tuple):
    url = 'https://www.meteoservice.ru/weather/overview/tomsk'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    temp = soup.find('span', 'value')
    print(temp.text)
    play_voice_assistant_speech("Сейчас" + temp.text)

def Isactivation():

    porcupine = pvporcupine.create(
        access_key="rGmjFzlpPYfcYnKSjE6cUZhQaW38gssHbfAMBUhYcS5NFAHBzT3GXA==",
        keywords=["grapefruit"])
    recoder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

    try:
        recoder.start()

        while True:
            keyword_index = porcupine.process(recoder.read())
            if keyword_index >= 0:
                return True

    except KeyboardInterrupt:
        recoder.stop()
    finally:
        porcupine.delete()
        recoder.delete()

commands = {
    ('список команд', 'команды', 'что ты умеешь', 'твои навыки', 'навыки'): help,
    ("здравствуй", "привет", "приветствую"): play_greetings,
    #("как дела"): play_dela,
    ("найди"): search_in_internet,
    ("выход", "стоп", "досвидания", "пока"): play_farewell_and_quit,
    ("включи видео"): search_for_video_on_youtube,
    ('время', 'текущее время', 'сейчас времени', 'который час'): ctime,
    ("открой приложение"): openExe,
    ("кто наш руководитель"): theBest,
    ("покажи расписание", "расписание"): play_rasp,
    ("какая погода сейчас", "погода", "температура", "какая сейчас погода"): search_weather,
}

if __name__ == "__main__":

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    # инициализация инструмента синтеза речи
    ttsEngine = pyttsx3.init()

    # настройка данных голосового помощника
    assistant = VoiceAssistant()
    assistant.name = "Алиса"
    assistant.sex = "female"
    assistant.speech_language = "ru"

    # установка голоса по умолчанию
    setup_assistant_voice()

    while True:

        activation = Isactivation()

        # отделение команд от дополнительной информации (аргументов)
        if activation:

            voice_input = record_and_recognize_audio()
            os.remove("microphone-results.wav")

            print(voice_input)

            voice_input = voice_input.split(" ")

            k=0

            while k<3:
                print(voice_input)

                if k == 0:
                    command = voice_input[0]
                if (k == 1) and (k < len(voice_input)):
                    command = voice_input[0] + " " + voice_input[1]
                if (k == 2) and (k < len(voice_input)):
                    command = voice_input[0] + " " + voice_input[1] + " " + voice_input[2]

                command_options = [str(input_part) for input_part in voice_input[(k+1):len(voice_input)]]

                print(k)
                print(command)
                print(command_options)

                if execute_command_with_name(command, command_options):
                    k += 10
                else:
                    k += 1

            if k < 5:
                play_voice_assistant_speech("Я не поняла, что вы сказали. Повторите пожалуйста.")

            activation = False

