import gradio as gr
gr.load_chat("http://localhost:11434/v1/", model="llama3.2", token="ollama").launch()


# import random

# def random_response(message, history):
#     return random.choice(["Yes", "No"])

# gr.ChatInterface(
#     fn=random_response,
#     type="messages"
#     ).lunch()

def alternatingly_agree(message, history):
    if len([h for h in history if h['role'] == "assistant"]) % 2 == 0:
        return f"Yes, I do think that: {message}"
    else:
        return "I don't think so"
    
gr.ChatInterface(
    fn=alternatingly_agree,
    type="messages"
).launch()


# Streaming ChatBot
import time 
import gradio as gr

def slow_echo(message, history):
    for i in range(len(message)):
        time.sleep(0.3)
        yield "You typed: " + message[: i+1]

gr.ChatInterface(
    fn=slow_echo,
    type="messages"
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> b84fe18 (chat ChatBot1)
).launch()



import gradio as gr

def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
<<<<<<< HEAD
demo.lunch()
gr.load_chat
(Add voice and the app searches online
).launch()(Chatbots)
=======
demo.lunch()
>>>>>>> b84fe18 (chat ChatBot1)
