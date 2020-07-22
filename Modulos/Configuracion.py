import PySimpleGUI as sg
import ScrabbleAR
from Modulos import Tablero
import json

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
        return [jug,tema,level,tiempo]

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
                    window2.Close()
                    break
                elif event2 == 'Confirmar':
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
                                sg.Popup('Error. No existe la carpeta "Archivos".', no_titlebar=True)
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
                                sg.Popup('Error. No existe la carpeta "Archivos".', no_titlebar=True)
                            finally:
                                break
                    window4.Close()
        #los break son para que corte el while y no dé error

if __name__ == '__main__':
    main()
