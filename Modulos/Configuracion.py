import os
import sys
import json
import ScrabbleAR
import PySimpleGUI as sg
from Modulos import Tablero
from os.path import isdir, isfile
def main():
    def definir_parametros(values):
        '''Asigna los valores que el jugador selecciono a los parametros que se enviaran al tablero'''

        if values['nom'] != '':
            jug = values['nom']
        else:
            jug = 'Jugador'
        if values['claro'] == True:
            tema = 'claro'
        elif values['oscuro'] == True:
            tema = 'oscuro'
        else:
            tema = 'madera'
        if values['nivel1'] == True:
            level = 'nivel1'
        elif values['nivel2'] == True:
            level = 'nivel2'
        else:
            level = 'nivel3'
        tiempo = values['tiempo']
        return [False, jug, tema ,level, tiempo]

    sg.ChangeLookAndFeel('DarkAmber')

    dat = [
        [sg.Text('Nombre del jugador'),sg.Input(key='nom')],
        [sg.Text('Tema'), sg.Radio('Claro', "tema", default=True, key='claro'),sg.Radio('Oscuro', "tema", key='oscuro'),
        sg.Radio('Madera', "tema",key='madera')]
    ]

    game = [
        [sg.Text('Niveles'),sg.Radio('Nivel 1', "nivel", default=True, key='nivel1'),sg.Radio('Nivel 2', "nivel", key='nivel2'), sg.Radio('Nivel 3', "nivel", key='nivel3')],
        [sg.Text('Tiempo'), sg.Slider(range=(1,20), default_value=3, orientation='horizontal', key='tiempo'),sg.Text('Minutos')]
    ]

    conf = [
        [sg.Frame('Datos', dat, title_color='white',background_color='black')],
        [sg.Frame('Juego', game, title_color='white',background_color='black')],
        [sg.Button('Confirmar'), sg.Button('Volver al menu'), sg.Button('Modificar letras')]
    ]

    window = sg.Window('Configuración').Layout(conf).Finalize()

    ok = False #Booleano para saber si se modifico la cantidad de alguna letra
    ok2= False #Booleano para saber si se modifico el puntaje de alguna letra

    while True:
        event, values = window.Read()
        if event is None:
            window.Close()
            break


        elif event == 'Confirmar':
            parametros = definir_parametros(values)
            window.Close()
            Tablero.main(*parametros, ok, ok2)
            break


        elif event == 'Volver al menu':
            #guardo las cantidades por defecto
            aux_L = {"A": 11, "E": 11, "O": 8, "S": 7, "I": 6, "U": 6, "N": 5, "L": 4, "R": 4, "T": 4, "C": 4,
            "D": 4, "G": 2, "M": 3, "B": 3, "P": 2, "F": 2, "H": 2, "V": 2, "Y": 1, "J": 2, "K": 1, "LL": 1,
            "\u00d1": 1, "Q": 1, "RR": 1, "W": 1, "X": 1, "Z": 1}
            with open('Archivos/Letras_modificado.json','w') as file: #Guardo el diccionario en un JSON
                json.dump(aux_L,file)
                ok = True
            #guardo los puntajes por defecto
            aux_P = {"A": 1, "E": 1, "O": 1, "S": 1, "I": 1, "U": 1, "N": 1, "L": 1, "R": 1, "T": 1, "C": 2,
            "D": 2, "G": 2, "M": 3, "B": 3, "P": 3, "F": 4, "H": 4, "V": 4, "Y": 4, "J": 6, "K": 8, "LL": 8,
            "\u00d1": 8, "Q": 8, "RR": 8, "W": 8, "X": 8, "Z": 10}
            with open('Archivos/Puntajes_modificado.json','w') as file: #Guardo el diccionario en un JSON
                json.dump(aux_P,file)
                ok = True
            window.Close()
            ScrabbleAR.main()
            break


        elif event == 'Modificar letras': #Guardo las cantidades de las letras en un diccionario nuevo

            modificar =[
                        [sg.Text("")],
                        [sg.Text("")],
                        [sg.Button('Modificar La Cantidad De Letras', button_color=("white", "blue"), border_width=0),sg.VerticalSeparator(),
                        sg.Button('Modificar El Puntaje De Las Letras', button_color=("white", "red"), border_width=0)],
                        [sg.Text("")],
                        [sg.Text("")],
                        [sg.Text("                             "), sg.Button('Confirmar'),sg.Button('Cancelar')]]

            window2 = sg.Window('Modificar letras',size =(500,250)).Layout(modificar).Finalize()

            while True:
                event2, values2 = window2.Read()
                if event2 == None or event2 == 'Cancelar':
                    aux_L = {"A": 11, "E": 11, "O": 8, "S": 7, "I": 6, "U": 6, "N": 5, "L": 4, "R": 4, "T": 4, "C": 4,
                    "D": 4, "G": 2, "M": 3, "B": 3, "P": 2, "F": 2, "H": 2, "V": 2, "Y": 1, "J": 2, "K": 1, "LL": 1,
                    "\u00d1": 1, "Q": 1, "RR": 1, "W": 1, "X": 1, "Z": 1}
                    with open('Archivos/Letras_modificado.json','w') as file: #Guardo el diccionario en un JSON
                        json.dump(aux_L,file)
                        ok = True
                    aux_P = {"A": 1, "E": 1, "O": 1, "S": 1, "I": 1, "U": 1, "N": 1, "L": 1, "R": 1, "T": 1, "C": 2,
                    "D": 2, "G": 2, "M": 3, "B": 3, "P": 3, "F": 4, "H": 4, "V": 4, "Y": 4, "J": 6, "K": 8, "LL": 8,
                    "\u00d1": 8, "Q": 8, "RR": 8, "W": 8, "X": 8, "Z": 10}
                    with open('Archivos/Puntajes_modificado.json','w') as file: #Guardo el diccionario en un JSON
                        json.dump(aux_P,file)
                        ok = True
                    window2.Close()
                    break


                elif event2 == 'Confirmar':
                    sg.PopupNoButtons('La configuración fue guardada con éxito', auto_close = True, auto_close_duration = 3, no_titlebar = True)
                    window2.Close()
                    break


                elif event2 == 'Modificar La Cantidad De Letras':
                    letras = [
                        [sg.Text('A'), sg.Spin([i for i in range(1,12)], initial_value=1, key='A'),
                        sg.Text('B'), sg.Spin([i for i in range(1,12)], initial_value=1, key='B'),
                        sg.Text('C'), sg.Spin([i for i in range(1,12)], initial_value=1, key='C'),
                        sg.Text('D'), sg.Spin([i for i in range(1,12)], initial_value=1, key='D')],
                        [sg.Text('E'), sg.Spin([i for i in range(1,12)], initial_value=1, key='E'),
                        sg.Text('F'), sg.Spin([i for i in range(1,12)], initial_value=1, key='F'),
                        sg.Text('G'), sg.Spin([i for i in range(1,12)], initial_value=1, key='G'),
                        sg.Text('H'), sg.Spin([i for i in range(1,12)], initial_value=1, key='H')],
                        [sg.Text('I'), sg.Spin([i for i in range(1,12)], initial_value=1, key='I'),
                        sg.Text('J'), sg.Spin([i for i in range(1,12)], initial_value=1, key='J'),
                        sg.Text('K'), sg.Spin([i for i in range(1,12)], initial_value=1, key='K'),
                        sg.Text('L'), sg.Spin([i for i in range(1,12)], initial_value=1, key='L')],
                        [sg.Text('LL'), sg.Spin([i for i in range(1,12)], initial_value=1, key='LL'),
                        sg.Text('M'), sg.Spin([i for i in range(1,12)], initial_value=1, key='M'),
                        sg.Text('N'), sg.Spin([i for i in range(1,12)], initial_value=1, key='N'),
                        sg.Text('Ñ'), sg.Spin([i for i in range(1,12)], initial_value=1, key='Ñ')],
                        [sg.Text('O'), sg.Spin([i for i in range(1,12)], initial_value=1, key='O'),
                        sg.Text('P'), sg.Spin([i for i in range(1,12)], initial_value=1, key='P'),
                        sg.Text('Q'), sg.Spin([i for i in range(1,12)], initial_value=1, key='Q'),
                        sg.Text('R'), sg.Spin([i for i in range(1,12)], initial_value=1, key='R')],
                        [sg.Text('RR'), sg.Spin([i for i in range(1,12)], initial_value=1, key='RR'),
                        sg.Text('S'), sg.Spin([i for i in range(1,12)], initial_value=1, key='S'),
                        sg.Text('T'), sg.Spin([i for i in range(1,12)], initial_value=1, key='T'),
                        sg.Text('U'), sg.Spin([i for i in range(1,12)], initial_value=1, key='U')],
                        [sg.Text('V'), sg.Spin([i for i in range(1,12)], initial_value=1, key='V'),
                        sg.Text('W'), sg.Spin([i for i in range(1,12)], initial_value=1, key='W'),
                        sg.Text('X'), sg.Spin([i for i in range(1,12)], initial_value=1, key='X'),
                        sg.Text('Y'), sg.Spin([i for i in range(1,12)], initial_value=1, key='Y')],
                        [sg.Text('Z'), sg.Spin([i for i in range(1,12)], initial_value=1, key='Z')],
                        [sg.Text("    "),sg.Button('Confirmar', key='confirmar'), sg.Button('Cancelar')]
                        ]
                    window3 = sg.Window('Cantidad De Letras').Layout(letras).Finalize()

                    try:
                        with open('Archivos/Letras_modificado.json','r') as archivo_cantidades: #cargo el json con los valores por defecto
                            cantidadMOD = json.load(archivo_cantidades)
                        for L, C in cantidadMOD.items():
                            window3.Element(L).Update(value = C)
                    except:
                        if not isdir("Archivos"): #si no existe la carpeta archivos, informo y doy la opcion de crearla
                            respuesta = sg.PopupYesNo('ERROR. La carpeta "Archivos" no existe. ¿Desea crearla?',no_titlebar=True)
                            if respuesta == "Yes":
                                os.mkdir('Archivos')
                            else:
                                sys.exit()
                        if not isfile("Archivos/Letras_modificado.json"): #si no existe el json
                            respuesta = sg.PopupYesNo('ERROR. El archivo JSON "Letras_modificado.json" no existe. ¿Desea crear el archivo (con los valores por defecto)?',no_titlebar=True) #pregunto si quiere crear el json faltante
                            if respuesta == "Yes":
                                auxDic = {"A": 11, "E":11, "O":8, "S":7, "I":6, "U":6, "N":5, "L":4, "R":4, "T":4, "C":4, "D":4,
                                    "G":2, "M":3, "B":3, "P":2, "F":2, "H":2, "V":2, "Y":1, "J":2, "K":1, "LL":1, "Ñ":1, "Q":1, "RR":1,
                                     "W":1, "X":1, "Z":1}
                                with open('Archivos/Letras_modificado.json','w') as file: #Guardo el diccionario vacio en un JSON
                                    json.dump(auxDic,file)
                                with open('Archivos/Letras_modificado.json','r') as archivo_cantidades: #cargo el json con los valores por defecto
                                    cantidadMOD = json.load(archivo_cantidades)
                                for L, C in cantidadMOD.items():
                                    window3.Element(L).Update(value = C)

                            else:
                                sys.exit()
                    while True:
                        event3, values3 = window3.Read()
                        if event3 == None or event3 == 'Cancelar':
                            break


                        elif event3 == 'confirmar':
                            dic = {}
                            for key,valor in values3.items():  #Transformo los valores en integer
                                dic[key] = int(valor)
                            try:
                                with open('Archivos/Letras_modificado.json','w') as file: #Guardo el diccionario en un JSON
                                    json.dump(dic,file)
                                    ok = True
                            except(FileNotFoundError):
                                if not isdir("Archivos"): #si no existe la carpeta archivos, informo y doy la opcion de crearla
                                    respuesta = sg.PopupYesNo('ERROR. La carpeta "Archivos" no existe. ¿Desea crearla?',no_titlebar=True)
                                    if respuesta == "Yes":
                                        os.mkdir('Archivos')
                                    else:
                                        sys.exit()
                                if not isfile("Archivos/Letras_modificado.json"): #si no existe el json
                                    respuesta = sg.PopupYesNo('ERROR. El archivo JSON "Letras_modificado.json" no existe. ¿Desea crear el archivo (con los valores por defecto)?',no_titlebar=True) #pregunto si quiere crear el json faltante
                                    if respuesta == "Yes":
                                        auxDic = {"A": 11, "E":11, "O":8, "S":7, "I":6, "U":6, "N":5, "L":4, "R":4, "T":4, "C":4, "D":4,
                                         "G":2, "M":3, "B":3, "P":2, "F":2, "H":2, "V":2, "Y":1, "J":2, "K":1, "LL":1, "Ñ":1, "Q":1, "RR":1,
                                          "W":1, "X":1, "Z":1}
                                        with open('Archivos/Letras_modificado.json','w') as file: #Guardo el diccionario vacio en un JSON
                                            json.dump(auxDic,file)
                                        ok = False

                                    else:
                                        sys.exit()
                            finally:
                                break

                    window3.Close()



                elif event2 == 'Modificar El Puntaje De Las Letras':
                    letras2 = [
                        [sg.Text('A'), sg.Spin([i for i in range(1,21)], initial_value=1, key='A'),
                        sg.Text('B'), sg.Spin([i for i in range(1,21)], initial_value=1, key='B'),
                        sg.Text('C'), sg.Spin([i for i in range(1,21)], initial_value=1, key='C'),
                        sg.Text('D'), sg.Spin([i for i in range(1,21)], initial_value=1, key='D')],
                        [sg.Text('E'), sg.Spin([i for i in range(1,21)], initial_value=1, key='E'),
                        sg.Text('F'), sg.Spin([i for i in range(1,21)], initial_value=1, key='F'),
                        sg.Text('G'), sg.Spin([i for i in range(1,21)], initial_value=1, key='G'),
                        sg.Text('H'), sg.Spin([i for i in range(1,21)], initial_value=1, key='H')],
                        [sg.Text('I'), sg.Spin([i for i in range(1,21)], initial_value=1, key='I'),
                        sg.Text('J'), sg.Spin([i for i in range(1,21)], initial_value=1, key='J'),
                        sg.Text('K'), sg.Spin([i for i in range(1,21)], initial_value=1, key='K'),
                        sg.Text('L'), sg.Spin([i for i in range(1,21)], initial_value=1, key='L')],
                        [sg.Text('LL'), sg.Spin([i for i in range(1,21)], initial_value=1, key='LL'),
                        sg.Text('M'), sg.Spin([i for i in range(1,21)], initial_value=1, key='M'),
                        sg.Text('N'), sg.Spin([i for i in range(1,21)], initial_value=1, key='N'),
                        sg.Text('Ñ'), sg.Spin([i for i in range(1,21)], initial_value=1, key='Ñ')],
                        [sg.Text('O'), sg.Spin([i for i in range(1,21)], initial_value=1, key='O'),
                        sg.Text('P'), sg.Spin([i for i in range(1,21)], initial_value=1, key='P'),
                        sg.Text('Q'), sg.Spin([i for i in range(1,21)], initial_value=1, key='Q'),
                        sg.Text('R'), sg.Spin([i for i in range(1,21)], initial_value=1, key='R')],
                        [sg.Text('RR'), sg.Spin([i for i in range(1,21)], initial_value=1, key='RR'),
                        sg.Text('S'), sg.Spin([i for i in range(1,21)], initial_value=1, key='S'),
                        sg.Text('T'), sg.Spin([i for i in range(1,21)], initial_value=1, key='T'),
                        sg.Text('U'), sg.Spin([i for i in range(1,21)], initial_value=1, key='U')],
                        [sg.Text('V'), sg.Spin([i for i in range(1,21)], initial_value=1, key='V'),
                        sg.Text('W'), sg.Spin([i for i in range(1,21)], initial_value=1, key='W'),
                        sg.Text('X'), sg.Spin([i for i in range(1,21)], initial_value=1, key='X'),
                        sg.Text('Y'), sg.Spin([i for i in range(1,21)], initial_value=1, key='Y')],
                        [sg.Text('Z'), sg.Spin([i for i in range(1,21)], initial_value=1, key='Z')],
                        [sg.Text("    "),sg.Button('Confirmar', key='confirmar'), sg.Button('Cancelar')]
                        ]
                    window4 = sg.Window('Puntaje De Letras').Layout(letras2).Finalize()

                    try:
                        with open('Archivos/Puntajes_modificado.json','r') as archivo_puntajes: #cargo el json con los valores por defecto
                            puntajesMOD = json.load(archivo_puntajes)
                        for L, C in puntajesMOD.items():
                            window4.Element(L).Update(value = C)
                    except:
                        if not isdir("Archivos"): #si no existe la carpeta archivos, informo y doy la opcion de crearla
                            respuesta = sg.PopupYesNo('ERROR. La carpeta "Archivos" no existe. ¿Desea crearla?',no_titlebar=True)
                            if respuesta == "Yes":
                                os.mkdir('Archivos')
                            else:
                                sys.exit()
                        if not isfile("Archivos/Puntajes_modificado.json"): #si no existe el json
                            respuesta = sg.PopupYesNo('ERROR. El archivo JSON "Puntajes_modificado.json" no existe. ¿Desea crear el archivo (con los valores por defecto)?',no_titlebar=True) #pregunto si quiere crear el json faltante
                            if respuesta == "Yes":
                                auxDic = {"A": 1, "E": 1, "O": 1, "S": 1, "I": 1, "U": 1, "N": 1, "L": 1, "R": 1, "T": 1, "C": 2, "D": 2,
                                 "G": 2, "M": 3, "B": 3, "P": 3, "F": 4, "H": 4, "V": 4, "Y": 4, "J": 6, "K": 8, "LL": 8, "\u00d1": 8,
                                 "Q": 8, "RR": 8, "W": 8, "X": 8, "Z": 10}
                                with open('Archivos/Puntajes_modificado.json','w') as file: #Guardo el diccionario vacio en un JSON
                                    json.dump(auxDic,file)
                                with open('Archivos/Puntajes_modificado.json','r') as archivo_puntajes: #cargo el json con los valores por defecto
                                    puntajesMOD = json.load(archivo_puntajes)
                                for L, C in puntajesMOD.items():
                                    window4.Element(L).Update(value = C)
                            else:
                                sys.exit()
                    while True:
                        event4, values4 = window4.Read()
                        if event4 == None or event4 == 'Cancelar':
                            break


                        elif event4 == 'confirmar':
                            dic = {}
                            for key,valor in values4.items():  #Transformo los valores en integer
                                dic[key] = int(valor)
                            try:
                                with open('Archivos/Puntajes_modificado.json','w') as file: #Guardo el diccionario en un JSON
                                    json.dump(dic,file)
                                    ok2 = True
                            except(FileNotFoundError):
                                if not isdir("Archivos"): #si no existe la carpeta archivos, informo y doy la opcion de crearla
                                    respuesta = sg.PopupYesNo('ERROR. La carpeta "Archivos" no existe. ¿Desea crearla?',no_titlebar=True)
                                    if respuesta == "Yes":
                                        os.mkdir('Archivos')
                                    else:
                                        sys.exit()
                                if not isfile("Archivos/Puntajes_modificado.json"): #si no existe el json
                                    respuesta = sg.PopupYesNo('ERROR. El archivo JSON "Puntajes_modificado.json" no existe. ¿Desea crear el archivo (con los valores por defecto)?',no_titlebar=True) #pregunto si quiere crear el json faltante
                                    if respuesta == "Yes":
                                        auxDic = {"A": 1, "E": 1, "O": 1, "S": 1, "I": 1, "U": 1, "N": 1, "L": 1, "R": 1, "T": 1, "C": 2,
                                        "D": 2, "G": 2, "M": 3, "B": 3, "P": 3, "F": 4, "H": 4, "V": 4, "Y": 4, "J": 6, "K": 8, "LL": 8,
                                        "\u00d1": 8, "Q": 8, "RR": 8, "W": 8, "X": 8, "Z": 10}
                                        with open('Archivos/Puntajes_modificado.json','w') as file: #Guardo el diccionario vacio en un JSON
                                            json.dump(auxDic,file)
                                        ok = False
                            finally:
                                break

                    window4.Close()
        #los break son para que corte el while y no dé error

if __name__ == '__main__':
    main()
