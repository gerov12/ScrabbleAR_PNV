import PySimpleGUI as sg
import json
import random
import pattern.es
import Menú

def main(nombre = 'Jugador', tema ='Claro', nivel = 'nivel1', tiempo = 3.0):
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

    def cargar_casillas(): #carga las keys de las casillas del tablero
        with open('Casillas.json','r') as archivo_casillas:
            cas = json.load(archivo_casillas)
        return cas

    def cargar_casillas_especiales(nivel = 'nivel1'):
        with open ('Especiales.json','r') as archivo_casillas: #falta escribir el archivo Especiales.json
            casillas_esp=json.load(archivo_casillas)
        return casillas_esp#[nivel] #devuelve el dic del nivel correspondiente

    def cargar_tablero(casillas_esp): #crea el layout del tablero
        board = []
        for y in range(14,-1,-1): #de 14 a 0 ya que las filas en el layout van en ese orden
            fila = []
            for x in range(15):
                auxKey = ''
                if x<10:
                    auxKey = '0'+str(x) #si el valor de la coordenada x es de un solo digito le agrego un 0 adelante
                else:
                    auxKey = str(x)
                if y<10:
                    auxKey = auxKey+'0'+str(y) #si el valor de la coordenada y es de un solo digito le agrego un 0 adelante
                else:
                    auxKey = auxKey+str(y)
                if auxKey in casillas_esp:
                    color = casillas_esp[auxKey][1] #si es una casilla especial le coloco el color correspondiente
                else:
                    color = 'white'
                fila.append(sg.Button('', size = (2,2),button_color = ('black',color), pad = (0,0), key = auxKey))
            board.append(fila)
        return board

    def activar():
        window.Element('CAMBIO').Update(disabled = True)
        window.Element('TODAS').Update(disabled = False)    #activo las opciones
        window.Element('ALGUNAS').Update(disabled = False)
        window.Element('CANCEL').Update(disabled = False)
        for i in atril:
            window.Element(i).Update(disabled = True) #desactivo los clicks en el atril

    def desactivar():
        window.Element('CAMBIO').Update(disabled = False)
        window.Element('TODAS').Update(disabled = True)    #activo las opciones
        window.Element('ALGUNAS').Update(disabled = True)
        window.Element('CANCEL').Update(disabled = True)
        for i in atril:
            window.Element(i).Update(disabled = False) #activo los clicks en el atril

    def mezclar(datos, bolsa): #cambia las letras en 'datos' por letras al azar de la bolsa
        for i in datos:
            pos = random.randrange(len(bolsa))
            window.FindElement(i).Update(text=bolsa[pos])
            del bolsa[pos]

    def colocar_letra(casilla, posA, let, pal, fichas_desocupadas, casillas_ocupadas): #pone la letra en la casilla correspondiente y la saca del atril
        window.Element(casilla).Update(text=let) #pongo la letra "let" como texto de la "casilla" clickeada
        window.Element(posA).Update(text='') #la elimino del atril (reemplazandola por '')
        palabra.append(let) #guardo la letra en la lista de letras para luego verificar si es una palabra
        fichas_desocupadas.append(posA) #guardo la pos del atril desocupada para luego devolver o colocar letras
        casillas_ocupadas.append(casilla) #guardo la key de la casilla ocupada en la lista

    def consecutivo(casilla): #indica si la casilla seleccionada es consecutivo a la letra anteriormente colocada
        aux = False
        orient = ''
        izquierda = str((int(casilla[0:2])-1))+casilla[2:4] #(el primer digito-1)+el segundo digito (es decir la casilla de la izquierda)
        arriba = casilla[0:2]+str((int(casilla[2:4])+1)) #el primer digito+(el segundo digito+1) (es decir la casilla de arriba)
        if izquierda[0]!='-': #si el primer digito de "izquierda" no es '-' (es decir que no elegí una casilla de la columna 0)
            if len(izquierda)<4: #si el valor de x queda de un solo digito
                izquierda = '0'+izquierda #le agrego un 0 adelante para que respete el formato de las keys de las casillas
            if window.Element(izquierda).GetText() != '': #si el elemento de la izquierda no está vacío
                aux = True #elegí una casilla consecutiva a la primer letra
                orient = 'Horizontal' #y comencé a armar la palabra de manera horizontal
                return [aux, orient]
        if int(arriba[2:4])<15: #si no elegí una casilla correcta para la orientacion horizontal chequeo si es vertical
        #si el sgundo digito de la casilla de arriba es menor a 4 (es decir que no elegí una casilla de la fila 3)
        #(el 4 mas adelante debería cambiarse por la altura del tablero)
            if len(arriba)<4: #si el valor de y queda de n digito
                arriba = arriba[0:2]+'0'+arriba[2] #le agrego un 0 adelante
            if window.Element(arriba).GetText() != '': #si el elemento de arriba no está vacío
                aux = True #elegí una casilla consecutiva a la primer letra
                orient = 'Vertical' #y comencé a armar la palabra de manera vertical
                return [aux, orient]
        return [aux, orient] #devuelve Flase y ''

    def orientada(casilla, orient): #indica si seleccione una casilla correcta según la orientacion definida
        aux = False
        if orient == 'Horizontal': #si la orientacion es horizontal hago el chequeo correspondiente
            izquierda = str((int(casilla[0:2])-1))+casilla[2:4]
            if izquierda[0]!='-':
                if len(izquierda)<4: #si el valor de x queda de un solo digito
                    izquierda = '0'+izquierda #le agrego un 0 adelante para que respete el formato de las keys de las casillas
                if window.Element(izquierda).GetText() != '':
                    aux = True
        elif orient == 'Vertical': #si la orientacion es vertical hago el chequeo correspondiente
            arriba = casilla[0:2]+str((int(casilla[2:4])+1))
            if int(arriba[2:4])<15:
                if len(arriba)<4: #si el valor de y queda de n digito
                    arriba = arriba[0:2]+'0'+arriba[2] #le agrego un 0 adelante
                if window.Element(arriba).GetText() != '':
                    aux = True
        return aux

    def chequear_casilla(letra, palabra, event, posAtril, orientacion):
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

    def es_palabra(pal, nivel = 'nivel1'): #determina si el conjunto de letras ingresado es una palabra
        aux = False
        if not pal.lower() in pattern.es.verbs:
            if pal.lower() in pattern.es.lexicon:
                print(pal + " en lexicon")
                aux = True
                if pal.lower() in pattern.es.spelling:
                    print(pal + " en spelling")
                    aux = True
        else:
            print(pal + " en verbs")
            aux = True
        if nivel == 'nivel1':
            return aux
        # elif nivel == 'nivel2':
        #     si es verbo y aux true
        #     retorna true
        # elif nivel =='nivel3':
        #     ...

    def devolver(fichas_desocupadas, casillas_ocupadas): #devuelve las letras al atril en caso de que una palabra sea incorrecta
        for i in range(len(fichas_desocupadas)):
            pos = random.randrange(len(casillas_ocupadas)) #elijo una casilla ocupada al azar
            letter = window.FindElement(casillas_ocupadas[pos]).GetText() #guardo la letra de la pos
            window.FindElement(casillas_ocupadas[pos]).Update(text = '') #elimino la letra de la pos
            window.FindElement(fichas_desocupadas[i]).Update(text=letter)  #coloco la letra en la casilla
            del casillas_ocupadas[pos] #quito la casilla que acabo de "limpiar" de la lista de casillas ocupadas

    def sumar_puntos (puntajes,casillas_esp,palabra,casilla,actual): #suma al total los puntos de la palabra ingresada
        print('entra a la funcion') #
        total=0
        valor=0 #valor por el que hay que multiplicar la palabra
        ok=False #si hay casilla multiplicadora de palabra
        for i in range(len(palabra)):
            print('-'+palabra[i]+'-')
            if casilla[i] in casillas_esp and casilla[i] != '0707': #si es una casilla especial entro
                print('es especial') #
                print('función de la casilla: '+casillas_esp[casilla[i]][0])
                if casillas_esp[casilla[i]][0] == 'Px2' or casillas_esp[casilla[i]][0] == 'Px3':
                    print('suma '+str(total)+'+'+str(puntajes[palabra[i]])) #
                    total += puntajes[palabra[i]] #le suma al total el puntaje correspondiente a la letra
                    print('sumó = '+str(total)) #
                    if casillas_esp[casilla[i]][0] == 'Px2':
                        print('duplica palabra') #
                        valor = valor+2
                    else:
                        print('triplica palabra') #
                        valor = valor+3
                    ok = True
                elif casillas_esp[casilla[i]][0] == 'Lx2' or casillas_esp[casilla[i]][0] == 'Lx3':
                    if casillas_esp[casilla[i]][0] == 'Lx2':
                        print('suma '+str(total)+'+'+str(puntajes[palabra[i]])+' duplicado') #
                        total += puntajes[palabra[i]]*2
                        print('sumó = '+str(total)) #
                    else:
                        print('suma '+str(total)+'+'+str(puntajes[palabra[i]])+' triplicado') #
                        total += puntajes[palabra[i]]*3
                        print('sumó = '+str(total)) #
            else: #si no es una casilla especial, suma normal
                print('no es especial') #
                print('suma '+str(total)+'+'+str(puntajes[palabra[i]])) #
                total += puntajes[palabra[i]]
                print('sumó = '+str(total)) #
            print('------------------------------')
        if ok: #si hay que multiplicar la palabra entera
            print('multiplicó '+str(total)+'*'+str(valor)) #
            total = total*valor
        print('suma final: '+str(total)) #
        actual += total #al puntaje actual le agrego el obtenido con la nueva palabra
        return actual


    sg.ChangeLookAndFeel('DarkAmber')

    bolsa = llenar_bolsa(nivel) #el argumento 3 del programa tiene el nivel elegido
    puntajes = cargar_puntajes()
    casillasESP = cargar_casillas_especiales() #se le enviaria el nivel por parametro pero falta terminar el json

    #keys de las casillas y las posiciones del atril (se usa para saber dónde clickea el jugador)
    casillas = cargar_casillas()
    atril = ['J1','J2','J3','J4','J5','J6','J7']

    #layout del tablero
    tablero = cargar_tablero(casillasESP) #las casillas especiales se mandarían como parametro para configurar el color de c/u

    #texto con el puntaje de la PC (layout para el frame)
    puntCOM = [
        [sg.Text(0, size=(45,1), text_color= 'white', background_color= 'grey',key='PC')]
    ]

    #texto con el puntaje del jugador (layout para el frame)
    puntJUG = [
        [sg.Text(0, size=(45,1), text_color= 'white', background_color= 'grey', key='PJ')]
    ]

    #marco con el atril de la PC
    frameAtrilCOM = [
        [sg.Button('',visible=False,key='C1'),sg.Button('',visible=False,key='C2'),sg.Button('',visible=False,key='C3'),sg.Button('',visible=False,key='C4'),sg.Button('',visible=False,key='C5'),sg.Button('',visible=False,key='C6'),
        sg.Button('',visible=False,key='C7'),sg.Button('',size=(2,2), button_color = ('black','white')),sg.Button('',size=(2,2), button_color = ('black','white')),sg.Button('',size=(2,2), button_color = ('black','white')),
        sg.Button('',size=(2,2), button_color = ('black','white')),sg.Button('',size=(2,2), button_color = ('black','white')),sg.Button('',size=(2,2), button_color = ('black','white')),
        sg.Button('',size=(2,2), button_color = ('black','white'))],
        #los botones invisibles (visible=false) guardan las letras del atril de la maquina]
        #y los 7 botones vacios del final son de fachada
    ]

    #marco con el atril del jugador
    frameAtrilJUG = [
        [sg.Button('',size=(2,2), button_color = ('black','white'), key='J1'),sg.Button('',size=(2,2), button_color = ('black','white'),key='J2'),sg.Button('',size=(2,2), button_color = ('black','white'),key='J3'),
        sg.Button('',size=(2,2), button_color = ('black','white'),key='J4'),sg.Button('',size=(2,2), button_color = ('black','white'),key='J5'),sg.Button('',size=(2,2), button_color = ('black','white'),key='J6'),
        sg.Button('',size=(2,2), button_color = ('black','white'),key='J7')],
        #atril del jugador
    ]

    #elementos de la derecha de la ventana
    colExtras = [
            [sg.Frame('',frameAtrilCOM,border_width=8)], #atril de la PC
            [sg.Frame('PUNTAJE COMPUADORA', puntCOM, title_color='white',background_color='black', key= 'LC')], #puntaje de la PC
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Button('Pausa', size=(20,1), button_color = ('black','white')),sg.Button('Reglas', size=(20,1), button_color = ('black','white'))],
            [sg.Button('Confirmar Palabra', size=(45,1), button_color = ('black','white'))],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Button('Cambiar Letras', disabled = False, button_color = ('black','white'), key = 'CAMBIO'),
            sg.Button('Todas', disabled = True, button_color = ('black','white'), key = 'TODAS'),
            sg.Button('Algunas', disabled = True, button_color = ('black','white'), key = 'ALGUNAS'),
            sg.Button('Cancelar', disabled = True, button_color = ('black','white'), key = 'CANCEL')],
            [sg.Frame('PUNTAJE '+nombre.upper(), puntJUG, title_color='white',background_color='black', key= 'LJ')], #puntaje del jugador
            [sg.Frame('',frameAtrilJUG,border_width=8)], #atril del jugador
            [sg.Button('Cambiar', button_color = ('black','white'), visible = False, key = 'OK'), sg.Button('Cancelar', button_color = ('black','white'), visible = False, key = 'CancelAlgunas')]
    ]

    #marco con el tablero
    frameTablero =[
        [sg.Frame('',tablero,border_width=8)]
    ]

    #layout del juego
    juego = [
        [sg.Column(frameTablero),sg.VerticalSeparator(), sg.Column(colExtras)] #tablero a la izquierda y elementos a la derecha
    ]

    window = sg.Window('Tablero de nivel '+nivel[-1]).Layout(juego).Finalize()
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
    palabra = [] #lista de letras colocadas en el turno
    casillas_ocupadas = [] #lista de casillas ocupadas en el turno
    fichas_desocupadas = [] #lista de lugares del atril desocupados
    orientacion = ''
    inicial = True #indica si se tiene que colocar la primer ficha de la partida
    totalJUG = 0 #puntos del jugador
    totalCOM = 0 #puntos de la PC
    cambioActivado = False #si se están cambiando letras
    a_cambiar = [] #lista de pos de atril a cambiar con mezclar()

    while True:
        event, values = window.Read()
        if event is None:
            break
        elif event == 'CAMBIO' and len(palabra) == 0: #solo puedo cambiar letras si no coloqué ninguna en el tablero
            activar() #hago utilizables los botones de cambio
        elif event == 'TODAS': #cambia todas las letras del atril
            mezclar(atril, bolsa)
            desactivar() #hago invisibles los botones de cambio
        elif event == 'ALGUNAS': #cambia letras especificas del atril (elif auxiliares abajo)
            window.Element('OK').Update(visible = True) #hago visibles los botones para cambiar algunas letras
            window.Element('CancelAlgunas').Update(visible = True)
            window.Element('TODAS').Update(disabled = True) #desactivo el boton TODAS
            window.Element('CANCEL').Update(disabled = True) #desactivo cancel general
            cambioActivado = True #activo cambio activado
            for i in atril:
                window.Element(i).Update(disabled = False) #activo los clicks en el atril
            window.Element('ALGUNAS').Update(disabled = True) #desactivo el botón que acabo de apretar
        elif event == 'OK': #cambia las letras seleccionadas
            if len(a_cambiar)>0: #si seleccioné letras
                mezclar(a_cambiar, bolsa)
                for i in a_cambiar:
                    window.Element(i).Update(button_color = ('black','white')) #vuelve a poner en blanco a todas las letras del atril
                a_cambiar = []
                desactivar() #hago utilizables los botones de cambio
                cambioActivado = False #desactivo el cambio para que el atril vuelva a funcionar con normalidad
                window.Element('CancelAlgunas').Update(visible = False)
                window.Element('OK').Update(visible = False) #hago invisibles los botones para cambiar algunas letras
        elif event == 'CancelAlgunas': #cancelo el cambio de algunas letras
            window.Element('OK').Update(visible = False) #hago invisibles los botones para cambiar algunas letras
            window.Element('CancelAlgunas').Update(visible = False)
            window.Element('CANCEL').Update(disabled = False) #activo cancel general
            window.Element('TODAS').Update(disabled = False) #activo el boton TODAS
            cambioActivado = False #desactivo cambio activado
            for i in a_cambiar:
                window.Element(i).Update(button_color = ('black','white')) #vuelve a poner en blanco a todas las letras del atril
            a_cambiar = [] #vacío la lista de fichas a cambiar
            for i in atril:
                window.Element(i).Update(disabled = True) #desactivo los clicks en el atril
            window.Element('ALGUNAS').Update(disabled = False) #activo el botón que acabo de apretar
        elif event == 'CANCEL': #cancelo el cambio de letras y vuelvo a la funcionalidad normal del atril
            desactivar()
        elif event in atril: #si hago click en una letra del atril
            print('entro a atril. cambioActivado: '+str(cambioActivado))
            if cambioActivado:
                if event in a_cambiar:
                    a_cambiar.remove(event)
                    window.Element(event).Update(button_color = ('black','white'))
                else:
                    a_cambiar.append(event)
                    window.Element(event).Update(button_color = ('black','grey'))
                print(a_cambiar)
            else:
                posAtril = event #guarda la posicion en el atril de la letra clickeada
                letra = window.Element(posAtril).GetText() #guarda la letra clickeada
        elif event in casillas:#si hago click en una casilla del tablero
            if inicial: #si es la ficha inicial
                if event == '0707': #si selecciono el casillero inicial
                    if letra != '': #si previamente clickee una letra del atril
                        if len(palabra) == 0: #si es la primer letra de la palabra
                            colocar_letra(event, posAtril, letra, palabra, fichas_desocupadas, casillas_ocupadas) #coloco la letra en la casilla
                            posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
                            letra = '' #idem pero con la letra
                        elif len(palabra) == 1: #si es la segunda letra de la palabra
                            resultado = consecutivo(event)
                            if resultado[0]: #si la casilla (event) seleccionada es consecutivo a la letra anteriormente colocada
                                orientacion = resultado[1] #guardo la orientacion
                                colocar_letra(event, posAtril, letra, palabra, fichas_desocupadas, casillas_ocupadas) #coloco la letra en la casilla
                                posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
                                letra = '' #idem pero con la letra
                                print(orientacion)
                        elif len(palabra) > 1: #si es la letra 3 o mayor (ya está definida la orientacion)
                            if orientada(event, orientacion): #si la casilla es consecutiva según la orientación definida
                                colocar_letra(event, posAtril, letra, palabra, fichas_desocupadas, casillas_ocupadas) #coloco la letra en la casilla
                                posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
                                letra = '' #idem pero con la letra
                    inicial = False
            else:
                if letra != '': #si previamente clickee una letra del atril
                    if len(palabra) == 0: #si es la primer letra de la palabra
                        colocar_letra(event, posAtril, letra, palabra, fichas_desocupadas, casillas_ocupadas) #coloco la letra en la casilla
                        posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
                        letra = '' #idem pero con la letra
                    elif len(palabra) == 1: #si es la segunda letra de la palabra
                        resultado = consecutivo(event)
                        if resultado[0]: #si la casilla (event) seleccionada es consecutivo a la letra anteriormente colocada
                            orientacion = resultado[1] #guardo la orientacion
                            colocar_letra(event, posAtril, letra, palabra, fichas_desocupadas, casillas_ocupadas) #coloco la letra en la casilla
                            posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
                            letra = '' #idem pero con la letra
                            print(orientacion) #
                    elif len(palabra) > 1: #si es la letra 3 o mayor (ya está definida la orientacion)
                        if orientada(event, orientacion): #si la casilla es consecutiva según la orientación definida
                            colocar_letra(event, posAtril, letra, palabra, fichas_desocupadas, casillas_ocupadas) #coloco la letra en la casilla
                            posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
                            letra = '' #idem pero con la letra

        elif event == 'Confirmar Palabra':
            orientacion = ''
            word = ''.join(letra for letra in palabra) #junto las letras colocadas
            print(word)
            if es_palabra(word) and len(word)>=2: #ya que lexicon y spelling toman como palabras a las letras individuales
                print('entra con puntos : ' + str(totalJUG)) #
                totalJUG = sumar_puntos(puntajes, casillasESP, palabra, casillas_ocupadas, totalJUG) #luego hay que ver si el que arma la palabra es el jugador o la maquina (totalJUG a modo de prueba)
                print('nuevo total: '+str(totalJUG)) #
                print() #
                window.Element('PJ').Update(value = totalJUG)
                mezclar(fichas_desocupadas, bolsa) #relleno el atril
                fichas_desocupadas = [] #reinicio la lista de fichas desocupadas
            else:
                print(word+' no es palabra') #
                if '0707' in casillas_ocupadas: #si era la palabra inicial vuelvo a activar la variable que indica que se colocará la primer palabra del juego
                    inicial = True
                devolver(fichas_desocupadas, casillas_ocupadas) #devuelve las letras al atril
                fichas_desocupadas = [] #reinicio la lista de fichas desocupadas
            palabra = [] #reinicio la lista
            casillas_ocupadas = [] #idem

    window.Close()

if __name__ == '__main__':
    main(nombre = 'Jugador', tema ='Claro', nivel = 'nivel1', tiempo = 3.0)
