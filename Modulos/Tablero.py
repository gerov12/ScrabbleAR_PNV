import PySimpleGUI as sg
import sys
import json
import time
import random
import pattern.es
import itertools as it
from pattern.es import tag
from Modulos import Reglas
from Modulos import GameOver


def main(nombre = 'Jugador', tema ='claro', nivel = 'nivel1', tiempo = 3.0, modificado = False, modificado2 = False):
    def cargar_diccionarios(dic_verbs, dic_lexicon, dic_spelling):
        '''Crea un nuevo diccionario para los 3 del modulo pattern.es pero quitandole las tildes a las palabras'''
        for pal in pattern.es.verbs.keys():
            aux = []
            aux.append(pal.lower()) #guardo la key
            for p in pattern.es.verbs[pal]:
                aux.append(p.lower()) #guardo las conjugaciones de la key
            for i in aux: #le quito la tilde a todas las palabras que guardé
                i = i.replace('á','a')
                i = i.replace('é','e')
                i = i.replace('í','i')
                i = i.replace('ó','o')
                i = i.replace('ú','u')
                dic_verbs.append(i) #guardo cada palabra sin tilde en la lista de verbos

        for pal in pattern.es.lexicon.keys():
            aux_item = pattern.es.lexicon[pal] #guardo el contenido de la key
            aux_key = pal.lower() #guardo la key
            aux_key = aux_key.replace('á','a')
            aux_key = aux_key.replace('é','e')
            aux_key = aux_key.replace('í','i')
            aux_key = aux_key.replace('ó','o')
            aux_key = aux_key.replace('ú','u')
            dic_lexicon[aux_key] = aux_item #guardo en el nuevo diccionario pero sin tilde

        for pal in pattern.es.spelling.keys(): #idem
            aux_item = pattern.es.spelling[pal] #guardo el contenido de la key
            aux_key = pal.lower() #guardo la key
            aux_key = aux_key.replace('á','a')
            aux_key = aux_key.replace('é','e')
            aux_key = aux_key.replace('í','i')
            aux_key = aux_key.replace('ó','o')
            aux_key = aux_key.replace('ú','u')
            dic_spelling[aux_key] = aux_item #guardo en el nuevo diccionario pero sin tilde

    def llenar_bolsa(nivel):
        '''Carga las cantidades para cada letra segun el nivel ingresado por parametro.
        Si el usuario decide cambiar la cantidad de letras, estas se obtienen de otro archivo llamado letras_modificado.
        Si por alguna razon estos archivos no existen se levanta la excepcion y se le avisa al usuario
        mediante un Popup'''

        bolsa = []
        if not modificado:
            try:
                with open('Archivos/Letras.json','r') as archivo_letras:
                    letras = json.load(archivo_letras)
                    letrasN = letras[nivel] #toma el diccionario de letras:cantidades del nivel correspondiente
                    for letra, cantidad in letrasN.items():
                        for i in range(1,cantidad+1): #guarda "cantidad" veces la letra correspondiente
                            bolsa.append(letra)
            except (FileNotFoundError):
                sg.Popup('ERROR. La carpeta "Archivos" o el archivo JSON solicitado no existen.',no_titlebar=True)
                sys.exit()
        else:
            try:
                with open('Archivos/Letras_modificado.json','r') as archivo_letras:
                    letras = json.load(archivo_letras)
                    letrasN = letras #toma el diccionario de letras modificado
                    for letra, cantidad in letrasN.items():
                        for i in range(1,cantidad+1): #guarda "cantidad" veces la letra correspondiente
                            bolsa.append(letra)
            except (FileNotFoundError):
                sg.Popup('ERROR. La carpeta "Archivos" o el archivo JSON solicitado no existen.',no_titlebar=True)
                sys.exit()
        return bolsa

    def cargar_puntajes():
        '''Carga los puntajes para cada letra.
        Si el usuario los modificó, se obtienen de otro archivo llamado Puntajes_modificado.
        Si por alguna razon estos archivos no existen se levanta la excepcion y se le avisa al usuario
        mediante un Popup'''

        if not modificado2:
            try:
                with open('Archivos/Puntajes.json','r') as archivo_puntajes:
                    puntajes = json.load(archivo_puntajes)
            except (FileNotFoundError):
                sg.Popup('ERROR. La carpeta "Archivos" o el archivo JSON solicitado no existen.',no_titlebar=True)
                sys.exit()
        else:
            try:
                with open ('Archivos/Puntajes_modificado.json', 'r') as archivo_puntajes:
                    puntajes = json.load(archivo_puntajes)
            except (FileNotFoundError):
                sg.Popup('ERROR. La carpeta "Archivos" o el archivo JSON solicitado no existen.',no_titlebar=True)
                sys.exit()
        return puntajes

    def cargar_casillas():
        '''Carga las keys de las casillas del tablero
        Si el archivo con las keys no existe se levanta una excepcion y se avisa al usuario mediante un Popup'''
        try:
            with open('Archivos/Casillas.json','r') as archivo_casillas:
                cas = json.load(archivo_casillas)
            return cas
        except (FileNotFoundError):
            sg.Popup('ERROR. La carpeta "Archivos" o el archivo JSON solicitado no existen.',no_titlebar=True)
            sys.exit()

    def cargar_casillas_especiales(nivel):
        '''Carga las keys de las casillas especiales del tablero.
        Si el archivo con las keys no existe se levanta una excepcion y se avisa al usuario mediante un Popup'''
        try:
            with open ('Archivos/Especiales.json','r') as archivo_casillas: #falta escribir el archivo Especiales.json
                casillas_esp=json.load(archivo_casillas)
            return casillas_esp[nivel] #devuelve el dic del nivel correspondiente
        except (FileNotFoundError):
            sg.Popup('ERROR. La carpeta "Archivos" o el archivo JSON solicitado no existen.',no_titlebar=True)
            sys.exit()

    def cargar_tablero(casillas_esp, nivel):
        '''Crea el layout del tablero, asignandole a cada boton que lo conforma la key
        y el color correspondiente'''
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
        '''Activa los botones para cambiar letras si el boton para hacerlo fue clickeado'''
        window.Element('CAMBIO').Update(disabled = True)
        window.Element('TODAS').Update(disabled = False)    #activo las opciones
        window.Element('ALGUNAS').Update(disabled = False)
        window.Element('CANCEL').Update(disabled = False)
        for i in atril:
            window.Element(i).Update(disabled = True) #desactivo los clicks en el atril

    def desactivar():
        '''Desactiva los botones para cambiar letras si el boton para hacerlo fue clickeado'''
        window.Element('CAMBIO').Update(disabled = False)
        window.Element('TODAS').Update(disabled = True)    #activo las opciones
        window.Element('ALGUNAS').Update(disabled = True)
        window.Element('CANCEL').Update(disabled = True)
        for i in atril:
            window.Element(i).Update(disabled = False) #activo los clicks en el atril

    def mezclar(datos, bolsa,clickeo=False):
        '''Cambia las letras en 'datos' por letras al azar de la bolsa ('datos' contiene las fichas del atril a cambiar).
        De no tener suficientes fichas en la bolsa no realiza modificaciónes y avisa al jugador con un Popup'''
        aux=False #aux indica si se cambiaron las letras
        if len(bolsa) >= len(datos): #si tengo 7 o mas elementos en la bolsa, entro
            for i in datos:
                pos = random.randrange(len(bolsa))
                window.FindElement(i).Update(text=bolsa[pos])
                let = window.Element(i).GetText() #guardo la letra que acabo de colocar en el atril
                window.Element(i).Update(image_filename = 'Imagenes/Temas/'+tema.lower()+'/'+let+'_'+tema.lower()+'.png') #le coloco la imagen correspondiente al botón
                del bolsa[pos]
            aux=True #Si cambio las letras
        elif len(bolsa) < len(datos):
            if (clickeo):
                sg.PopupNoButtons('Solo se pueden cambiar '+str(len(bolsa))+' letras.',auto_close=True,auto_close_duration=3,no_titlebar=True)
        else:
            sg.PopupNoButtons('No quedan letras en la bolsa',auto_close=True,auto_close_duration=3,no_titlebar=True) #?
        return aux

    def colocar_letra(casilla, posA, let, pal, fichas_desocupadas, casillas_ocupadas):
        '''Coloca la letra en la casilla correspondiente y la quita del atril.
        Retorna la posicion del atril en la que fue colocada'''
        window.Element(casilla).Update(text=let) #pongo la letra "let" como texto de la "casilla" clickeada
        window.Element(casilla).Update(image_filename = 'Imagenes/Temas/'+tema.lower()+'/'+let+'_'+tema.lower()+'.png') #le coloco la imagen correspondiente al botón
        window.Element(posA).Update(text='') #la elimino del atril (reemplazandola por '')
        window.Element(posA).Update(image_filename = 'Imagenes/Temas/invisible.png') #elimino la imagen del atril
        palabra.append(let) #guardo la letra en la lista de letras para luego verificar si es una palabra
        fichas_desocupadas.append(posA) #guardo la pos del atril desocupada para luego devolver o colocar letras
        casillas_ocupadas.append(casilla) #guardo la key de la casilla ocupada en la lista
        return casilla #la pos donde se coloca la letra

    def consecutivo(casilla,anterior): #
        '''Indica si la casilla seleccionada es consecutivo a la letra anteriormente colocada.
        Retorna una lista con un booleano y la orientacón de la palabra'''
        aux = False
        orient = ''
        izquierda = str((int(casilla[0:2])-1))+casilla[2:4] #(el primer digito-1)+el segundo digito (es decir la casilla de la izquierda)
        arriba = casilla[0:2]+str((int(casilla[2:4])+1)) #el primer digito+(el segundo digito+1) (es decir la casilla de arriba)
        if izquierda[0]!='-': #si el primer digito de "izquierda" no es '-' (es decir que no elegí una casilla de la columna 0)
            if len(izquierda)<4: #si el valor de x queda de un solo digito
                izquierda = '0'+izquierda #le agrego un 0 adelante para que respete el formato de las keys de las casillas
            if (int(anterior[0:2]) == int(casilla[0:2])-1) and (int(anterior[2:4]) == int(casilla[2:4])): #verifico que sea consecutivo a la letra anterior
                if window.Element(izquierda).GetText() != '': #si el elemento de la izquierda no está vacío
                    aux = True #elegí una casilla consecutiva a la primer letra
                    orient = 'Horizontal' #y comencé a armar la palabra de manera horizontal
                    return [aux, orient]
        if int(arriba[2:4])<15: #si no elegí una casilla correcta para la orientacion horizontal chequeo si es vertical
        #si el sgundo digito de la casilla de arriba es menor a 4 (es decir que no elegí una casilla de la fila 3)
        #(el 4 mas adelante debería cambiarse por la altura del tablero)
            if len(arriba)<4: #si el valor de y queda de n digito
                arriba = arriba[0:2]+'0'+arriba[2] #le agrego un 0 adelante
            if int(anterior[0:2]) == int(casilla[0:2]) and int(anterior[2:4]) == int(casilla[2:4])+1:
                if window.Element(arriba).GetText() != '': #si el elemento de arriba no está vacío
                    aux = True #elegí una casilla consecutiva a la primer letra
                    orient = 'Vertical' #y comencé a armar la palabra de manera vertical
                    return [aux, orient]
        return [aux, orient] #devuelve Flase y ''

    def orientada(casilla, orient,anterior):
        '''Retorna un booleano que indica si la casilla seleccionada cumple con la orientacion definida'''
        aux = False
        if orient == 'Horizontal': #si la orientacion es horizontal hago el chequeo correspondiente
            izquierda = str((int(casilla[0:2])-1))+casilla[2:4]
            if izquierda[0]!='-':
                if len(izquierda)<4: #si el valor de x queda de un solo digito
                    izquierda = '0'+izquierda #le agrego un 0 adelante para que respete el formato de las keys de las casillas
                if (int(anterior[0:2]) == int(casilla[0:2])-1) and (int(anterior[2:4]) == int(casilla[2:4])): #verifico que sea consecutivo a la letra anterior
                    if window.Element(izquierda).GetText() != '':
                        aux = True
        elif orient == 'Vertical': #si la orientacion es vertical hago el chequeo correspondiente
            arriba = casilla[0:2]+str((int(casilla[2:4])+1))
            if int(arriba[2:4])<15:
                if len(arriba)<4: #si el valor de y queda de n digito
                    arriba = arriba[0:2]+'0'+arriba[2] #le agrego un 0 adelante
                if int(anterior[0:2]) == int(casilla[0:2]) and int(anterior[2:4]) == int(casilla[2:4])+1:
                    if window.Element(arriba).GetText() != '':
                        aux = True
        return aux

    def elegir_clasificacion ():
        '''Mediante un random decide que tipo de palabra será la admitida en el nivel 3
        0 -> Adjetivos
        1 -> Verbos'''

        if random.randint(0, 1) == 1:
            return 'VB' #verbos
        else:
            return 'JJ' #adjetivos

    def seleccion_random ():
        return(random.randint(0,1))

    def es_palabra(pal, nivel,clasificacion=999):
        '''Determina si el conjunto de letras ingresado es una palabra.
        En el caso del nivel 2 y 3 también verifica si pertenece al tipo de palabra correspondiente al nivel que se esta jugando.'''

        aux = False
        if len(pal) >= 2: #solo se admiten palabras que contengan minimo 2 letras
            if not pal.lower() in dic_verbs:
                if pal.lower() in dic_lexicon:
                    print(pal + " en lexicon")
                    if pal.lower() in dic_spelling:
                        print(pal + " en spelling")
                        aux = True
            else:
                print(pal + " en verbs")
                aux = True

            if aux:
                p,tipo=tag(pal)[0] #guardo el tipo de palabra
                print(tag(pal)[0])
                print('tipo'+tipo)
                if nivel == 'nivel1':
                    return True
                elif nivel == 'nivel2':
                    if tipo == 'VB' or tipo == 'JJ':
                        return True
                    else:
                        sg.PopupNoButtons('Tipo de palabra no valido para este nivel',auto_close=True,auto_close_duration=4,no_titlebar=True)
                        return False
                elif nivel =='nivel3':
                    if tipo == clasificacion:
                        return True
                    else:
                        sg.PopupNoButtons('Tipo de palabra no valido para este nivel',auto_close=True,auto_close_duration=4,no_titlebar=True)
                        return False
        else:
            return False

    def turno_COM (atrilCOM ,nivel, bolsaCOM, cant_COM, inicial, tema, puntajes, casillas_esp, puntCOM, clasificacion = 999):

        colocada = False

        letrasCOM = []
        for i in atrilCOM:
            letrasCOM.append(window.FindElement(i).GetText()) #guardo las letras del atril
            print(letrasCOM)#

        palabrasCOM = set()
        for i in range(2, 8):
            palabrasCOM.update((map("".join, it.permutations(letrasCOM, i)))) #formo todas las permutaciones posibles

        pal_validas = []
        for i in palabrasCOM:
            if nivel == "nivel3":
                if es_palabra(i, nivel, clasificacion): #filtro las palabras validas
                    pal_validas.append(i)
                    print("encontró una pal valida")#
            else:
                if es_palabra(i, nivel): #filtro las palabras validas
                    pal_validas.append(i)
                    print("encontró una pal valida")#

        cambio = False
        if len(pal_validas) == 0:
            if cant_COM <= 3:
                cambio = mezclar(atrilCOM, bolsaCOM)
                return [colocada, cambio, inicial, puntCOM] #retorna si colocó la palabra, si cambio las letras y la variable "inicial"
            else:
                window.Close()
                GameOver(totalJUG,puntCOM)
                sys.exit()
        else: #si tiene palabra valida
            orientacion = seleccion_random() #0 es vertical y 1 es horizontal
            if (inicial):
                print("pal inicial")#
                aux = random.randrange(len(pal_validas[0])) #la letra que ocupará la casilla inicial
                if orientacion == 1: #si es horizontal
                    ocupadas = []
                    coordenada_inicial = "0"+str(7-aux)+"07" #calculo la key de la coordenada inicial
                    for i in range(len(pal_validas[0])):
                        aux_x = int(coordenada_inicial[0:2])+i
                        if aux_x<10:
                            aux_x = '0'+str(aux_x) #si el valor de la coordenada x es de un solo digito le agrego un 0 adelante
                        else:
                            aux_x = str(aux_x)

                        window.FindElement(aux_x+'07').Update(text=pal_validas[0][i]) #coloco la letra
                        window.FindElement(aux_x+'07').Update(image_filename='Imagenes/Temas/'+tema.lower()+'/'+pal_validas[0][i]+'_'+tema.lower()+'.png') #y la imagen
                        ocupadas.append(aux_x+'07') #agrego la casilla ocupada a la lista

                    desocupadasCOM = [] #keys que desocupa

                    for i in range(len(pal_validas[0])): #itero las letras de la palabra ingresada
                        for j in atrilCOM:
                            if window.Element(j).GetText() == pal_validas[0][i]: #si la pos j del atril la contiene la elimino
                                window.Element(j).Update(text = "")
                                window.Element(j).Update(image_filename='Imagenes/Temas/invisible.png')
                                desocupadasCOM.append(j) #agrego la key a la lista de keys desocupadas
                                break

                    relleno = mezclar(desocupadasCOM, bolsaCOM) #relleno el atril

                    colocada = True
                    inicial = False

                    puntos = sumar_puntos(puntajes, casillas_esp, pal_validas[0], ocupadas, puntCOM) #hay que retornar los puntos

                    del pal_validas
                    print("Palabra colocada")
                    return [colocada, cambio, inicial, puntos, relleno] #retorna si colocó la palabra, si cambio las letras , la variable "inicial" y si pudo rellenar el atril

                else: #si es vertical
                    ocupadas = []
                    coordenada_inicial = "07"+"0"+str(7+aux) #calculo la key de la coordenada inicial
                    for i in range(len(pal_validas[0])):
                        aux_y = int(coordenada_inicial[2:])-i
                        if aux_y<10:
                            aux_y = '0'+str(aux_y) #si el valor de la coordenada x es de un solo digito le agrego un 0 adelante
                        else:
                            aux_y = str(aux_y)

                        window.FindElement('07'+aux_y).Update(text=pal_validas[0][i]) #coloco la letra
                        window.FindElement('07'+aux_y).Update(image_filename='Imagenes/Temas/'+tema.lower()+'/'+pal_validas[0][i]+'_'+tema.lower()+'.png') #y la imagen
                        ocupadas.append('07'+aux_y) #agrego la casilla ocupada a la lista

                    desocupadasCOM = [] #keys que desocupa

                    for i in range(len(pal_validas[0])): #itero las letras de la palabra ingresada
                        for j in atrilCOM:
                            if window.Element(j).GetText() == pal_validas[0][i]: #si la pos j del atril la contiene la elimino
                                window.Element(j).Update(text = "")
                                window.Element(j).Update(image_filename='Imagenes/Temas/invisible.png')
                                desocupadasCOM.append(j) #agrego la key a la lista de keys desocupadas
                                break

                    relleno = mezclar(desocupadasCOM, bolsaCOM) #relleno el atril

                    colocada = True
                    inicial = False

                    puntos = sumar_puntos(puntajes, casillas_esp, pal_validas[0], ocupadas, puntCOM) #hay que retornar los puntos

                    del pal_validas
                    print("Palabra colocada")
                    return [colocada, cambio, inicial, puntos, relleno] #retorna si colocó la palabra, si cambio las letras , la variable "inicial" y si pudo rellenar el atril

            else:
                intentos = 0 #cantididad de orientaciones intentadas (maximo 2)
                while intentos < 2:

                    if orientacion == 1: #cambio la orientación
                        orientacion = 0
                    else:
                        orientacion = 1

                    if orientacion == 1: #horizontal
                        print("horizontal")#
                        while len(pal_validas) > 0:
                            invalidas = []
                            colocada = False
                            while colocada == False and len(invalidas) <= (15*(len(pal_validas[0])-1)): #mientras no haya colocado la palabra y haya coordenadas iniciales validas
                                x = random.randrange(15-(len(pal_validas[0])-1))
                                if x<10:
                                    coordenada_inicial = '0'+str(x) #si el valor de la coordenada x es de un solo digito le agrego un 0 adelante
                                else:
                                    coordenada_inicial = str(x)

                                y = random.randrange(15)
                                if y<10:
                                    coordenada_inicial = coordenada_inicial+'0'+str(y) #si el valor de la coordenada y es de un solo digito le agrego un 0 adelante
                                else:
                                    coordenada_inicial = coordenada_inicial+str(y)

                                if not coordenada_inicial in invalidas: #si no verifiqué esta coordenada inicial
                                    desocupadas = 0 #cantidad de casillas libres
                                    for i in range(len(pal_validas[0])): #verifico que todas las casillas a ocupar no esten ocupadas
                                        aux_X = int(coordenada_inicial[0:2])+i
                                        if aux_X<10:
                                            aux_X = '0'+str(aux_X) #si el valor de la coordenada x es de un solo digito le agrego un 0 adelante
                                        else:
                                            aux_X = str(aux_X)
                                        if window.FindElement(aux_X+coordenada_inicial[2:]).GetText() == "": #si está desocupada
                                            desocupadas = desocupadas + 1

                                    if desocupadas == len(pal_validas[0]): #si todas las casillas están desocupadas coloco la palabra
                                        ocupadas = [] #casillas ocupadas
                                        for i in range(len(pal_validas[0])):
                                            aux_x = int(coordenada_inicial[0:2])+i
                                            if aux_x<10:
                                                aux_x = '0'+str(aux_x) #si el valor de la coordenada x es de un solo digito le agrego un 0 adelante
                                            else:
                                                aux_x = str(aux_x)

                                            window.FindElement(aux_x+coordenada_inicial[2:]).Update(text=pal_validas[0][i]) #coloco la letra
                                            window.FindElement(aux_x+coordenada_inicial[2:]).Update(image_filename='Imagenes/Temas/'+tema.lower()+'/'+pal_validas[0][i]+'_'+tema.lower()+'.png') #y la imagen
                                            ocupadas.append(aux_x+coordenada_inicial[2:]) #agrego la casilla ocupada a la lista

                                        desocupadasCOM = [] #keys que desocupa

                                        for i in range(len(pal_validas[0])): #itero las letras de la palabra ingresada
                                            for j in atrilCOM:
                                                if window.Element(j).GetText() == pal_validas[0][i]: #si la pos j del atril la contiene la elimino
                                                    window.Element(j).Update(text = "")
                                                    window.Element(j).Update(image_filename='Imagenes/Temas/invisible.png')
                                                    desocupadasCOM.append(j) #agrego la key a la lista de keys desocupadas
                                                    break

                                        relleno = mezclar(desocupadasCOM, bolsaCOM) #relleno el atril

                                        colocada = True

                                        puntos = sumar_puntos(puntajes, casillas_esp, pal_validas[0], ocupadas, puntCOM) #hay que retornar los puntos

                                        del pal_validas
                                        print("Palabra colocada")
                                        return [colocada, cambio, inicial, puntos, relleno]#retorna si colocó la palabra, si cambio las letras , la variable "inicial" y si pudo rellenar el atril

                                    else:
                                        invalidas.append(coordenada_inicial)

                            if len(invalidas) > (15*(len(pal_validas[0])-1)): #si se acabaron las coordenadas iniciales validas (la palabra no entra)
                                del pal_validas[0] #la segunda palabra pasa a ser la 0
                                del invalidas #vacio la lista de coordenadas iniciales validas

                    else: #si es vertical
                        print("vertical")#
                        while len(pal_validas) > 0:
                            invalidas = []
                            colocada = False
                            while colocada == False and len(invalidas) <= (15*(len(pal_validas[0])-1)): #mientras no haya colocado la palabra y haya coordenadas iniciales validas
                                x = random.randrange(15)
                                if x<10:
                                    coordenada_inicial = '0'+str(x) #si el valor de la coordenada x es de un solo digito le agrego un 0 adelante
                                else:
                                    coordenada_inicial = str(x)

                                y = random.randrange((0+len(pal_validas[0])),15)
                                if y<10:
                                    coordenada_inicial = coordenada_inicial+'0'+str(y) #si el valor de la coordenada y es de un solo digito le agrego un 0 adelante
                                else:
                                    coordenada_inicial = coordenada_inicial+str(y)

                                if not coordenada_inicial in invalidas: #si no verifiqué esta coordenada inicial
                                    desocupadas = 0 #cantidad de casillas libres
                                    for i in range(len(pal_validas[0])): #verifico que todas las casillas a ocupar no esten ocupadas
                                        aux_Y = int(coordenada_inicial[2:])-i
                                        if aux_Y<10:
                                            aux_Y = '0'+str(aux_Y) #si el valor de la coordenada x es de un solo digito le agrego un 0 adelante
                                        else:
                                            aux_Y = str(aux_Y)
                                        if window.FindElement(coordenada_inicial[0:2]+aux_Y).GetText() == "": #si está desocupada
                                            desocupadas = desocupadas + 1

                                    if desocupadas == len(pal_validas[0]): #si todas las casillas están desocupadas coloco la palabra
                                        ocupadas = [] #casillas ocupadas
                                        for i in range(len(pal_validas[0])):
                                            aux_y = int(coordenada_inicial[2:])-i
                                            if aux_y<10:
                                                aux_y = '0'+str(aux_y) #si el valor de la coordenada x es de un solo digito le agrego un 0 adelante
                                            else:
                                                aux_y = str(aux_y)

                                            window.FindElement(coordenada_inicial[0:2]+aux_y).Update(text=pal_validas[0][i]) #coloco la letra
                                            window.FindElement(coordenada_inicial[0:2]+aux_y).Update(image_filename='Imagenes/Temas/'+tema.lower()+'/'+pal_validas[0][i]+'_'+tema.lower()+'.png') #y la imagen
                                            ocupadas.append(coordenada_inicial[0:2]+aux_y) #agrego la casilla ocupada a la lista

                                        desocupadasCOM = [] #keys que desocupa

                                        for i in range(len(pal_validas[0])): #itero las letras de la palabra ingresada
                                            for j in atrilCOM:
                                                if window.Element(j).GetText() == pal_validas[0][i]: #si la pos j del atril la contiene la elimino
                                                    window.Element(j).Update(text = "")
                                                    window.Element(j).Update(image_filename='Imagenes/Temas/invisible.png')
                                                    desocupadasCOM.append(j) #agrego la key a la lista de keys desocupadas
                                                    break

                                        relleno = mezclar(desocupadasCOM, bolsaCOM) #relleno el atril

                                        colocada = True

                                        puntos = sumar_puntos(puntajes, casillas_esp, pal_validas[0], ocupadas, puntCOM) #hay que retornar los puntos

                                        del pal_validas
                                        print("Palabra colocada")
                                        return [colocada, cambio, inicial, puntos, relleno] #retorna si colocó la palabra, si cambio las letras , la variable "inicial" y si pudo rellenar el atril

                                    else:
                                        invalidas.append(coordenada_inicial)

                            if len(invalidas) > (15*(len(pal_validas[0])-1)): #si se acabaron las coordenadas iniciales validas (la palabra no entra)
                                del pal_validas[0] #la segunda palabra pasa a ser la 0
                                del invalidas #vacio la lista de coordenadas iniciales validas

                    intentos += 1 #ya intenté con una orientacion

                if cant_COM <= 3: #si no pudo poner la palabra en vertical ni en horizontal intenta cambiar letras
                    cambio = mezclar(atrilCOM, bolsaCOM)
                    return [colocada, cambio, inicial, puntCOM] #retorna si colocó la palabra, si cambio las letras y la variable "inicial"
                else:
                    window.Close()
                    GameOver.main(totalJUG, puntCOM, nombre, tema, nivel, tiempo, modificado, modificado2)
                    sys.exit()

    def devolver(fichas_desocupadas, casillas_ocupadas):
        '''Devuelve las letras al atril en caso de que una palabra sea incorrecta'''
        for i in range(len(fichas_desocupadas)):
            pos = random.randrange(len(casillas_ocupadas)) #elijo una casilla ocupada al azar
            letter = window.FindElement(casillas_ocupadas[pos]).GetText() #guardo la letra de la pos
            window.FindElement(casillas_ocupadas[pos]).Update(text = '') #elimino la letra de la pos
            window.FindElement(casillas_ocupadas[pos]).Update(image_filename = 'Imagenes/Temas/invisible.png') #elimino la imagen de la pos
            window.FindElement(fichas_desocupadas[i]).Update(text=letter)  #coloco la letra en la casilla
            window.FindElement(fichas_desocupadas[i]).Update(image_filename='Imagenes/Temas/'+tema.lower()+'/'+letter+'_'+tema.lower()+'.png')  #coloco la letra en la casilla
            del casillas_ocupadas[pos] #quito la casilla que acabo de "limpiar" de la lista de casillas ocupadas

    def sumar_puntos (puntajes,casillas_esp,palabra,casilla,actual):
        '''Calcula el puntaje de la palabra, lo suma al total los puntos y retorna este último'''

        print('entra a la funcion') #
        total=0
        valor=0 #valor por el que hay que multiplicar la palabra
        restar=0#valor por el que hay que restar la palabra
        ok=False #si hay casilla multiplicadora de palabra
        ok2=False#si hay una casilla de resto
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
                elif casillas_esp[casilla[i]][0] == 'R2':
                    print('suma '+str(total)+'+'+str(puntajes[palabra[i]])) #
                    print('restará = '+str(restar)+' + 2') #
                    total += puntajes[palabra[i]]
                    print('sumó = '+str(total)) #
                    restar+=2
                    ok2 = True
            else: #si no es una casilla especial, suma normal
                print('no es especial') #
                print('suma '+str(total)+'+'+str(puntajes[palabra[i]])) #
                total += puntajes[palabra[i]]
                print('sumó = '+str(total)) #
            print('------------------------------')
        if ok: #si hay que multiplicar la palabra entera
            print('multiplicó '+str(total)+'*'+str(valor)) #
            total = total*valor
        if ok2: #si hay que restar puntos
            print('resto '+str(total)+'-'+str(restar))#
            total-=restar
        print('suma final: '+str(total)) #
        actual += total #al puntaje actual le agrego el obtenido con la nueva palabra
        return actual

    def extraer_datos_top10(nivel):
        '''Abre el archivo JSON que tiene la informacion del top 10 del nivel ingresado como parametro,
        deserializa la informacion y la retorna'''

        with open('Archivos/top10_'+nivel+'.json', 'r') as archivo: #abro el archivo del top 10 en modo lectura
            info = json.load(archivo) #deserializo la info que tiene el archivo
        return info #en info esta el contenido del archivo

    def guardar_datos (nivel,datos):
        '''Si el archivo NO existe lo crea, serializa la informacion ingresada en 'datos' y lo carga en el archivo JSON.
        Si el archivo existe, lo abre, actualiza la información y la carga en el archivo JSON'''
        with open('Archivos/top10_'+nivel+'.json','w') as archivo: #(si no existe lo creo al archivo) lo abro en modo escritura
            json.dump(datos,archivo) #serializo la info

    def calcular_top10(nivel,puntaje): #recibo el puntaje del jugador
        '''Una vez terminado el juego, esta funcion se fija en el puntaje del jugador:
        ->Si el archivo top 10 del nivel actual no existe, se levanta una excepcion,
        esta es manejada por el bloque try-except el cuál crea el archivo cargando la informacion del jugador actual.
        ->Si el archivo top 10 del nivel correspondiente existe, carga el nuevo puntaje a la estructura de datos
        la ordena y determina si tiene longitud mayor a 10. Si esta estructura de datos tiene longitud mayor a 10
        se elimina el ultimo puntaje'''

        if nombre != "Jugador":
            n = nombre
        else:
            n = "Desconocido"

        nuevo={"nombre": n, "puntaje":puntaje, "fecha":time.strftime("%d %b %Y %H:%M"), "nivel":nivel} #creo un dic para cargar la info nueva
        try:
            datos = extraer_datos_top10(nivel) #si existe, voy a asignarle su contenido a la variable datos
            #if not puntaje in datos["puntaje"]:
            datos.append(nuevo) #cargo el nuevo puntaje
            datos=sorted(datos,key=lambda jugador: jugador['puntaje'],reverse=True) #lo ordeno, para ver si el nuevo puntaje supera a algunos de los puntajes del archivo
            if len(datos) > 10: #si tengo 11 elementos entro
                del datos[10] #elimino el dato que no me sirve (elemento n 11 de la lista)
        except (FileNotFoundError): #aca solo va a entrar una sola vez, (el primer dato de la lista)
            datos=[]#creo una lista de diccionario para guardar mis datos
            datos.append(nuevo)#agrego el primer puntaje
        finally:
            guardar_datos(nivel,datos) #llamo a la funcion que serializa la info para subir la info al archivo

