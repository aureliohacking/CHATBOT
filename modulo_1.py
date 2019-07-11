from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import pyttsx3
import sys
import datetime 
from chatterbot.response_selection import get_random_response
import os
import random
import mysql.connector



datos_conexion = {
    'host':'localhost',
    'user':'root',
    'password':'12345678',
    'database':'bd_preguntas'    #Base de datos o modelo sobre el cual trabajaremos
}
#Datos de la conexión

conexion = mysql.connector.connect(**datos_conexion)

cursor = conexion.cursor()
#Conexión a la bd y demás


   
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


def aprendizaje1(frase,hora_de_inicio):
    global conexion, cursor, datos_conexion
    preguntas = []
    sql = 'SELECT * FROM preguntas'
    cursor.execute(sql)
    consulta = cursor.fetchall()
    for i in consulta: 
        preguntas.append(i[1]) 
    #Consultamos las preguntas sin responder, más adelante se usan    



    print("Bot: Lo siento, no entendí \n¿Puedes explicarme qué respuesta dar a tal conversación?")
    engine.say("Lo siento, no entendí. ¿Puedes explicarme qué respuesta dar a tal conversación?")
    engine.runAndWait()

    aux = input('Si = S \nNo = Cualquier caracter\n-->')

    if(str(aux) == 'S' or str(aux) == 's'):
        print("Bot: Digita la frase adecuada para responder a: ",frase)
        engine.say("Digita la frase adecuada para responder a: ",frase)
        engine.runAndWait()
        respuesta = input('Respuesta: ')
        trainer.train([ 
        frase,
        str(respuesta)
        ])
        print("Bot: Aprendido")
        engine.say("Aprendido")
        engine.runAndWait()
        return hora_de_inicio #La función siempre retorna la hora inicial
    else: 
        if(str(frase in preguntas) == 'False'): 

            sql_insertar_pregunta = "INSERT INTO `bd_preguntas`.`preguntas`(`pregunta`)VALUES(%s)"   
            cursor.execute(sql_insertar_pregunta,(frase,))#se coloca la coma porque es solo un dato, 
            #si son más datos la coma ya no se pone al final
            conexion.commit()#Con este terminamos de hacer la consulta de inserción

        print("Entonces cambiemos de tema, cuando sepas la respuesta me enseñas")
        engine.say("Entonces cambiemos de tema, cuando sepas la respuesta me enseñas")
        engine.runAndWait()
        
        
        if(len(preguntas) > 0):
            hay_preguntas_para_hacer = True
        else:
            hay_preguntas_para_hacer = False           


        if((int(datetime.datetime.now().strftime("%M")) - int(hora_de_inicio)) > 4 and hay_preguntas_para_hacer == True):
               
            pregunta_escogida = random.choice(preguntas)
            

            print("A proposito, ¿Ya sabes cómo responder a esta conversación?")
            print("\n \"",pregunta_escogida,"\"")
            engine.say("A propósito, ¿Ya sabes cómo responder a esta conversación?")
            engine.runAndWait()
            aux = input('Si = S \nNo = Cualquier caracter\n-->')

            if(str(aux) == 'S' or str(aux) == 's'):
                print("Entonces digita a continuación cómo responder a: ",pregunta_escogida)
                engine.say("Entonces digita a continuación cómo responder a")
                engine.runAndWait() 
                respuesta = input('Respuesta: ')
                try:
                    trainer.train([ 
                    str(pregunta_escogida),
                    str(respuesta)
                    ]) 
                except: 
                    print("Hubo un problema al entrenar al bot")
                else:        

                    sql_eliminar_pregunta = 'DELETE FROM `bd_preguntas`.`preguntas` WHERE pregunta=%s'
                    cursor.execute(sql_eliminar_pregunta,(pregunta_escogida,))
                    conexion.commit()   
                    print("Conversación aprendida exitosamente")
                    engine.say("Conversación aprendida exitosamente")
                    engine.runAndWait() 
                    hora_de_inicio = datetime.datetime.now().strftime("%M")
                    return hora_de_inicio

            else:
                print("Ok, será en otra ocasión")
                engine.say("Ok, será en otra ocasión")
                engine.runAndWait()   
                return hora_de_inicio 

    return hora_de_inicio        
