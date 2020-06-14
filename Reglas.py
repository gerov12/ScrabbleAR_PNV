import PySimpleGUI as sg

def main (nivel = 'nivel1',clasificacion =999):
        if (nivel == 'nivel1'):
            reglas= [[sg.Image(filename = "Imagenes/Reglas/reglas_nivel1.png", size=(530,530))],]
        elif (nivel == 'nivel2'):
            reglas= [[sg.Image(filename = "Imagenes/Reglas/reglas_nivel2.png", size=(530,530))],]
        else:
            if (clasificacion == 'VB'):
                reglas= [[sg.Image(filename = "Imagenes/Reglas/reglas_nivel3vb.png", size=(530,530))],]
            else:
                reglas= [[sg.Image(filename = "Imagenes/Reglas/reglas_nivel3jj.png", size=(530,530))],]

        window = sg.Window('Reglas').Layout(reglas).Finalize()

if __name__ =='__main__':
    main(nivel = 'nivel1',clasificacion = 999)
