import time
import webbrowser #работа с браузером
from vosk import Model, KaldiRecognizer  # оффлайн-распознавание от Vosk
import pyttsx3  # синтез речи (Text-To-Speech)
import json  # работа с json-файлами и json-строками
import pyaudio #запись голоса
import os  # работа с файловой системой
import datetime #работа с датами
from num2words import num2words #улучшенное распознавание чисел
from bs4 import BeautifulSoup
import requests #работа с YandexGPT
import pvporcupine #стартовое слово
from pvrecorder import PvRecorder #запись голоса для стартового слова
from fuzzywuzzy import fuzz #поиск расстояния Левенштейна
import wave
import librosa
import soundfile as sf


# инициализация модели Vosk
model = Model("models/small_model_ru")
rec = KaldiRecognizer(model, 16000)


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


def speach_recognition(text_to_speech):
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
    try:
        print("Слушаю...")

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        try:
            # проверка наличия модели на нужном языке в каталоге приложения
            if not os.path.exists("models/small_model_ru"):
                print("Please download the model from:\n"
                      "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
                exit(1)
            while True:
                # анализ записанного в микрофон аудио (чтобы избежать повторов фразы)
                data = stream.read(4000, exception_on_overflow=False)

                if (rec.AcceptWaveform(data)) and (len(data) > 0):
                    recognized_data = json.loads(rec.Result())
                    if recognized_data['text']:
                        return recognized_data['text']
        except:
            print("Извините, произошла какая-то ошибка")
    except:
        pass


def execute_command_with_name(command_name: str):
    """
    Выполнение заданной пользователем команды
    """
    for key in commands.keys():
        if (type(key) == tuple):
            for variant in key:
                commandRate = fuzz.WRatio(str(command_name), variant)
                if commandRate >= 80:
                    commands[key]()
                    return True
                else:
                    pass
        else:
            commandRate = fuzz.WRatio(str(command_name), key)
            if commandRate >= 80:
                commands[key]()
                return True
            else:
                pass

def search_for_video_on_youtube():
    """
    Поиск видео на YouTube с автоматическим открытием ссылки на список результатов
    """
    text_to_speach("Что открыть в YouTube?")
    search_term = record_and_recognize_audio()

    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)

    text_to_speach("Вот какие видео я нашла по запросу " + search_term + "на ютубе")


def search_in_internet():
    """
    Поиск в интернете с автоматическим открытием ссылки на список результатов
    """
    text_to_speach("Что открыть в браузере?")
    search_term = record_and_recognize_audio()

    url = "https://yandex.ru/search/?clid=2358536&text=" + search_term
    webbrowser.get().open(url)

    text_to_speach("Вот что я нашла по запросу " + search_term + "в интернете")


def play_greetings():
    """
    Приветствие
    """
    hour = int(datetime.datetime.now().hour)

    if hour >= 6 and hour < 12:
        text_to_speach("Доброе утро!")

    elif hour >= 12 and hour < 18:
        text_to_speach("Добрый день!")

    elif hour > 18 and hour < 24:
        text_to_speach("Добрый вечер!")

    else:
        text_to_speach("Доброй ночи!")


def play_farewell_and_quit():
    """
    Прощание
    """
    text_to_speach("Досвидания")
    os.remove("audio.wav")
    exit()


def ctime():
    now = datetime.datetime.now()
    text = "Сейчас " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang='ru')
    text_to_speach(text)


def help():
    text = "Я умею: ..."
    text += "произносить текущее время ..."
    text += "искать что-то в интернете  ..."
    text += "искать видео в youtube ..."
    text += "открывать такие приложения, как Photoshop, браузер, игры ..."
    text += "открывать сайт расписания нужной вам группы ..."
    text += "озвучивать текущую погоду ..."
    text_to_speach(text)


def openExe():
    while True:
        text_to_speach("Какое приложение открыть?")
        voice_input = record_and_recognize_audio()

        if "photoshop" in voice_input:
            text_to_speach("Открываю!")
            codePath = "C:\\Program Files\\Adobe\\Adobe Photoshop 2022\\Photoshop.exe"
            os.startfile(codePath)
            return True
        if "игру" in voice_input:
            text_to_speach("Открываю!")
            codePath = "C:\\Games\\Keep Talking and Nobody Explodes v1.9.24\\ktane.exe"
            os.startfile(codePath)
            return True
        if "браузер" in voice_input:
            text_to_speach("Открываю!")
            codePath = "C:\\Users\\demge\\AppData\\Local\\Programs\\Opera GX\\launcher.exe"
            os.startfile(codePath)
            return True

        text_to_speach("Я вас не поняла, повторите ещё раз")

def theBest():
    prepodavatel = "Погребной Александр Владимирович"
    text_to_speach(prepodavatel)


