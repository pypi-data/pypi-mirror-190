import numpy as np

def saludar():
    print("Hola, te saludo desde saludos.saludar()")

def prueba():
    print("Esto es una nueva prueba de la nueva versión 6.0.")

def generar_array(numeros):
    return np.arange(numeros)

class Saludo:
    def __init__(self):
        print("Hola te saludo desde Saludo.__init__()")


if __name__ == "__main__": # Con esta condición solo se ejecutaría el código de abajo al ejecutar el script original y no al ser llamado desde otro script (__name__ es __main__ cuando se ejecuta saludos y __name__ es saludos cuando se ejecuta test)
    print(generar_array(5))