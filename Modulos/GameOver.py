import json
import ScrabbleAR
import PySimpleGUI as sg
from Modulos import Tablero

def main (puntos_jugador,puntos_computadora,nombre, tema, nivel, tiempo, modificado, modificado2, cargado):
    '''Define quien gano o si hubo un empate y lo muestra con la imagen correspondiente
    Si la imagen o la carpeta que las contiene no existe levanta una excepcion y lo informa con un Popup'''

    sg.ChangeLookAndFeel('DarkAmber')
    try:
        if cargado: #si terminé una partida pospuesta, esta se elimina
            aux = {}
            with open ("Archivos/Partida.json", "w") as archivo:
                json.dump(aux, archivo)
    except (FileNotFoundError):
        sg.Popup('ERROR. El archivo JSON solicitado o su carpeta contenedora no existen.',no_titlebar=True)
        sys.exit()

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
            print('Resultado Final             ---> Ganó El Jugador')#


        elif puntos_computadora > puntos_jugador:
            fin = [
                [sg.Image(filename = "Imagenes/Fin/Perdedor.png", size=(630,630))], [sg.Button('Volver a Jugar'),sg.Button('Menú'),sg.Button('Salir', button_color=('black','red'))],
                [sg.Text('', size=(1,1))]
                ]
            print('Resultado Final             ---> Ganó La Computadora')#

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
                break


            elif event == 'Menú':
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


            elif event == 'Volver a Jugar':
                window.Close()
                Tablero.main(False, nombre, tema, nivel, tiempo, modificado, modificado2)
                break

        window.Close()

    except(FileNotFoundError):
        sg.Popup('Error. No existe la carpeta "Imagenes" o la imagen solicitada.', no_titlebar=True)

if __name__ =='__main__':
    main(0,0,"jugador", "Claro", "nivel1", 3.0, False, False)