def play_rasp():
    """
    Разговор
    """
    x = 0
    while x == 0:
        try:
            text_to_speach("Расписание какой группы вы хотите открыть?")
            voice_input = record_and_recognize_audio()

            if "восемь ноль два" in voice_input:
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

    text_to_speach("Расписание на какую неделю вы хотите открыть?")
    voice_input = record_and_recognize_audio()
    print(voice_input)

    if "текущую" in voice_input:
        week_number = datetime.datetime.today().isocalendar()[1] + 18
        print(week_number)
        url = 'https://rasp.tpu.ru/gruppa_' + gr + '/2023/' + str(week_number) + '/view.html'
        webbrowser.get().open(url)
        text_to_speach("Открываю расписание на " + voice_input + "неделю")
    else:
        week_number = datetime.datetime.today().isocalendar()[1] + 18
        url = 'https://rasp.tpu.ru/gruppa_' + gr + '/2023/' + str(week_number) + '/view.html'
        webbrowser.get().open(url)
        text_to_speach("Открываю расписание на " + voice_input + "неделю")


def search_weather():
    url = 'https://www.meteoservice.ru/weather/overview/tomsk'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    temp = soup.find('span', 'value')
    text_to_speach("Сейчас" + temp.text)


def Isactivation():

    porcupine = pvporcupine.create(
        access_key="rGmjFzlpPYfcYnKSjE6cUZhQaW38gssHbfAMBUhYcS5NFAHBzT3GXA==",
        keywords=["grapefruit", "computer"])
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

def text_to_speach(text):
    headers = {'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTU1NWE5ZDEtMzAzMy00ZDE0LWJkYmMtNmE4NDVkNTEzMGNhIiwidHlwZSI6ImFwaV90b2tlbiJ9.tN5TVNRGqQ9CxrE4C-pKPvzINGdGuB-agM_EBCR19hk'}
    url = "https://api.edenai.run/v2/audio/text_to_speech"
    payload = {
        "providers": "openai",
        "language": "ru",
        "option": "FEMALE",
        "openai": "ru_shimmer",
        "text": f"{text}"
    }
    response = requests.post(url, json = payload, headers= headers)
    result = json.loads(response.text)

    audio_url = result["openai"]["audio_resource_url"]
    print((audio_url))
    r = requests.get(audio_url)

    with open("audio.wav", "wb") as file:
        file.write(r.content)
    file.close()

    x, _ = librosa.load('./audio.WAV', sr=40000)
    sf.write('audio.wav', x, 20000)
    wave.open('audio.wav', 'r')
    audio_file = wave.open('audio.wav', 'r')

    FORMAT = audio_file.getsampwidth()  # глубина звука
    CHANNELS = audio_file.getnchannels()  # количество каналов
    RATE = audio_file.getframerate()  # частота дискретизации
    N_FRAMES = audio_file.getnframes()  # кол-во отсчетов
    audio = pyaudio.PyAudio()

    # открываем поток для записи на устройство вывода - динамик - с такими же параметрами
    out_stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, output=True)

    out_stream.write(audio_file.readframes(N_FRAMES))  # отправляем на динамик

    audio.terminate()



commands = {
    ('список команд', 'команды', 'что ты умеешь', 'твои навыки', 'навыки'): help,
    ("здравствуй", "привет", "приветствую"): play_greetings,
    ("открой в браузере"): search_in_internet,
    ("выход", "стоп", "досвидания", "пока"): play_farewell_and_quit,
    ("включи видео"): search_for_video_on_youtube,
    ('время', 'текущее время', 'сейчас времени', 'который час', 'сколько времени'): ctime,
    ("открой приложение"): openExe,
    ("кто наш руководитель"): theBest,
    ("расписание"): play_rasp,
    ("какая погода сейчас", "погода", "температура", "какая сейчас погода"): search_weather,
}


if __name__ == "__main__":
    # инициализация инструмента синтеза речи
    ttsEngine = pyttsx3.init()



    # настройка данных голосового помощника
    assistant = VoiceAssistant()
    assistant.name = "Алиса"
    assistant.sex = "female"
    assistant.speech_language = "ru"

    # установка голоса по умолчанию
    setup_assistant_voice()

    text_to_speach("Здравствуйте, меня зовут Компьютер")

    while True:

        activation = False
        activation = Isactivation()

        if activation:

            text_to_speach("Да, сэр")

            voice_input = record_and_recognize_audio(model, rec)

            #print(voice_input)

            if not execute_command_with_name(voice_input):

                prompt = {
                    "modelUri": "gpt://b1giqp5u18ts53m4t8dt/yandexgpt-lite",
                    "completionOptions": {
                        "stream": False,
                        "temperature": 0.6,
                        "maxTokens": "2000"
                    },
                    "messages": [
                        {
                            "role": "system",
                            "text": "Ты преподаватель в университете."
                        },
                        {
                            "role": "user",
                            "text": "Здравствуйте! Мне нужна ваша помощь."
                        },
                        {
                            "role": "assistant",
                            "text": "Здравствуйте! Задавайте свой вопрос."
                        },
                        {
                            "role": "user",
                            "text": voice_input
                        }
                    ]
                }

                url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Api-Key AQVN1PQls17JJj1VhazwvzUnjyBbcUD_XuLOuSiQ"
                }
                endOfStringNum =66
                newText =""
                response = requests.post(url, headers=headers, json=prompt)
                result = response.text
                while response.text[endOfStringNum] != '"':
                    endOfStringNum+=1

                for i in range(66, endOfStringNum ):
                    newText += response.text[i]
                #play_voice_assistant_speech(newText)
                text_to_speach(newText)



