import gradio as gr
import random
import requests
import speech_recognition as sr
import pyttsx3
import openai
from googletrans import Translator
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for retry mechanism
MAX_RETRIES = 3
BACKOFF_FACTOR = 1
ERROR_CODES = [502, 503, 504]

class SpeechSystem:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.translator = Translator()
        
    def speak(self, text, voice='default', lang='en'):
        """Convert text to speech with translation support."""
        try:
            # Handle voice selection
            if voice == 'female' and len(self.voices) > 1:
                self.engine.setProperty('voice', self.voices[1].id)
            elif voice == 'male':
                self.engine.setProperty('voice', self.voices[0].id)
            
            # Translate text if needed
            if lang != 'en':
                translated_text = self.translator.translate(text, dest=lang).text
                logger.info(f"Translated '{text}' to '{translated_text}' in {lang}")
                text_to_speak = translated_text
            else:
                text_to_speak = text
            
            # Speak the text
            self.engine.say(text_to_speak)
            self.engine.runAndWait()
            return text_to_speak
        
        except Exception as e:
            logger.error(f"Error in speak function: {str(e)}")
            raise

class Assistant:
    def __init__(self):
        self.speech_system = SpeechSystem()
        openai.api_key = "sk-proj-KvKFj3m1BDXSl4kS81O_tGv4YjvctkQyfWlkWfq-qs4jIe33MMf2OjCoucdrkU2CmFfMn3q8EVT3PlbkFJJ5QRWIjzMJOfguHCqiBDjMEulpdqSDxCuYRFaXZFH4H8niRpTWoFzDpbcrVXL8-1vJ0Eaqeq8A"
        
    def fetch_information(self, question, lang='en'):
        """Fetch information using OpenAI API with translation support."""
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=BACKOFF_FACTOR,
            status_forcelist=ERROR_CODES,
            allowed_methods=["POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        
        for attempt in range(MAX_RETRIES):
            try:
                response = session.post(
                    'https://api.openai.com/v1/chat/completions',
                    json={
                        'model': 'gpt-4',
                        'messages': [{'role': 'user', 'content': question}],
                        'temperature': 0,
                        'max_tokens': 2048,
                        'top_p': 0.95,
                        'frequency_penalty': 0,
                        'presence_penalty': 0
                    },
                    headers={'Authorization': f'Bearer {openai.api_key}'},
                    timeout=30
                )
                
                response.raise_for_status()
                result = response.json()['choices'][0]['message']['content']
                
                if lang != 'en':
                    translated_response = self.speech_system.translator.translate(
                        result, dest=lang).text
                    logger.info(f"Successfully translated response to {lang}")
                    return translated_response
                return result
                
            except requests.exceptions.RequestException as e:
                logger.error(f"API Request Error (attempt {attempt + 1}/{MAX_RETRIES}): {str(e)}")
                
                if attempt == MAX_RETRIES - 1:
                    raise Exception(f"Failed after {MAX_RETRIES} attempts: {str(e)}")
                
                # Exponential backoff
                delay = BACKOFF_FACTOR * (2 ** attempt)
                time.sleep(delay)
                logger.info(f"Waiting {delay} seconds before retry...")

    def assistive_nurse(self, patient_name, age, symptoms, question, lang='en'):
        """Nurse Mode: Collects patient data and provides health advice."""
        try:
            info = self.fetch_information(question, lang) if question else \
                   "Please consult a doctor for detailed advice."
            response = f"Hello {patient_name}, aged {age}. {info}"
            translated_response = self.speech_system.speak(response, voice='female', lang=lang)
            return translated_response
        except Exception as e:
            logger.error(f"Nurse mode error: {str(e)}")
            return "An error occurred while processing your request."

    def child_assistant(self, question, lang='en'):
        """Child Mode: Answers questions conversationally."""
        try:
            response = self.fetch_information(question, lang)
            translated_response = self.speech_system.speak(response, voice='male', lang=lang)
            return translated_response
        except Exception as e:
            logger.error(f"Child assistant error: {str(e)}")
            return "I'm sorry, I couldn't process your question."

def listen():
    """Listen for voice commands."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            logger.error("Speech recognition error: Could not understand audio")
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            logger.error("Speech recognition service unavailable")
            return "Speech recognition service is unavailable."

# Create assistant instance
assistant = Assistant()

# Build Gradio interface
with gr.Blocks() as chatbot:
    gr.Markdown("### Assistive Nurse & Child Care Chatbot with Multilingual Support")
    
    with gr.Tab("Nurse Mode"):
        patient_name = gr.Textbox(label="Patient Name")
        age = gr.Number(label="Age")
        symptoms = gr.Textbox(label="Symptoms")
        question = gr.Textbox(label="Ask a Health Question")
        lang = gr.Textbox(label="Language (e.g., en, fr, es)", value="en")
        output = gr.Textbox(label="Response")
        submit = gr.Button("Get Advice")
        voice_command = gr.Button("Speak Command")
        
        submit.click(
            lambda n, a, s, q, l: assistant.assistive_nurse(n, a, s, q, l),
            inputs=[patient_name, age, symptoms, question, lang],
            outputs=output
        )
        voice_command.click(
            lambda: assistant.assistive_nurse(listen(), listen(), listen(), listen(), listen()),
            outputs=output
        )
    
    with gr.Tab("Child Mode"):
        child_question = gr.Textbox(label="Ask me anything!")
        lang = gr.Textbox(label="Language (e.g., en, fr, es)", value="en")
        child_output = gr.Textbox(label="Response")
        child_submit = gr.Button("Ask")
        child_voice_command = gr.Button("Speak Question")
        
        child_submit.click(
            lambda q, l: assistant.child_assistant(q, l),
            inputs=[child_question, lang],
            outputs=child_output
        )
        child_voice_command.click(
            lambda: assistant.child_assistant(listen(), listen()),
            outputs=child_output
        )

if __name__ == "__main__":
    chatbot.launch(share=True)