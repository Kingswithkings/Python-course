import speech_recognition as sr
from selenium import webdriver

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.listen_on_mic()

    def listen_on_mic(self):
        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = self.recognizer.listen(source)
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"Command: {command}")

                    if "search" in command:
                        query = command.split("search ")[-1]
                        driver = webdriver.Chrome()  # ✅ Fixed capitalization
                        driver.get(f"https://www.google.com/search?q={query}")
            except sr.UnknownValueError:  # ✅ Fixed typo in exception
                print("Could not understand audio, please try again.")

listener = VoiceAssistant()