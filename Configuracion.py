import PySimpleGUI as sg
import Menú
import Tablero

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
        [sg.Button('Confirmar'), sg.Button('Volver al menu')]
    ]

    window = sg.Window('Configuración').Layout(conf).Finalize()

    while True:
        event, values = window.Read()
        if event is None:
            break
        elif event == 'Confirmar':
            parametros = definir_parametros(values)
            window.Close()
            Tablero.main(*parametros)
        elif event == 'Volver al menu':
            window.Close()
            Menú.main()

    window.Close()

if __name__ == '__main__':
    main()
