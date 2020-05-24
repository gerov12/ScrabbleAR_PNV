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

def colocar_letra(casilla, posA, let, pal): #pone la letra en la casilla correspondiente y la saca del atril
    window.Element(casilla).Update(text=let) #pongo la letra "let" como texto de la "casilla" clickeada
    window.Element(posA).Update(text='') #la elimino del atril (reemplazandola por '')
    palabra.append(let) #guardo la letra en la lista de letras para luego verificar si es una palabra

def consecutivo(casilla): #indica si la casilla seleccionada es consecutivo a la letra anteriormente colocada
    aux = False
    orient = ''
    izquierda = str((int(casilla[0])-1))+casilla[1] #(el primer digito-1)+el segundo digito (es decir la casilla de la izquierda)
    arriba = casilla[0]+str((int(casilla[1])+1)) #el primer digito+(el segundo digito+1) (es decir la casilla de arriba)
    if izquierda[0]!='-': #si el primer digito de "izquierda" no es '-' (es decir que no elegí una casilla de la columna 0)
        if window.Element(izquierda).GetText() != '': #si el elemento de la izquierda no está vacío
            aux = True #elegí una casilla consecutiva a la primer letra
            orient = 'Horizontal' #y comencé a armar la palabra de manera horizontal
            return [aux, orient]
    if int(arriba[1])<4: #si no elegí una casilla correcta para la orientacion horizontal chequeo si es vertical
    #si el sgundo digito de la casilla de arriba es menor a 4 (es decir que no elegí una casilla de la fila 3)
    #(el 4 mas adelante debería cambiarse por la altura del tablero)
        if window.Element(arriba).GetText() != '': #si el elemento de arriba no está vacío
            aux = True #elegí una casilla consecutiva a la primer letra
            orient = 'Vertical' #y comencé a armar la palabra de manera vertical
            return [aux, orient]
    return [aux, orient] #devuelve Flase y ''

def orientada(casilla, orient): #indica si seleccione una casilla correcta según la orientacion definida
    aux = False
    if orient == 'Horizontal': #si la orientacion es horizontal hago el chequeo correspondiente
        izquierda = str((int(casilla[0])-1))+casilla[1]
        if izquierda[0]!='-':
            if window.Element(izquierda).GetText() != '':
                aux = True
    elif orient == 'Vertical': #si la orientacion es vertical hago el chequeo correspondiente
        arriba = casilla[0]+str((int(casilla[1])+1))
        if arriba[1]!='4':
            if window.Element(arriba).GetText() != '':
                aux = True
    return aux

bolsa = llenar_bolsa() #el nivel se manda como parametro
puntajes = cargar_puntajes()

#keys de las casillas y las posiciones del atril (se usa mas adelante)
casillas = ['00','01','02','03','10','11','12','13','20','21','22','23','30','31','32','33']
atril = ['J1','J2','J3','J4','J5','J6','J7']

#columnas
# for i in range(15):
#     if len(str(i)) == 1:
#         col{}.format(i) = [
#             [sg.Button('',size=(3,4),key = '0{}14'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}13'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}12'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}11'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}10'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}09'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}08'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}07'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}06'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}05'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}04'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}03'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}02'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}01'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '0{}00'.format(str(i)))],
#         ]
#     else:
#         col{}.format(i) = [
#             [sg.Button('',size=(3,4),key = '{}14'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}13'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}12'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}11'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}10'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}09'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}08'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}07'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}06'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}05'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}04'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}03'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}02'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}01'.format(str(i)))],
#             [sg.Button('',size=(3,4),key = '{}00'.format(str(i)))],
#         ]


