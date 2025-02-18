import gradio as gr
import speech_recognition as sr
import pyttsx3
import openai
import sqlite3
import logging
from googletrans import Translator

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

class PatientDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("patients.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id TEXT PRIMARY KEY,
                name TEXT,
                age INTEGER,
                history TEXT
            )
        """)
        self.conn.commit()

    def save_patient(self, patient_id, name, age, history):
        self.cursor.execute("INSERT OR REPLACE INTO patients VALUES (?, ?, ?, ?)",
                            (patient_id, name, age, history))
        self.conn.commit()

    def get_patient(self, patient_id):
        self.cursor.execute("SELECT * FROM patients WHERE id=?", (patient_id,))
        return self.cursor.fetchone()

class Assistant:
    def __init__(self):
        self.speech_system = SpeechSystem()
        self.db = PatientDatabase()
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
        response = f"Patient: {patient_name}, Age: {age}. Symptoms: {symptoms}. {self.fetch_information(question, lang)}"
        return self.speech_system.speak(response, voice='female', lang=lang)
    
    def child_assistant(self, question, lang='en'):
        response = f"{self.fetch_information(question, lang)}"
        return self.speech_system.speak(response, voice='male', lang=lang)
    
    def assistive_doctor(self, patient_id, medical_history, symptoms, question, lang='en'):
        self.db.save_patient(patient_id, "Unknown", 0, medical_history)
        response = f"Patient ID: {patient_id}. Medical History: {medical_history}. Symptoms: {symptoms}. {self.fetch_information(question, lang)}"
        return self.speech_system.speak(response, voice='male', lang=lang)

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
    
    with gr.Tab("Child Mode"):
        question = gr.Textbox(label="Ask a Question")
        lang = gr.Textbox(label="Language", value="en")
        output = gr.Textbox(label="Response")
        submit = gr.Button("Ask")
        submit.click(lambda q, l: assistant.child_assistant(q, l),
                     inputs=[question, lang],
                     outputs=output)
    
    with gr.Tab("Doctor Mode"):
        patient_id = gr.Textbox(label="Patient ID")
        medical_history = gr.Textbox(label="Medical History")
        symptoms = gr.Textbox(label="Symptoms")
        question = gr.Textbox(label="Medical Question")
        lang = gr.Textbox(label="Language", value="en")
        output = gr.Textbox(label="Response")
        submit = gr.Button("Analyze")
        submit.click(lambda pid, hist, symp, q, l: assistant.assistive_doctor(pid, hist, symp, q, l),
                     inputs=[patient_id, medical_history, symptoms, question, lang],
                     outputs=output)

if __name__ == "__main__":
    chatbot.launch()
