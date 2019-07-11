from chatterbot import ChatBot #Librería para el Bot
from chatterbot.trainers import ChatterBotCorpusTrainer #Librería entrenar al bot con conversaciones prediseñadas
from chatterbot.trainers import ListTrainer #Librería para entrenar al Bot con distintos entrenadores o trainers
import pyttsx3 #Librería para convertir texto a voz
import sys #Librería para funciones directamente con el intérprete
from chatterbot.response_selection import get_random_response #Para el adaptador lógico de respuesta aleatoria
import datetime #Librería para obtener datos relacionados con la fecha (hora, día, mes, etcétera)
import os #Librería para acceder a funcionalidades dependientes del Sistema Operativo
import random #Librería para trabajar con la aleatoridad
import mysql.connector #Librería para la conexión de py y mysql
import modulo_1 #Módulo encargado del aprendizaje del bot
import modulo_2 #Módulo encargado del aprendizaje del bot
import modulo_3 #Módulo encargado del aprendizaje del bot

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
    storage_adapter='chatterbot.storage.SQLStorageAdapter', #Especificamos que la BD de conocimientos del bot será sqlite3
    logic_adapters=[
    'chatterbot.logic.MathematicalEvaluation', #¿Cuánto es 1+(-*/)2?, y el bot responderá al cálculo
    'chatterbot.logic.BestMatch', #Escoge la mejor respuesta
    ],
    preprocessors=[
    'chatterbot.preprocessors.clean_whitespace' #Elimina espacios en blanco
    ],
    response_selection_method=get_random_response #Cuando se encuentren varias respuestas
    #una sentencia de entrada, el bot escogerá aleatoriamente una de estas respuestas para
    #responde, esto hace que no sea monótono y las conversaciones sean más dinámicas
    )







trainer = ListTrainer(chatbot) #La variable trainer será el puntero para referenciar a la función 
#"ListTrainer(chatbot)"

#trainer.train("chatterbot.corpus.spanish") Con esta sentencia le enseñamos al Bot un grupo de 
#conversaciones en español prediseñadas que nos brinda ChatterBotCorpus


trainer.train([ #Comentar este fragmento después de la primera ejecución exitosa del programa
'Adios',
'Adios'
])

trainer.train([ #Comentar este fragmento después de la primera ejecución exitosa del programa
'Adios',
'Hasta luego'
])

trainer.train([ #Comentar este fragmento después de la primera ejecución exitosa del programa
'Hola',
'Hola'
])

trainer.train([ #Comentar este fragmento después de la primera ejecución exitosa del programa
'Hola',
'Hola'
])

trainer.train("chatterbot.corpus.spanish") #Comentar este fragmento después de la primera ejecución exitosa del programa

 


hora_de_inicio = datetime.datetime.now().strftime("%M") #Variable que usa para calcular
#cuánto tiempo ha pasado desde que el usuario inició el programa, y desde que el usuario activa
#la forma dos de aprendizaje del módulo_1
input1_usuario = 'Hola' #Se inicializa un input al bot para que responda con un saludo
contador_auto_aprendizaje = 0
input2_usuario = 0
cont_ciclo = 0 #Variable que cuenta cuántas veces se ha ejecutado el ciclo, solo se necesita para
#evitar que al principio del programa, el usuario digite que no es la respuesta correcta (Cuando
#obviamente no hay conversación, porque no se ha conversado a penas)

while True: #Acá se ejecuta todo el flujo entrada/salida de conversaciones con el bot, y el aprendizaje
    cont_ciclo += 1 

    if(str(input1_usuario) == "Bot esa no es la respuesta" and input2_usuario != 0 and cont_ciclo != 2): #Cuando nos encontramos con 
        #una respuesta incorrecta por parte del bot, entonces le decimos al bot; "Bot esa
        # no es la respuesta", con lo cual iremos al modulo_2 donde corregimos al bot
        #diciéndole cómo debería responder.
        modulo_2.aprendizaje2(input2_usuario)
        input1_usuario = input('ME: ')#Al volver del módulo donde se corrige al bot
        #debemos abrir nuevamente el flujo de entrada al usuario para la conversación 
        #en pocas palabras, que el usuario inicie ahora la conversación
        input2_usuario = 0
        while str(input1_usuario) == "Bot esa no es la respuesta":#Al volver del módulo_2 no podemos
        #decirle al bot nuevamente que no es la respuesta, dado que no se ha iniciado una conversación
            input1_usuario = input('ME: ')


    if(str(input1_usuario) == "Bot ya sé la respuesta"):#Cuando ya sabemos la respuesta
    #a una de las conversaciones de las que el bot no sabe responder, le decimos al bot; 
    #"Bot ya sé la respuesta", con esto el bot nos presentará una lista con las conversaciones
    #a las cuales el bot no sabe responder, seleccionaremos la conversación a la cual queremos
    #enseñarle al bot a responder, y le enseñaremos a responderla, también podemos decirlo
    #para enseñarle conversaciones al bot por nuestra cuenta
        modulo_3.aprendizaje3()
        input1_usuario = input('ME: ')
        input2_usuario = 0 #Al volver del módulo 2 y 3 es necesario 
        while str(input1_usuario) == "Bot esa no es la respuesta":#Al volver del módulo_3 no podemos
        #decirle al bot que no es la respuesta, dado que no se ha iniciado una conversación
            input1_usuario = input('ME: ')
        continue

       
    response = chatbot.get_response(str(input1_usuario))
    
    if float(response.confidence) > 0.5: #El bot solo responde si la respuesta es lo suficiente confiable, el nivel es de 0 a 1 en decimales
        print("Bot: ",response)
        engine.say(response)
        engine.runAndWait()
        if cont_ciclo != 1:
            input2_usuario = input1_usuario

    
    elif(str(input1_usuario) != "Bot esa no es la respuesta" and str(input1_usuario) != "Bot ya sé la respuesta"):
        hora_de_inicio = modulo_1.aprendizaje1(input1_usuario, hora_de_inicio)
    #Si el nivel de confianza de la respuesta del bot no es lo suficientemente confiable,
    #y además el input del usuario no es ninguna de las palabras clave para el aprendizaje
    #del bot, entonces significa que el bot no sabe responder a tal conversación, por lo
    #tanto el bot le dice al usuario que no sabe responder a tal conversación y que por favor
    #le enseñe 

    if str(response) == 'Adios' or str(response) == 'Hasta luego':       
        sys.exit()
    #Si la respuesta del bot es "Adios", o "Hasta luego", entonces significa que se están
    #despidiendo, por lo tanto la conversación ha concluido y el programa se cierra.
    #Para que el bot responda con un "Adios" o "Hasta luego", es necesario que el
    #input del usuario sea "Adios", "Chao", o "Hasta luego"
    #también se le puede enseñar al bot a que diga "Adios" o "Hasta luego" a otras conversaciones 
    #o inputs.

        
    input1_usuario = input('ME: ')





#Designed by CABA 2019
#Universidad de la Guajira sede Maicao 