# col0 = [
#     [sg.Button('',size=(3,4),key = '0014')],
#     [sg.Button('',size=(3,4),key = '0013')],
#     [sg.Button('',size=(3,4),key = '0012')],
#     [sg.Button('',size=(3,4),key = '0011')],
#     [sg.Button('',size=(3,4),key = '0010')],
#     [sg.Button('',size=(3,4),key = '0009')],
#     [sg.Button('',size=(3,4),key = '0008')],
#     [sg.Button('',size=(3,4),key = '0007')],
#     [sg.Button('',size=(3,4),key = '0006')],
#     [sg.Button('',size=(3,4),key = '0005')],
#     [sg.Button('',size=(3,4),key = '0004')],
#     [sg.Button('',size=(3,4),key = '0003')],
#     [sg.Button('',size=(3,4),key = '0002')],
#     [sg.Button('',size=(3,4),key = '0001')],
#     [sg.Button('',size=(3,4),key = '0000')],
# ]
#
# col1 = [
#     [sg.Button('',size=(3,4),key = '0114')],
#     [sg.Button('',size=(3,4),key = '0113')],
#     [sg.Button('',size=(3,4),key = '0112')],
#     [sg.Button('',size=(3,4),key = '0111')],
#     [sg.Button('',size=(3,4),key = '0110')],
#     [sg.Button('',size=(3,4),key = '0109')],
#     [sg.Button('',size=(3,4),key = '0108')],
#     [sg.Button('',size=(3,4),key = '0107')],
#     [sg.Button('',size=(3,4),key = '0106')],
#     [sg.Button('',size=(3,4),key = '0105')],
#     [sg.Button('',size=(3,4),key = '0104')],
#     [sg.Button('',size=(3,4),key = '0103')],
#     [sg.Button('',size=(3,4),key = '0102')],
#     [sg.Button('',size=(3,4),key = '0101')],
#     [sg.Button('',size=(3,4),key = '0100')],
# ]
#
# col2 = [
#     [sg.Button('',size=(3,4),key = '0214')],
#     [sg.Button('',size=(3,4),key = '0213')],
#     [sg.Button('',size=(3,4),key = '0212')],
#     [sg.Button('',size=(3,4),key = '0211')],
#     [sg.Button('',size=(3,4),key = '0210')],
#     [sg.Button('',size=(3,4),key = '0209')],
#     [sg.Button('',size=(3,4),key = '0208')],
#     [sg.Button('',size=(3,4),key = '0207')],
#     [sg.Button('',size=(3,4),key = '0206')],
#     [sg.Button('',size=(3,4),key = '0205')],
#     [sg.Button('',size=(3,4),key = '0204')],
#     [sg.Button('',size=(3,4),key = '0203')],
#     [sg.Button('',size=(3,4),key = '0202')],
#     [sg.Button('',size=(3,4),key = '0201')],
#     [sg.Button('',size=(3,4),key = '0200')],
# ]
#
# col3 = [
#     [sg.Button('',size=(3,4),key = '0314')],
#     [sg.Button('',size=(3,4),key = '0313')],
#     [sg.Button('',size=(3,4),key = '0312')],
#     [sg.Button('',size=(3,4),key = '0311')],
#     [sg.Button('',size=(3,4),key = '0310')],
#     [sg.Button('',size=(3,4),key = '0309')],
#     [sg.Button('',size=(3,4),key = '0308')],
#     [sg.Button('',size=(3,4),key = '0307')],
#     [sg.Button('',size=(3,4),key = '0306')],
#     [sg.Button('',size=(3,4),key = '0305')],
#     [sg.Button('',size=(3,4),key = '0304')],
#     [sg.Button('',size=(3,4),key = '0303')],
#     [sg.Button('',size=(3,4),key = '0302')],
#     [sg.Button('',size=(3,4),key = '0301')],
#     [sg.Button('',size=(3,4),key = '0300')],
# ]
#
# col4 = [
#     [sg.Button('',size=(3,4),key = '0414')],
#     [sg.Button('',size=(3,4),key = '0413')],
#     [sg.Button('',size=(3,4),key = '0412')],
#     [sg.Button('',size=(3,4),key = '0411')],
#     [sg.Button('',size=(3,4),key = '0410')],
#     [sg.Button('',size=(3,4),key = '0409')],
#     [sg.Button('',size=(3,4),key = '0408')],
#     [sg.Button('',size=(3,4),key = '0407')],
#     [sg.Button('',size=(3,4),key = '0406')],
#     [sg.Button('',size=(3,4),key = '0405')],
#     [sg.Button('',size=(3,4),key = '0404')],
#     [sg.Button('',size=(3,4),key = '0403')],
#     [sg.Button('',size=(3,4),key = '0402')],
#     [sg.Button('',size=(3,4),key = '0401')],
#     [sg.Button('',size=(3,4),key = '0400')],
# ]
#
# col5 = [
#     [sg.Button('',size=(3,4),key = '0514')],
#     [sg.Button('',size=(3,4),key = '0513')],
#     [sg.Button('',size=(3,4),key = '0512')],
#     [sg.Button('',size=(3,4),key = '0511')],
#     [sg.Button('',size=(3,4),key = '0510')],
#     [sg.Button('',size=(3,4),key = '0509')],
#     [sg.Button('',size=(3,4),key = '0508')],
#     [sg.Button('',size=(3,4),key = '0507')],
#     [sg.Button('',size=(3,4),key = '0506')],
#     [sg.Button('',size=(3,4),key = '0505')],
#     [sg.Button('',size=(3,4),key = '0504')],
#     [sg.Button('',size=(3,4),key = '0503')],
#     [sg.Button('',size=(3,4),key = '0502')],
#     [sg.Button('',size=(3,4),key = '0501')],
#     [sg.Button('',size=(3,4),key = '0500')],
# ]
#
# col6 = [
#     [sg.Button('',size=(3,4),key = '0614')],
#     [sg.Button('',size=(3,4),key = '0613')],
#     [sg.Button('',size=(3,4),key = '0612')],
#     [sg.Button('',size=(3,4),key = '0611')],
#     [sg.Button('',size=(3,4),key = '0610')],
#     [sg.Button('',size=(3,4),key = '0609')],
#     [sg.Button('',size=(3,4),key = '0608')],
#     [sg.Button('',size=(3,4),key = '0607')],
#     [sg.Button('',size=(3,4),key = '0606')],
#     [sg.Button('',size=(3,4),key = '0605')],
#     [sg.Button('',size=(3,4),key = '0604')],
#     [sg.Button('',size=(3,4),key = '0603')],
#     [sg.Button('',size=(3,4),key = '0602')],
#     [sg.Button('',size=(3,4),key = '0601')],
#     [sg.Button('',size=(3,4),key = '0600')],
# ]
#
# col7 = [
#     [sg.Button('',size=(3,4),key = '0714')],
#     [sg.Button('',size=(3,4),key = '0713')],
#     [sg.Button('',size=(3,4),key = '0712')],
#     [sg.Button('',size=(3,4),key = '0711')],
#     [sg.Button('',size=(3,4),key = '0710')],
#     [sg.Button('',size=(3,4),key = '0709')],
#     [sg.Button('',size=(3,4),key = '0708')],
#     [sg.Button('',size=(3,4),key = '0707')],
#     [sg.Button('',size=(3,4),key = '0706')],
#     [sg.Button('',size=(3,4),key = '0705')],
#     [sg.Button('',size=(3,4),key = '0704')],
#     [sg.Button('',size=(3,4),key = '0703')],
#     [sg.Button('',size=(3,4),key = '0702')],
#     [sg.Button('',size=(3,4),key = '0701')],
#     [sg.Button('',size=(3,4),key = '0700')],
# ]
#
# col8 = [
#     [sg.Button('',size=(3,4),key = '0814')],
#     [sg.Button('',size=(3,4),key = '0813')],
#     [sg.Button('',size=(3,4),key = '0812')],
#     [sg.Button('',size=(3,4),key = '0811')],
#     [sg.Button('',size=(3,4),key = '0810')],
#     [sg.Button('',size=(3,4),key = '0809')],
#     [sg.Button('',size=(3,4),key = '0808')],
#     [sg.Button('',size=(3,4),key = '0807')],
#     [sg.Button('',size=(3,4),key = '0806')],
#     [sg.Button('',size=(3,4),key = '0805')],
#     [sg.Button('',size=(3,4),key = '0804')],
#     [sg.Button('',size=(3,4),key = '0803')],
#     [sg.Button('',size=(3,4),key = '0802')],
#     [sg.Button('',size=(3,4),key = '0801')],
#     [sg.Button('',size=(3,4),key = '0800')],
# ]
#
# col9 = [
#     [sg.Button('',size=(3,4),key = '0914')],
#     [sg.Button('',size=(3,4),key = '0913')],
#     [sg.Button('',size=(3,4),key = '0912')],
#     [sg.Button('',size=(3,4),key = '0911')],
#     [sg.Button('',size=(3,4),key = '0910')],
#     [sg.Button('',size=(3,4),key = '0909')],
#     [sg.Button('',size=(3,4),key = '0908')],
#     [sg.Button('',size=(3,4),key = '0907')],
#     [sg.Button('',size=(3,4),key = '0906')],
#     [sg.Button('',size=(3,4),key = '0905')],
#     [sg.Button('',size=(3,4),key = '0904')],
#     [sg.Button('',size=(3,4),key = '0903')],
#     [sg.Button('',size=(3,4),key = '0902')],
#     [sg.Button('',size=(3,4),key = '0901')],
#     [sg.Button('',size=(3,4),key = '0900')],
# ]
#
# col10 = [
#     [sg.Button('',size=(3,4),key = '1014')],
#     [sg.Button('',size=(3,4),key = '1013')],
#     [sg.Button('',size=(3,4),key = '1012')],
#     [sg.Button('',size=(3,4),key = '1011')],
#     [sg.Button('',size=(3,4),key = '1010')],
#     [sg.Button('',size=(3,4),key = '1009')],
#     [sg.Button('',size=(3,4),key = '1008')],
#     [sg.Button('',size=(3,4),key = '1007')],
#     [sg.Button('',size=(3,4),key = '1006')],
#     [sg.Button('',size=(3,4),key = '1005')],
#     [sg.Button('',size=(3,4),key = '1004')],
#     [sg.Button('',size=(3,4),key = '1003')],
#     [sg.Button('',size=(3,4),key = '1002')],
#     [sg.Button('',size=(3,4),key = '1001')],
#     [sg.Button('',size=(3,4),key = '1000')],
# ]
#
# col11 = [
#     [sg.Button('',size=(3,4),key = '1114')],
#     [sg.Button('',size=(3,4),key = '113')],
#     [sg.Button('',size=(3,4),key = '1112')],
#     [sg.Button('',size=(3,4),key = '1111')],
#     [sg.Button('',size=(3,4),key = '1110')],
#     [sg.Button('',size=(3,4),key = '1109')],
#     [sg.Button('',size=(3,4),key = '1108')],
#     [sg.Button('',size=(3,4),key = '1107')],
#     [sg.Button('',size=(3,4),key = '1106')],
#     [sg.Button('',size=(3,4),key = '1105')],
#     [sg.Button('',size=(3,4),key = '1104')],
#     [sg.Button('',size=(3,4),key = '1103')],
#     [sg.Button('',size=(3,4),key = '1102')],
#     [sg.Button('',size=(3,4),key = '1101')],
#     [sg.Button('',size=(3,4),key = '1100')],
# ]
#
# col12 = [
#     [sg.Button('',size=(3,4),key = '1214')],
#     [sg.Button('',size=(3,4),key = '1213')],
#     [sg.Button('',size=(3,4),key = '1212')],
#     [sg.Button('',size=(3,4),key = '1211')],
#     [sg.Button('',size=(3,4),key = '1210')],
#     [sg.Button('',size=(3,4),key = '1209')],
#     [sg.Button('',size=(3,4),key = '1208')],
#     [sg.Button('',size=(3,4),key = '1207')],
#     [sg.Button('',size=(3,4),key = '1206')],
#     [sg.Button('',size=(3,4),key = '1205')],
#     [sg.Button('',size=(3,4),key = '1204')],
#     [sg.Button('',size=(3,4),key = '1203')],
#     [sg.Button('',size=(3,4),key = '1202')],
#     [sg.Button('',size=(3,4),key = '1201')],
#     [sg.Button('',size=(3,4),key = '1200')],
# ]
#
# col13 = [
#     [sg.Button('',size=(3,4),key = '1314')],
#     [sg.Button('',size=(3,4),key = '1313')],
#     [sg.Button('',size=(3,4),key = '1312')],
#     [sg.Button('',size=(3,4),key = '1311')],
#     [sg.Button('',size=(3,4),key = '1310')],
#     [sg.Button('',size=(3,4),key = '1309')],
#     [sg.Button('',size=(3,4),key = '1308')],
#     [sg.Button('',size=(3,4),key = '1307')],
#     [sg.Button('',size=(3,4),key = '1306')],
#     [sg.Button('',size=(3,4),key = '1305')],
#     [sg.Button('',size=(3,4),key = '1304')],
#     [sg.Button('',size=(3,4),key = '1303')],
#     [sg.Button('',size=(3,4),key = '1302')],
#     [sg.Button('',size=(3,4),key = '1301')],
#     [sg.Button('',size=(3,4),key = '1300')],
# ]
#
# col14 = [
#     [sg.Button('',size=(3,4),key = '1414')],
#     [sg.Button('',size=(3,4),key = '1413')],
#     [sg.Button('',size=(3,4),key = '1412')],
#     [sg.Button('',size=(3,4),key = '1411')],
#     [sg.Button('',size=(3,4),key = '1410')],
#     [sg.Button('',size=(3,4),key = '1409')],
#     [sg.Button('',size=(3,4),key = '1408')],
#     [sg.Button('',size=(3,4),key = '1407')],
#     [sg.Button('',size=(3,4),key = '1406')],
#     [sg.Button('',size=(3,4),key = '1405')],
#     [sg.Button('',size=(3,4),key = '1404')],
#     [sg.Button('',size=(3,4),key = '1403')],
#     [sg.Button('',size=(3,4),key = '1402')],
#     [sg.Button('',size=(3,4),key = '1401')],
#     [sg.Button('',size=(3,4),key = '1400')],
# ]

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
    [sg.Column(col0), sg.Column(col1), sg.Column(col2), sg.Column(col3)],
    # sg.Column(col4), sg.Column(col5), sg.Column(col6), sg.Column(col7), sg.Column(col8), sg.Column(col9), sg.Column(col10), sg.Column(col11), sg.Column(col12), sg.Column(col13), sg.Column(col14)], #columnas una al lado de la otra
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
orientacion = ''

