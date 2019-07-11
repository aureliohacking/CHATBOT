from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import pyttsx3
import sys 
from chatterbot.response_selection import get_random_response 
import os


   
engine = pyttsx3.init()
voices = engine.getProperty('voices') #a voices se le carga un vector con la información de todas las voces
#getPropierty es para obtener información de algo, ya sea el volumen o la velocidad con que habla
engine.setProperty('voice', voices[0].id) #setProperty es para cambiar una propiedad, ya sea voz o volumen
volume = engine.getProperty('volume') #para obtener el volumen actual
engine.setProperty('volume', volume+1.0)#cambiar el volumen
rate = engine.getProperty('rate')#para obtener la velocidad actual
engine.setProperty('rate', rate-80)#cambiar la velocidad con que habla



chatbot = ChatBot(
    'Terminal',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
    'chatterbot.logic.MathematicalEvaluation',
    'chatterbot.logic.BestMatch',
    ],
    preprocessors=[
    'chatterbot.preprocessors.clean_whitespace'
    ],
    response_selection_method=get_random_response
    ) 



trainer = ListTrainer(chatbot) 



def aprendizaje2(frase):
    print("Bot: Perdón, no soy experto en el lenguaje natural. Digita la frase adecuada para responder a: ",frase)
    engine.say("Perdón, no soy experto en el lenguaje natural. Digita la frase adecuada para responder a: ",frase)
    engine.runAndWait()
    respuesta = input('Corrección: ')
    trainer.train([ 
    frase,
    str(respuesta)
    ])
    print("Bot: Gracias por corregirme")
    engine.say("Gracias por corregirme")
    engine.runAndWait()
    return