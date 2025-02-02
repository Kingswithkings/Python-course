import gradio as gr
import random
import speech_recognition as sr
import pyttsx3
import openai
from googletrans import Translator

engine = pyttsx3.init()
voices = engine.getProperty('voices')


def speak(text, voice='default', lang='en'):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voice == 'female':
        engine.setProperty('voice', voices[1].id)
    elif voice == 'male':
        engine.setProperty('voice, voices[0].id')


translator = Translator()
translated_text = translator.translate(text, dest=lang).text
engine.say(translated_text)
engine.runAndWait()
return translated_text     


engine.say("Text-to-Speech system initialized sucessfully.")
engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            return "Sorry, I didnt catch that."
        except sr.RequestError:
            return "Speech recognition service is unavailable."
        

def fetch_information(question, lang='en'):
    """
    Uses OpenAI to fetch accurate and detailed information.
    """
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": question}]
    )


def assistive_nurse(patient_name, age, symptons, question, lang='en'):
    """
    Nurse Mode: Collects patient data and provides health advice.
    """
    info = fetch_information(question, lang) if question else "Please consult a doctor for detailed advise."
    response = f"Hello {patient_name}, aged {age}. {info}"
    translated_reponse = speak(response, voice='female', lang=lang)
    return translated_reponse


def child_assistant(question, lang='en'):
    """
    Child Mode: Answers questions conversationally.
    """
    response = fetch_information(question, lang)
    translated_response = speak(response, voice='male', lang=lang)
    return translated_response


with gr.Blocks() as chatbot:
    gr.Markdown("### Assistive Nurse & Child care Chatbot with Multilingual Support")

    with gr.Tab("Nurse Mode"):
        patient_name = gr.Textbox(label="Patient Name")
        age = gr.Number(label="Age")
        symptoms = gr.Textbox(label="Symptoms")
        question = gr.Textbox(label="Ask a Health Question")
        lang = gr.Textbox(label="Language (e.g., en, fr, es)", value="en")
        output = gr.Textbox(label="Response")
        submit = gr.Button("Get Advice")
        voice_command = gr.Button("Speak Command")


        submit.click(assistive_nurse, inputs=[patient_name, age, symptoms, question, lang], outputs=output)
        voice_command.click(lambda: assistive_nurse(listen(), listen(), listen(), listen(), listen()), outputs=output)

with gr.Tab("Child Mode"):
    child_question = gr.Textbox(label="Ask me anything!")
    lang = gr.Textbox(label="Language (e.g., en, fr, es)", value="en")
    child_output = gr.Textbox(label="Response")
    child_submit = gr.Button("Ask")
    child_voice_command = gr.Button("speak Question")


    child_submit.click(child_assistant, inputs=[child_question, lang], outputs=child_output)
    child_voice_command.click(lambda: child_assistant(listen(), listen()), outputs=child_output)

    chatbot.launch()
