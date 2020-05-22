import PySimpleGUI as sg
import json
import random

def llenar_bolsa(nivel):
    with open('Letras.json','r') as archivo_letras:
        letras = json.load(archivo_letras)
        letrasN = letras[nivel]
        bolsa = []
        for letra, cantidad in letrasN.items():
            for i in range(1,cantidad+1):
                bolsa.append(letra)
    return bolsa

def cargar_puntajes():
    with open('Puntajes.json','r') as archivo_puntajes:
        puntajes = json.load(archivo_puntajes)
    return puntajes

bolsa = llenar_bolsa('nivel1')
puntajes = cargar_puntajes()

columna0 = ['','','','']
columna1 = ['','','','']
columna2 = ['','','','']
columna3 = ['','','','']

columnas = [columna0,columna1,columna2,columna3]

casillas = ['00','01','02','03','10','11','12','13','20','21','22','23','30','31','32','33']
atril = ['J1','J2','J3','J4','J5','J6','J7']

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

tablero = [
    [sg.Button('',visible=False,key='C1'),sg.Button('',visible=False,key='C2'),sg.Button('',visible=False,key='C3'),sg.Button('',visible=False,key='C4'),sg.Button('',visible=False,key='C5'),sg.Button('',visible=False,key='C6'),sg.Button('',visible=False,key='C7'),sg.Button('',size=(3,4)),sg.Button('',size=(3,4)),sg.Button('',size=(3,4)),sg.Button('',size=(3,4)),sg.Button('',size=(3,4)),sg.Button('',size=(3,4)),sg.Button('',size=(3,4))],
    [sg.Column(col0), sg.Column(col1), sg.Column(col2), sg.Column(col3)],
    [sg.Button('',size=(3,4),key='J1'),sg.Button('',size=(3,4),key='J2'),sg.Button('',size=(3,4),key='J3'),sg.Button('',size=(3,4),key='J4'),sg.Button('',size=(3,4),key='J5'),sg.Button('',size=(3,4),key='J6'),sg.Button('',size=(3,4),key='J7')]
]

window = sg.Window('Tablero').Layout(tablero).Finalize()

for i in range(1,8):
    aux = 'C'+str(i)
    indice = random.randrange(len(bolsa))
    window.Element(aux).Update(text=bolsa[indice])
    del bolsa[indice]

for i in range(1,8):
    aux = 'J'+str(i)
    indice = random.randrange(len(bolsa))
    window.Element(aux).Update(text=bolsa[indice])
    del bolsa[indice]

posAtril = ''
letra = ''
palabra = [] #despues hay que hacer un .join('')

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event in atril:
        posAtril = event
        letra = window.Element(posAtril).GetText()
        print(posAtril)
        print(letra)
    elif event in casillas:
        if posAtril != '':
            window.Element(event).Update(text=letra)
            window.Element(posAtril).Update(text='')
            palabra.append(letra) #voy guardando las letras para despues ver si es una palabra
            posAtril = ''
            letra = ''
window.Close()
