from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import pyttsx3
import sys 
import getpass
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



usuario = getpass.getuser()   
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



def aprendizaje3():
    cont = 0
    preguntas = []
    sql = 'SELECT * FROM preguntas'
    cursor.execute(sql)
    consulta = cursor.fetchall() #La variable consulta se convierte en un vector que 
    #en cada índice contiene un registro de la consulta hecha
    print("( B ) Olvidé la respuesta\n( A ) Enseñar otra conversación ")

    for i in consulta: #i en cada ciclo valor de cada índice del vector "consulta"
        preguntas.append(i[1]) #El vector "preguntas" se llena con el campo 1 de cada registro
    
    for i in preguntas: #imprimimos las preguntas
        print('(', cont,')', i)
        cont += 1
    
    print("¿A qué conversación le sabes la respuesta?\nDigita el número correspondiente")
    engine.say("¿A qué conversación le sabes la respuesta?. Digita el número correspondiente")
    engine.runAndWait()
    a = input('Digita un número entero: ')

    while True:

        if a == 'A' or a == 'a': 
            print("A continuación digita la frase, y luego su respuesta")
            engine.say("A continuación digita la frase, y luego su respuesta")
            engine.runAndWait()    
            frase = input('Frase: ')
            respuesta = input('Respuesta: ')
            try:
                trainer.train([ 
                frase,
                str(respuesta)
                ])
            except: 
                print("Hubo un problema al intentar entrenar al bot")

            else:
                print("Conversación aprendida exitosamente")
                engine.say("Conversación aprendida exitosamente")
                engine.runAndWait() 
                return  

                      
        if a == 'b' or a == 'B': #Si digitó b significa que quiere salir
            return

        try: a = int(a)  #Si se puede convertir a entero entonces se va al else
        except ValueError: #Si no se cumple el try y la razón es por un "ValueError"
            a = input('Digita un número entero: ') #Se pide nuevamente que ingresen el valor y luego con el continue
            continue #se vuelve al principio del while
        else:  #Si el digito es un número entero, ahora toca comprobar si es uno de la lista de preguntas mostradas
            if a >= 0 and a <= len(preguntas)-1: #len arroja el tamaño del vector,
            #recordemos que el tamaño se cuenta desde el 1, por lo tanto debemos restar para que cuente el índice cero
                break  #rompemos el ciclo ya que el digito es válido
            else: 
                a = input('Digita uno de los números de la lista: ')
                continue #Aunque el número es entero, no es ninguno de los que está en
                #la lista, por lo tanto seguimos el ciclo
                
                
    

    frase = preguntas[a] #La variable "frase" tendrá la frase escogida 
    
    print("Ahora digita la respuesta")
    engine.say("Ahora digita la respuesta")
    engine.runAndWait()
    respuesta = input('Respuesta: ')
    try:
        trainer.train([ 
        frase,
        str(respuesta)
        ])

    except: 
        print("Hubo un problema al intentar entrenar al bot")
    else:  #Si se aprendió a responder a tal frase, entonces debemos eliminarla de la BD de preguntas(frases) sin responder
        sql_eliminar_pregunta = 'DELETE FROM `bd_preguntas`.`preguntas` WHERE pregunta=%s'
        cursor.execute(sql_eliminar_pregunta,(frase,))
        conexion.commit()   
        print("Conversación aprendida exitosamente")
        engine.say("Conversación aprendida exitosamente")
        engine.runAndWait() 

    return