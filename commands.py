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

commands = {
    ('список команд', 'команды', 'что ты умеешь', 'твои навыки', 'навыки'): main.help,
    ("здравствуй", "привет", "приветствую"): main.play_greetings,
    ("как дела"): main.play_dela,
    ("найди"): main.search_in_internet,
    ("выход", "стоп", "досвидания", "пока"): main.play_farewell_and_quit,
    ("включи видео"): main.search_for_video_on_youtube,
    ('время', 'текущее время', 'сейчас времени', 'который час'): main.ctime,
    ("открой приложение"): main.openExe,
    ("кто наш руководитель"): main.theBest,
    ("покажи расписание", "расписание"): main.play_rasp,
    ("какая погода сейчас", "погода", "температура", "какая сейчас погода"): main.search_weather,
}