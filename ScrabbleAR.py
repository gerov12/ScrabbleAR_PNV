import PySimpleGUI as sg
import Tablero
import Configuracion
import json

def main():
    sg.ChangeLookAndFeel('DarkAmber')

    def actualizar(listbox,lis):
        '''Actualiza el contenido de la listbox con lo que contenga la variable "lis" '''

        listbox.Update(map(lambda x: "{}".format(x),lis))

    def retornar_datos (nom_archivo):
        '''Abre el archivo del top 10 del nivel correspondiente, si existe carga los datos del archivo a la
        variable "lis". Caso contrario si el archivo no existe se levanta una excepcion y se le informa al
        usuario que no hay datos mediante un Popup '''

        lis=[]
        try:
            archivo=open(nom_archivo)
            lis=json.load(archivo)
            archivo.close()
        except (FileNotFoundError):
            sg.Popup('No hay datos')
        return lis

    layout = [
        [sg.Image(filename = "Imagenes/TituloScrabble1.png", size=(400,200))],
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
            top10 = [[sg.Button('Nivel 1'),sg.Button('Nivel 2'),sg.Button('Nivel 3')],
                      [sg.Listbox(values = [],key='t10', size=(70,20))],
                      [sg.Button('Atras'),sg.Button('Cerrar')]]

            window2 = sg.Window('puntajes').Layout(top10).Finalize()

            while True:
                event2, values2 = window2.Read()
                if event2 == 'Cerrar' or event2 == None:
                    window2.Close()
                    break
                elif event2 == 'Atras':
                    window2.Close()
                    break
                elif event2 == 'Nivel 1':
                    actualizar(window2.Element('t10'), retornar_datos('top10_nivel1.json'))
                    #break
                elif event2 == 'Nivel 2':
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
