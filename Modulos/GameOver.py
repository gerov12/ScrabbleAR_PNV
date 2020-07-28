import ScrabbleAR
import PySimpleGUI as sg
from Modulos import Tablero

def main (puntos_jugador,puntos_computadora,nombre, tema, nivel, tiempo, modificado, modificado2):
    '''Define quien gano'''

    sg.ChangeLookAndFeel('DarkAmber')

    try:
        print('###############################')#
        print('Fin del juego')#
        print()#
        print('Puntos del jugador          ---> ' + str(puntos_jugador))#
        print('Puntos de la computadora    ---> ' + str(puntos_computadora))#

        if puntos_jugador > puntos_computadora:
            fin = [
                [sg.Image(filename = "Imagenes/Fin/Ganador.png", size=(630,630))], [sg.Button('Volver a Jugar'),sg.Button('Menú'), sg.Button('Salir', button_color=('black','red'))],
                [sg.Text('', size=(1,1))]
                ]
            print('Resultado Final             ---> Gano El Jugador')#


        elif puntos_computadora > puntos_jugador:
            fin = [
                [sg.Image(filename = "Imagenes/Fin/Perdedor.png", size=(630,630))], [sg.Button('Volver a Jugar'),sg.Button('Menú'),sg.Button('Salir', button_color=('black','red'))],
                [sg.Text('', size=(1,1))]
                ]
            print('Resultado Final             ---> Gano La Computadora')#

        else:
            fin = [
                [sg.Image(filename = "Imagenes/Fin/Empate.png", size=(630,630))], [sg.Button('Volver a Jugar'),sg.Button('Menú'), sg.Button('Salir', button_color=('black','red'))],
                [sg.Text('', size=(1,1))]
                ]
            print('Resultado Final             ---> Hubo Un Empate')#

        window = sg.Window('Game Over',no_titlebar=True).Layout(fin).Finalize()

        while True:
            event, values = window.Read()
            if event == 'Salir':
                break


            elif event == 'Menú':
                window.Close()
                ScrabbleAR.main()
                break


            elif event == 'Volver a Jugar':
                window.Close()
                Tablero.main(nombre, tema, nivel, tiempo, modificado, modificado2)
                break

        window.Close()

    except(FileNotFoundError):
        sg.Popup('Error. No existe la carpeta "Imagenes" o la imagen solicitada.', no_titlebar=True)

if __name__ =='__main__':
    main(puntos_jugador,puntos_computadora)
