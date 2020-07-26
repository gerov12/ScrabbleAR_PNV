import PySimpleGUI as sg
from Modulos import Tablero
from Modulos import Configuracion
import json
from os.path import isfile
import sys

def main():
    sg.ChangeLookAndFeel('DarkAmber')

    def actualizar(listbox,lis):
        '''Actualiza el contenido de la listbox con lo que contenga la variable "lis"'''
        aux = []
        for elem in lis:
            texto = ""
            for key, datos in elem.items():
                texto = texto+key+": "+str(datos)+" | "
            aux.append(texto.upper())
        listbox.Update(values = aux)

    def retornar_datos (nom_archivo):
        '''Abre el archivo del top 10 del nivel correspondiente, si existe carga los datos del archivo a la
        variable "lis". Caso contrario si el archivo no existe se levanta una excepcion y se le informa al
        usuario que no hay datos mediante un Popup'''

        lis=[]
        try:
            archivo=open("Archivos/"+nom_archivo)
            lis=json.load(archivo)
            archivo.close()
        except (FileNotFoundError):
            window2.Element("N1").Update(disabled = True)
            window2.Element("N2").Update(disabled = True)
            window2.Element("N3").Update(disabled = True)
            sg.Popup('No hay datos.', no_titlebar=True)
            window2.Element("N1").Update(disabled = False)
            window2.Element("N2").Update(disabled = False)
            window2.Element("N3").Update(disabled = False)
        return lis

    # try:
    #     if not isfile("Imagenes/TituloScrabble1.png"): #si no existe la carpeta o la imagen levanto la excepción para advertir y que se cierre el programa
    #         raise(FileNotFoundError)
    # except(FileNotFoundError):
    #     sg.Popup("La carpeta 'Imagenes' o la imagen solicitada no existen.", no_titlebar=True)
    #     sys.exit()

    if not isfile("Imagenes/Titulo/TituloScrabble1.png"): #si no existe la carpeta o la imagen advierte con un Popup y cierra el programa
        sg.Popup("La carpeta 'Imagenes' o la imagen solicitada no existen.", no_titlebar=True)
        sys.exit()

    layout = [
        [sg.Image(filename = "Imagenes/Titulo/TituloScrabble1.png", size=(400,200))],
        [sg.Button('Partida Rápida', size = (30, 2), pad=(90,4))],
        [sg.Button('Cargar Partida', size = (30, 2), pad=(90,4))],
        [sg.Button('Partida Personalizada', size = (30, 2), pad=(90,4))],
        [sg.Button('Top 10 Puntajes', size = (30, 2), pad=(90,4))],
        [sg.Button('Salir', size = (20, 2), pad=(125,4))]
    ]


    window = sg.Window('ScrabbleAR', size =(450, 540)).Layout(layout).Finalize()

    while True:
        event, values = window.Read()
        if event is None or event == 'Salir':
            window.Close()
            break
        elif event == 'Partida Rápida':
            window.Close()
            Tablero.main('Jugador', 'claro','nivel1',3)
            break
        # elif event == 'Cargar Partida':
        #     ...
        #     break
        elif event == 'Partida Personalizada':
            window.Close()
            Configuracion.main()
            break
        elif event == 'Top 10 Puntajes':
            top10 = [[sg.Button('Nivel 1', key="N1"),sg.Button('Nivel 2', key="N2"),sg.Button('Nivel 3', key="N3")],
                      [sg.Listbox(values = [],key='t10', size=(65,10), font = ("",15))],
                      [sg.Button('Atras')]]

            window2 = sg.Window('TOP 10').Layout(top10).Finalize()

            while True:
                event2, values2 = window2.Read()
                if event2 == 'Atras' or event2 == None:
                    window2.Close()
                    break
                elif event2 == 'N1':
                    actualizar(window2.Element('t10'), retornar_datos('top10_nivel1.json'))
                    #break
                elif event2 == 'N2':
                    actualizar(window2.FindElement('t10'), retornar_datos('top10_nivel2.json'))
                    #break
                else:
                    actualizar(window2.FindElement('t10'), retornar_datos('top10_nivel3.json'))
                    #break
            window2.Close()
    window.Close()

        #los break son para que corte el while y no dé error

if __name__ == '__main__':
    main()
