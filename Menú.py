import PySimpleGUI as sg
import Tablero
import Configuracion

def main():
    sg.ChangeLookAndFeel('DarkAmber')

    layout = [
        [sg.Image(filename = "Imagenes/TituloScrabble1.png", size=(400,200))],
        [sg.Button('Partida Rápida', size = (30, 2), pad=(90,4))],
        [sg.Button('Cargar Partida', size = (30, 2), pad=(90,4))],
        [sg.Button('Partida Personalizada', size = (30, 2), pad=(90,4))],
        [sg.Button('Salir', size = (20, 2), pad=(125,4))]
    ]

    window = sg.Window('ScrabbleAR', size =(450, 500)).Layout(layout).Finalize()

    while True:
        event, values = window.Read()
        if event is None or event == 'Salir':
            break
        elif event == 'Partida Rápida':
            window.Close()
            Tablero.main('Jugador', 'claro','nivel1',3)
        # elif event == 'Cargar Partida':
        #     ...
        #     break
        elif event == 'Partida Personalizada':
            window.Close()
            Configuracion.main()

    window.Close()

if __name__ == '__main__':
    main()