####################################################################################################################################################################################################

    sg.ChangeLookAndFeel('DarkAmber')
    dic_verbs = [] #lista con todos los verbos (infinitivos + conjugaciones) modificados (sin tildes)
    dic_lexicon = {}  #diccionario de pattern modificado (sin tildes)
    dic_spelling = {} #diccionario de pattern modificado (sin tildes)
    cargar_diccionarios(dic_verbs, dic_lexicon, dic_spelling) #modifico las palabras (les quito las tildes)
    bolsa = llenar_bolsa(nivel) #lleno la bolsa del jugador
    bolsaCOM = bolsa #lleno la bolsa de la computadora
    puntajes = cargar_puntajes() #cargo los puntajes de las fichas
    casillasESP = cargar_casillas_especiales(nivel)
    if (nivel == 'nivel3'): #se selecciona el tipo de palabra a utilizar
        clasificacion= elegir_clasificacion()
        if clasificacion == 'VB': #mensaje para el usuario
            sg.PopupNoButtons('En esta partida solo se usaran verbos',auto_close=True,auto_close_duration=3,no_titlebar=True)
        else:
            sg.PopupNoButtons('En esta partida solo se usaran adjetivos',auto_close=True,auto_close_duration=3,no_titlebar=True)

    #keys de las casillas y las posiciones del atril (se usa para saber dónde clickea el jugador)
    casillas = cargar_casillas()
    atril = ['J1','J2','J3','J4','J5','J6','J7']
    atrilCOM = ['C1','C2','C3','C4','C5','C6','C7']

    #layout del tablero
    tablero = cargar_tablero(casillasESP,nivel) #las casillas especiales se mandarían como parametro para configurar el color de c/u

    #texto con el puntaje de la PC (layout para el frame)
    puntCOM = [
        [sg.Text(0, size=(52,1), text_color= 'white', background_color= 'grey',key='PC')]
    ]

    #texto con el puntaje del jugador (layout para el frame)
    puntJUG = [
        [sg.Text(0, size=(52,1), text_color= 'white', background_color= 'grey', key='PJ')]
    ]

    #marco con el atril de la PC
    frameAtrilCOM = [
        [sg.Button('',visible=False,key='C1'),sg.Button('',visible=False,key='C2'),sg.Button('',visible=False,key='C3'),sg.Button('',visible=False,key='C4'),sg.Button('',visible=False,key='C5'),sg.Button('',visible=False,key='C6'),
        sg.Button('',visible=False,key='C7'),sg.Button('?',size=(2,2), button_color = ('black','white')),sg.Button('?',size=(2,2), button_color = ('black','white')),sg.Button('?',size=(2,2), button_color = ('black','white')),
        sg.Button('?',size=(2,2), button_color = ('black','white')),sg.Button('?',size=(2,2), button_color = ('black','white')),sg.Button('?',size=(2,2), button_color = ('black','white')),
        sg.Button('?',size=(2,2), button_color = ('black','white'))],
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

    frameTiempo = [
        [sg.Text('', size=(21,1), font=('Timer', 20), justification='center', key='time')]
    ] #Interfaz del cronometro

    #elementos de la derecha de la ventana
    colExtras = [
            [sg.Frame('',frameAtrilCOM,border_width=8)], #atril de la PC
            [sg.Frame('PUNTAJE COMPUADORA', puntCOM, title_color='white',background_color='black', key= 'LC')], #puntaje de la PC
            #[sg.Text('')],
            [sg.Button("COM")],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Frame('Tiempo',frameTiempo, title_color='white',background_color='black')],
            [sg.Text('')],
            [sg.Button('Pausa', size=(23,1), key='pausa', button_color = ('black','white')),sg.Button('Reglas', size=(23,1), pad=(8,0), button_color = ('black','white'), key = 'reglas')],
            [sg.Button('Terminar', size=(23,1), key='terminar', button_color=('black','white')), sg.Button('Guardar Partida', size=(23,1),pad=(8,0), key='guardar', button_color=('black', 'white'))], #Falta implementacion
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Text('')],
            [sg.Button('Confirmar Palabra', size=(52,1), button_color = ('black','white'))],
            [sg.Button('Cambiar Letras', disabled = False, button_color = ('black','white'), key = 'CAMBIO',size=(9,1)),
            sg.Button('Todas', disabled = True, button_color = ('black','white'), key = 'TODAS', size=(9,1)),
            sg.Button('Algunas', disabled = True, button_color = ('black','white'), key = 'ALGUNAS', size=(9,1)),
            sg.Button('Cancelar', disabled = True, button_color = ('black','white'), key = 'CANCEL', size=(9,1))],
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
        indice = random.randrange(len(bolsaCOM)) #tomo una letra random de la bolsa de letras
        window.Element(aux).Update(text=bolsaCOM[indice]) #la pongo como texto del boton correspondiente
        let = window.Element(aux).GetText() #guardo la letra que acabo de colocar en el atril
        window.Element(aux).Update(image_filename = 'Imagenes/Temas/'+tema.lower()+'/'+let+'_'+tema.lower()+'.png') #le coloco la imagen correspondiente al botón
        del bolsaCOM[indice] #la elimino de la bolsa

    for i in range(1,8): #lo mismo pero para el atril del Jugador
        aux = 'J'+str(i)
        indice = random.randrange(len(bolsa))
        window.Element(aux).Update(text=bolsa[indice])
        let = window.Element(aux).GetText() #guardo la letra que acabo de colocar en el atril
        window.Element(aux).Update(image_filename = 'Imagenes/Temas/'+tema.lower()+'/'+let+'_'+tema.lower()+'.png') #le coloco la imagen correspondiente al botón
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
    cambioActivado = False #si se están cambiando l etras
    a_cambiar = [] #lista de pos de atril a cambiar con mezclar()
    cant = 1 #cantidad de veces que el jugador apreta "Cambiar letras"
    cant_COM = 1 #cantidad de veces que la computadora apreta "Cambiar letras"

    actual_time = 0
    paused = False
    start_time = int(round(time.time() * 100))
    while True:
        event, values = window.Read(timeout=10)  #Ni idea que hace el timeout
        if event is None:
            break
        if actual_time >= (int(tiempo)*60)*100:       #CENTESIMAS
            sg.Popup('Terminó el Tiempo', no_titlebar = True)
            calcular_top10(nivel,totalJUG)
            window.Close()
            GameOver.main(totalJUG, totalCOM, nombre, tema, nivel, tiempo, modificado, modificado2)
            paused = True
            break

        if not paused:
            actual_time = int(round(time.time() * 100)) - start_time
        else:
            event,values = window.Read()


        if event == 'reglas':
            paused = True #Pongo en pausa el tiempo
            paused_time = int(round(time.time() * 100)) #Guardo donde quedo el tiempo
            if nivel == 'nivel1' or nivel == 'nivel2':
                Reglas.main(nivel)
            else:
                Reglas.main(nivel,clasificacion)
            if Reglas.reanudar_reloj():
                paused = False #Pongo play
                start_time = start_time + int(round(time.time() * 100)) - paused_time #Retomo desde donde quedé

        if event == 'pausa':
            if window.Element('pausa').GetText() == 'Pausa':
                paused = True
                paused_time = int(round(time.time() * 100))
                window.Element('pausa').Update(text='Continuar')
            else:
                paused = False
                start_time = start_time + int(round(time.time() * 100)) - paused_time
                window.Element('pausa').Update(text='Pausa')

        elif event == "COM":
            if nivel == "nivel3":
                aux = turno_COM(atrilCOM ,nivel, bolsaCOM, cant_COM, inicial, tema, puntajes, casillasESP, totalCOM, clasificacion)
                if aux[0]: #indica si se coloco una palabra
                    totalCOM = aux[3] #contiene los puntos totales de la computadora
                    window.Element("PC").Update(value = str(totalCOM))
                    print(totalCOM)
                    inicial = aux[2] #modifica la variable "inicial"
                    if not aux[4]: #indica si no se pudo rellenar el atril
                        window.Close()
                        GameOver.main(totalJUG, totalCOM, nombre, tema, nivel, tiempo, modificado, modificado2)
                        break
                elif aux[1]: #indica si se apreto el cambiar letras
                    cant_COM += 1
                else: #si no pudo colocar una palabra, ni cambiar las letras, finaliza el juego
                    window.Close()
                    GameOver.main(totalJUG, totalCOM, nombre, tema, nivel, tiempo, modificado, modificado2)
                    break

            else:
                aux = turno_COM(atrilCOM ,nivel, bolsaCOM, cant_COM, inicial, tema, puntajes, casillasESP, totalCOM)
                if aux[0]: #indica si se coloco una palabra
                    totalCOM = aux[3] #contiene los puntos totales de la computadora
                    window.Element("PC").Update(value = str(totalCOM))
                    print(totalCOM)
                    inicial = aux[2] #modifica la variable "inicial"
                    if not aux[4]: #indica si no se pudo rellenar el atril
                        window.Close()
                        GameOver.main(totalJUG, totalCOM, nombre, tema, nivel, tiempo, modificado, modificado2)
                        break
                elif aux[1]: #indica si se apreto el cambiar letras
                    cant_COM += 1
                else: #si no pudo colocar una palabra, ni cambiar las letras, finaliza el juego
                    window.Close()
                    GameOver.main(totalJUG, totalCOM, nombre, tema, nivel, tiempo, modificado, modificado2)
                    break

        elif event == 'CAMBIO' and len(palabra) == 0: #solo puedo cambiar letras si no coloqué ninguna en el tablero
            if cant <=3:
                activar() #hago utilizables los botones de cambio
            else:
                sg.PopupNoButtons('Esta función ya no esta disponible',auto_close=True,auto_close_duration=3,no_titlebar=True)


        elif event == 'TODAS': #cambia todas las letras del atril
            if mezclar(atril, bolsa,True):
                cant += 1 #incremento la variable que cuenta las veces que se apretó "Cambiar letras"
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
                if mezclar(a_cambiar, bolsa,True):
                    cant += 1 #incremento la variable que cuenta las veces que se apretó "Cambiar letras"
                    for i in a_cambiar:
                        window.Element(i).Update(button_color = ('black','white')) #vuelve a poner en blanco a todas las letras del atril
                else:
                    for i in a_cambiar:
                        window.Element(i).Update(button_color = ('black','white')) #vuelve a poner en blanco a todas las letras del atril
                        l = window.Element(i).GetText() #guardo la letra
                        window.Element(i).Update(image_filename = 'Imagenes/Temas/'+tema.lower()+'/'+l+'_'+tema.lower()+'.png') #le coloco la imagen original
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
                l = window.Element(i).GetText() #guardo la letra
                window.Element(i).Update(image_filename = 'Imagenes/Temas/'+tema.lower()+'/'+l+'_'+tema.lower()+'.png') #le coloco la imagen original
            a_cambiar = [] #vacío la lista de fichas a cambiar
            for i in atril:
                window.Element(i).Update(disabled = True) #desactivo los clicks en el atril
            window.Element('ALGUNAS').Update(disabled = False) #activo el botón que acabo de apretar


        elif event == 'CANCEL': #cancelo el cambio de letras y vuelvo a la funcionalidad normal del atril
            desactivar()
            cant -= 1 #decremento la variable que cuenta las veces que se apreta "Cambiar letras"


        elif event in atril: #si hago click en una letra del atril
            print('entro a atril. cambioActivado: '+str(cambioActivado))
            if cambioActivado: #si estoy cambiando letras
                if event in a_cambiar: #si ya está seleccionada la letra que elijo
                    a_cambiar.remove(event) #la elimino de la lista de seleccionadas
                    window.Element(event).Update(button_color = ('black','white')) #le devuelvo el color original
                    l = window.Element(event).GetText() #guardo la letra
                    window.Element(event).Update(image_filename = 'Imagenes/Temas/'+tema.lower()+'/'+l+'_'+tema.lower()+'.png')#le devuelvo la imagen original
                else:
                    a_cambiar.append(event)
                    window.Element(event).Update(button_color = ('black','grey'))
                    l = window.Element(event).GetText() #guardo la letra
                    window.Element(event).Update(image_filename = 'Imagenes/Temas/'+tema.lower()+'BN/'+l+'_'+tema.lower()+'.png') #le coloco la imagen en Blanco y Negro
                print(a_cambiar)
            else:
                posAtril = event #guarda la posicion en el atril de la letra clickeada
                letra = window.Element(posAtril).GetText() #guarda la letra clickeada


        elif event in casillas:#si hago click en una casilla del tablero
            if letra != '': #si previamente clickee una letra del atril
                if len(palabra) == 0: #si es la primer letra de la palabra
                    anterior = colocar_letra(event, posAtril, letra, palabra, fichas_desocupadas, casillas_ocupadas) #coloco la letra en la casilla
                    posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
                    letra = '' #idem pero con la letra
                elif len(palabra) == 1: #si es la segunda letra de la palabra
                    resultado = consecutivo(event,anterior)
                    if resultado[0]: #si la casilla (event) seleccionada es consecutivo a la letra anteriormente colocada
                        orientacion = resultado[1] #guardo la orientacion
                        anterior = colocar_letra(event, posAtril, letra, palabra, fichas_desocupadas, casillas_ocupadas) #coloco la letra en la casilla
                        posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
                        letra = '' #idem pero con la letra
                        print(orientacion) #
                elif len(palabra) > 1: #si es la letra 3 o mayor (ya está definida la orientacion)
                    if orientada(event, orientacion,anterior): #si la casilla es consecutiva según la orientación definida
                        anterior = colocar_letra(event, posAtril, letra, palabra, fichas_desocupadas, casillas_ocupadas) #coloco la letra en la casilla
                        posAtril = '' #borro la pos guardada para que no se guarde varias veces en el tablero al clickearlo
                        letra = '' #idem pero con la letra


        elif event == 'Confirmar Palabra':
            orientacion = ''
            word = ''.join(letra for letra in palabra) #junto las letras colocadas
            print(word)
            if nivel == 'nivel1' or nivel == 'nivel2':
                v_palabra = es_palabra(word, nivel) #booleano para entrar al if de mas abajo
            else:
                v_palabra = es_palabra(word, nivel,clasificacion)
            if v_palabra: #si es palabra
                if inicial: #si la palabra que coloqué es la primera del juego
                    if '0707' in casillas_ocupadas: #si la casilla inicial está ocupada
                        print('entra con puntos : ' + str(totalJUG)) #
                        totalJUG = sumar_puntos(puntajes, casillasESP, palabra, casillas_ocupadas, totalJUG) #luego hay que ver si el que arma la palabra es el jugador o la maquina (totalJUG a modo de prueba)
                        print('nuevo total: '+str(totalJUG)) #
                        print() #
                        window.Element('PJ').Update(value = totalJUG)
                        mezclar(fichas_desocupadas, bolsa) #relleno el atril
                        fichas_desocupadas = [] #reinicio la lista de fichas desocupadas
                        inicial = False #desactivo la variable que indica que la palabra inicial aún no se colocó
                    else: #si está desocupada
                        sg.PopupNoButtons("Una letra debe ocupar la casilla inicial", auto_close=True,auto_close_duration=3,no_titlebar=True) #informo el error
                        devolver(fichas_desocupadas, casillas_ocupadas) #devuelve las letras al atril
                        fichas_desocupadas = [] #reinicio la lista de fichas desocupadas
                else: #si no es la palabra incial prosigo normalmente
                    print('entra con puntos : ' + str(totalJUG)) #
                    totalJUG = sumar_puntos(puntajes, casillasESP, palabra, casillas_ocupadas, totalJUG) #luego hay que ver si el que arma la palabra es el jugador o la maquina (totalJUG a modo de prueba)
                    print('nuevo total: '+str(totalJUG)) #
                    print() #
                    window.Element('PJ').Update(value = totalJUG)
                    mezclar(fichas_desocupadas, bolsa) #relleno el atril
                    fichas_desocupadas = [] #reinicio la lista de fichas desocupadas
            else:
                print(word+' no es palabra') #
                sg.PopupNoButtons(word + ' no es palabra', auto_close=True, auto_close_duration=3, no_titlebar=True)
                if '0707' in casillas_ocupadas: #si era la palabra inicial vuelvo a activar la variable que indica que se colocará la primer palabra del juego
                    inicial = True
                devolver(fichas_desocupadas, casillas_ocupadas) #devuelve las letras al atril
                fichas_desocupadas = [] #reinicio la lista de fichas desocupadas
            palabra = [] #reinicio la lista
            casillas_ocupadas = [] #idem


        elif event == 'terminar':
            calcular_top10(nivel,totalJUG)
            window.Close()
            GameOver.main(totalJUG, totalCOM, nombre, tema, nivel, tiempo, modificado, modificado2)
            break
            
        window.FindElement('time').Update('{:02d}:{:02d}'.format((actual_time // 100) // 60,(actual_time // 100) % 60))

    window.Close()

if __name__ == '__main__':
    main(nombre = 'Jugador', tema ='Claro', nivel = 'nivel1', tiempo = 3.0)
