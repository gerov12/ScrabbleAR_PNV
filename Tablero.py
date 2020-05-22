import PySimpleGUI as sg
import json
import random

def llenar_bolsa(nivel = 'nivel1'): #carga las cantides para c/ letra segun el nivel ingresado por parametro
    #nivel por defecto es el 1
    with open('Letras.json','r') as archivo_letras:
        letras = json.load(archivo_letras)
        letrasN = letras[nivel] #toma el diccionario de letras:cantidades del nivel correspondiente
        bolsa = [] #bolsa de letras para repartir a los jugadores
        for letra, cantidad in letrasN.items():
            for i in range(1,cantidad+1): #guarda "cantidad" veces la letra correspondiente
                bolsa.append(letra)
    return bolsa

def cargar_puntajes(): #carga los puntajes para c/ letra
    with open('Puntajes.json','r') as archivo_puntajes:
        puntajes = json.load(archivo_puntajes)
    return puntajes

bolsa = llenar_bolsa() #el nivel se manda como parametro
puntajes = cargar_puntajes()

#keys de las casillas y las posiciones del atril (se usa mas adelante)
casillas = ['00','01','02','03','10','11','12','13','20','21','22','23','30','31','32','33']
atril = ['J1','J2','J3','J4','J5','J6','J7']

#columnas
col0 = [
    [sg.Button('',size=(3,4),key = '03')],
    [sg.Button('',size=(3,4),key = '02')],
    [sg.Button('',size=(3,4),key = '01')],
    [sg.Button('',size=(3,4),key = '00')],
]

col1 = [
    [sg.Button('',size=(3,4),key = '13')],
    [sg.Button('',size=(3,4),key = '12')],
    [sg.Button('',size=(3,4),key = '11')],
    [sg.Button('',size=(3,4),key = '10')],
]

col2 = [
    [sg.Button('',size=(3,4),key = '23')],
    [sg.Button('',size=(3,4),key = '22')],
    [sg.Button('',size=(3,4),key = '21')],
    [sg.Button('',size=(3,4),key = '20')],
]

col3 = [
    [sg.Button('',size=(3,4),key = '33')],
    [sg.Button('',size=(3,4),key = '32')],
    [sg.Button('',size=(3,4),key = '31')],
    [sg.Button('',size=(3,4),key = '30')],
]

#layout del tablero
tablero = [
    [sg.Button('',visible=False,key='C1'),sg.Button('',visible=False,key='C2'),sg.Button('',visible=False,key='C3'),sg.Button('',visible=False,key='C4'),sg.Button('',visible=False,key='C5'),sg.Button('',visible=False,key='C6'),sg.Button('',visible=False,key='C7'),sg.Button('',size=(3,4)),sg.Button('',size=(3,4)),sg.Button('',size=(3,4)),sg.Button('',size=(3,4)),sg.Button('',size=(3,4)),sg.Button('',size=(3,4)),sg.Button('',size=(3,4))],
    #los botones invisibles (visible=false) guardan las letras del atril de la maquina
    #y los 7 botones vacios del final son de fachada
    [sg.Column(col0), sg.Column(col1), sg.Column(col2), sg.Column(col3)], #columnas una al lado de la otra
    [sg.Button('',size=(3,4),key='J1'),sg.Button('',size=(3,4),key='J2'),sg.Button('',size=(3,4),key='J3'),sg.Button('',size=(3,4),key='J4'),sg.Button('',size=(3,4),key='J5'),sg.Button('',size=(3,4),key='J6'),sg.Button('',size=(3,4),key='J7')]
    #atril del jugador
]
#los botones se incializan en '' pero después al texto se le van cargando las letras

window = sg.Window('Tablero').Layout(tablero).Finalize()
#Finalize() hace una especie de lectura de la ventana para que los cambios a los botones se apliquen

for i in range(1,8): #de 1 a 7
    aux = 'C'+str(i) #aux es la key de la pos del atril de la Computadora a actualizar
    indice = random.randrange(len(bolsa)) #tomo una letra random de la bolsa de letras
    window.Element(aux).Update(text=bolsa[indice]) #la pongo como texto del boton correspondiente
    del bolsa[indice] #la elimino de la bolsa

for i in range(1,8): #lo mismo pero para el atril del Jugador
    aux = 'J'+str(i)
    indice = random.randrange(len(bolsa))
    window.Element(aux).Update(text=bolsa[indice])
    del bolsa[indice]

posAtril = '' #posicion en el atril de la letra clickeada
letra = '' #letra clickeada
palabra = [] #despues hay que hacer un .join('')

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event in atril: #si hago click en una letra del atril
        posAtril = event #guarda la posicion en el atril de la letra clickeada
        letra = window.Element(posAtril).GetText() #guarda la letra clickeada
    elif event in casillas:#si hago click en una casilla del tablero
        if posAtril != '': #si previamente clickee una letra del atril
            window.Element(event).Update(text=letra) #la pongo como texto del casillero elegido
            window.Element(posAtril).Update(text='') #la elimino del atril (reemplazandola por '')
            palabra.append(letra) #voy guardando las letras para despues ver si es una palabra
            posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
            letra = '' #idem
window.Close()
