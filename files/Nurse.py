import gradio as gr
import speech_recognition as sr
import pyttsx3
import openai
import sqlite3
import threading
import requests
import time
import logging
from googletrans import Translator
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import schedule

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for API retry mechanism
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
ERROR_CODES = [502, 503, 504]

class SpeechSystem:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.translator = Translator()
    
    def speak(self, text, voice='default', lang='en'):
        try:
            if voice == 'female' and len(self.voices) > 1:
                self.engine.setProperty('voice', self.voices[1].id)
            elif voice == 'male':
                self.engine.setProperty('voice', self.voices[0].id)
            
            if lang != 'en':
                text = self.translator.translate(text, dest=lang).text
                logger.info(f"Translated response: {text}")
            
            self.engine.say(text)
            self.engine.runAndWait()
            return text
        except Exception as e:
            logger.error(f"Speech error: {e}")
            return "Error in speech processing."

class MedicalInfoFetcher:
    def fetch_pubmed_info(self, query):
        url = f"https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/?format=citation&id={query}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return "No relevant medical information found."
    
    def scrape_webmd(self, symptom):
        url = f"https://www.webmd.com/search/search_results/default.aspx?query={symptom}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all("a", class_="search-results-doc-title")
            return [res.text for res in results[:5]]
        return ["No results found"]

fetcher = MedicalInfoFetcher()

def scheduled_data_update():
    logger.info("Updating medical information sources...")
    # Here, you can update cached data from external sources
    pass

schedule.every(6).hours.do(scheduled_data_update)

class Assistant:
    def __init__(self):
        self.speech_system = SpeechSystem()
        self.conversation_history = []
        openai.api_key = "your-api-key-here"
    
    def fetch_information(self, question, lang='en'):
        context = " ".join(self.conversation_history[-5:])
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": context}] +
                     [{"role": "user", "content": question}],
            temperature=0.7
        )
        result = response["choices"][0]["message"]["content"]
        self.conversation_history.append(question)
        self.conversation_history.append(result)
        
        if lang != 'en':
            result = self.speech_system.translator.translate(result, dest=lang).text
        
        return result
    
    def assistive_nurse(self, patient_name, age, symptoms, question, lang='en'):
        additional_info = fetcher.scrape_webmd(symptoms)
        response = f"Patient: {patient_name}, Age: {age}. Symptoms: {symptoms}. {self.fetch_information(question, lang)}. Additional Info: {additional_info}"
        return self.speech_system.speak(response, voice='female', lang=lang)

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Speech recognition unavailable."

assistant = Assistant()

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule, daemon=True).start()

with gr.Blocks() as chatbot:
    gr.Markdown("### Interactive Medical Assistant")
    
    with gr.Tab("Nurse Mode"):
        patient_name = gr.Textbox(label="Patient Name")
        age = gr.Number(label="Age")
        symptoms = gr.Textbox(label="Symptoms")
        question = gr.Textbox(label="Health Question")
        lang = gr.Textbox(label="Language", value="en")
        output = gr.Textbox(label="Response")
        submit = gr.Button("Get Advice")
        submit.click(lambda n, a, s, q, l: assistant.assistive_nurse(n, a, s, q, l),
                     inputs=[patient_name, age, symptoms, question, lang],
                     outputs=output)

if __name__ == "__main__":
    chatbot.launch()
