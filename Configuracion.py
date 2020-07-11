import PySimpleGUI as sg
import ScrabbleAR
import Tablero
import json

def main():
    def definir_parametros(values):
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

    ok = False #Booleano para saber si se modifico alguna letra

    while True:
        event, values = window.Read()
        if event is None:
            window.Close()
            break
        elif event == 'Confirmar':
            parametros = definir_parametros(values)
            window.Close()
            Tablero.main(*parametros, ok)
            break
        elif event == 'Volver al menu':
            window.Close()
            Menú.main()
            break
        elif event == 'Modificar letras': #Guardo las cantidades de las letras en un diccionario nuevo
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
                [sg.Text('Z'), sg.Spin([i for i in range(1,12)], initial_value=1, key='Z'),
                sg.Button('Confirmar', key='confirmar'), sg.Button('Cancelar')]
                ]
            window2 = sg.Window('Modificar letras').Layout(letras).Finalize()

            while True:
                evento, valores = window2.Read()
                if evento == None or evento == 'Cancelar':
                    break
                elif evento == 'confirmar':
                    dic = {}
                    for key,valor in valores.items():  #Transformo los valores en integer
                        dic[key] = int(valor)
                    try:
                        with open('Archivos/Letras_modificado.json','w') as file: #Guardo el diccionario en un JSON
                            json.dump(dic,file)
                            ok = True
                    except(FileNotFoundError):
                        sg.Popup('Error. No existe la carpeta "Archivos"')
                    finally:
                        break
            window2.Close()


        #los break son para que corte el while y no dé error

if __name__ == '__main__':
    main()
