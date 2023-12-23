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

import main


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
    main.play_voice_assistant_speech("Вот какие видео я нашла по запросу " + search_term + "на ютубе")

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
    main.play_voice_assistant_speech("Вот что я нашла по запросу " + search_term + "в интернете")

def play_greetings(*args: tuple):
    """
    Приветствие
    """
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        main.play_voice_assistant_speech("Доброе утро!")

    elif hour >= 12 and hour < 18:
        main.play_voice_assistant_speech("Добрый день!")

    else:
        main.play_voice_assistant_speech("Добрый вечер!")

    #play_voice_assistant_speech("Привет!")

def play_dela(*args: tuple):
    """
    Разговор
    """

    main.play_voice_assistant_speech("У меня все замечательно! Как у вас дела?")
    voice_input = main.record_and_recognize_audio()
    if "плохо" in voice_input:
        main.play_voice_assistant_speech("Что случилось?")
    else:
        main.play_voice_assistant_speech("Рада слышать!")

def play_farewell_and_quit(*args: tuple):
    """
    Прощание
    """
    main.play_voice_assistant_speech("Досвидания")
    exit()

def ctime(*args: tuple):
    now = datetime.datetime.now()
    text = "Сейчас " + num2words(now.hour, lang='ru') + " " + num2words(now.minute, lang='ru')
    main.play_voice_assistant_speech(text)

def helper(*args: tuple):
    text = "Я умею: ..."
    text += "произносить текущее время ..."
    text += "искать что-то в интернете  ..."
    text += "искать видео в youtube ..."
    text += "открывать такие приложения, как Photoshop, браузер, игры ..."
    main.play_voice_assistant_speech(text)

def openExe(*args: tuple):
    y = 0
    while y == 0:
        main.play_voice_assistant_speech("Какое приложение открыть?")
        voice_input = main.record_and_recognize_audio()

        if "photoshop" in voice_input:
            main.play_voice_assistant_speech("Открываю!")
            codePath = "C:\\Program Files\\Adobe\\Adobe Photoshop 2022\\Photoshop.exe"
            os.startfile(codePath)
            y += 1
        if "игру" in voice_input:
            main.play_voice_assistant_speech("Открываю!")
            codePath = "C:\\Games\\Keep Talking and Nobody Explodes v1.9.24\\ktane.exe"
            os.startfile(codePath)
            y += 1
        if "браузер" in voice_input:
            main.play_voice_assistant_speech("Открываю!")
            codePath = "C:\\Users\\demge\\AppData\\Local\\Programs\\Opera GX\\launcher.exe"
            os.startfile(codePath)
            y += 1


def theBest(*args: tuple):
    text = "Погребной Александр Владимирович"
    main.play_voice_assistant_speech(text)


def play_rasp(*args: tuple):
    """
    Разговор
    """
    x = 0
    while x == 0:
        try:
            main.play_voice_assistant_speech("Расписание какой группы вы хотите открыть?")
            voice_input = main.record_and_recognize_audio()
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

    main.play_voice_assistant_speech("Расписание на какую неделю вы хотите открыть?")
    voice_input = main.record_and_recognize_audio()
    print(voice_input)
    if "текущую" in voice_input:
        week_number = datetime.datetime.today().isocalendar()[1] + 18
        print(week_number)
        url = 'https://rasp.tpu.ru/gruppa_' + gr + '/2022/' + str(week_number) + '/view.html'
        webbrowser.get().open(url)
        main.play_voice_assistant_speech("Открываю расписание на " + voice_input + "неделю")
    else:
        week_number = datetime.datetime.today().isocalendar()[1] + 18
        url = 'https://rasp.tpu.ru/gruppa_' + gr + '/2022/' + str(week_number) + '/view.html'
        webbrowser.get().open(url)
        main.play_voice_assistant_speech("Открываю расписание на " + voice_input + "неделю")


def search_weather(*args: tuple):
    url = 'https://www.meteoservice.ru/weather/overview/tomsk'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    temp = soup.find('span', 'value')
    print(temp.text)
    main.play_voice_assistant_speech("Сейчас" + temp.text)