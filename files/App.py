import speech_recognition as sr
from selenium import webdriver

class voice:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.listenOnMic()

    def listenOnMic(self):
        while True:
            try:
                with sr.Microphone() as source:
                    audio = self.recognizer.listen(source)
                    command = self.recognizer.recognize_google(audio).lower()

                    if "search" in command:
                        driver = webdriver.chrome()
                        driver.get(f"https://www.google.com/search?q=google+search+url+link&oq=google+search+url&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBggBEEUYOTIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIHCAkQABiABNIBCjE0OTEwajFqMTWoAgiwAgE&sourceid=chrome&ie=UTF-8{command.split('search ')[-1]}")
            except sr.SpeechRecognition.UnknowValueError:
                pass

listener = voice()