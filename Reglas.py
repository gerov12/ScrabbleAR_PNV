import PySimpleGUI as sg

ok_r = True
def reanudar_reloj(): #Sirve para reanudar el tiempo
    return ok_r

def main (nivel = 'nivel1',clasificacion =999):
    '''Según el nivel se muestra la imagen correspondiente'''
    
    if (nivel == 'nivel1'):
        reglas= [[sg.Image(filename = "Imagenes/Reglas/reglas_nivel1.png", size=(530,530))], [sg.Text('', size=(31,1)), sg.Button('Cerrar', button_color=('black','white'))],
        [sg.Text('', size=(1,1))]]
    elif (nivel == 'nivel2'):
        reglas= [[sg.Image(filename = "Imagenes/Reglas/reglas_nivel2.png", size=(530,530))], [sg.Text('', size=(31,1)), sg.Button('Cerrar', button_color=('black','white'))],
        [sg.Text('', size=(1,1))]]
    else:
        if (clasificacion == 'VB'):
            reglas= [[sg.Image(filename = "Imagenes/Reglas/reglas_nivel3vb.png", size=(530,530))], [sg.Text('', size=(31,1)), sg.Button('Cerrar', button_color=('black','white'))],
            [sg.Text('', size=(1,1))]]
        else:
            reglas= [[sg.Image(filename = "Imagenes/Reglas/reglas_nivel3jj.png", size=(530,530))], [sg.Text('', size=(31,1)), sg.Button('Cerrar', button_color=('black','white'))],
            [sg.Text('', size=(1,1))]]

    window = sg.Window('Reglas', no_titlebar=True).Layout(reglas).Finalize()

    while True:
        event, values = window.Read()
        if event == 'Cerrar':
            break
    window.Close()

if __name__ =='__main__':
    main(nivel = 'nivel1',clasificacion = 999)