while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event in atril: #si hago click en una letra del atril
        posAtril = event #guarda la posicion en el atril de la letra clickeada
        letra = window.Element(posAtril).GetText() #guarda la letra clickeada
    elif event in casillas:#si hago click en una casilla del tablero
        if letra != '': #si previamente clickee una letra del atril
            if len(palabra) == 0: #si es la primer letra de la palabra
                colocar_letra(event, posAtril, letra, palabra)
                posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
                letra = '' #idem pero con la letra
            elif len(palabra) == 1: #si es la segunda letra de la palabra
                resultado = consecutivo(event)
                if resultado[0]: #si la casilla (event) seleccionada es consecutivo a la letra anteriormente colocada
                    orientacion = resultado[1] #guardo la orientacion
                    colocar_letra(event, posAtril, letra, palabra) #coloco la letra en la casilla
                    posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
                    letra = '' #idem pero con la letra
                    print(orientacion)
            elif len(palabra) > 1: #si es la letra 3 o mayor (ya está definida la orientacion)
                if orientada(event, orientacion): #si la casilla es consecutiva según la orientación definida
                    colocar_letra(event, posAtril, letra, palabra) #coloco la letra en la casilla
                    posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
                    letra = '' #idem pero con la letra
    # elif event == "Confirmar":
    #     orientacion = ''
    #     word = palabra.join()
    #     if word in diccionario correspondiente de pattern:
            #sumar_puntos

window.Close()
