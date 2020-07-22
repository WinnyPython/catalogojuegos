## Librerías usadas ##
import random
import os


## Funciones del programa ##
def borrar_pantalla ():
    x = input ("Presiona enter para continuar")
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

def reglas (juego):
    inicio = input ("Presione 1 para leer las instrucciones y cualquier otra tecla para iniciar a jugar: ")
    if inicio == "1":
        if juego == 1:
            print("Cada jugador obtiene dos cartas")
            print("Al usar una carta, el jugador recibe otra para volver a tener 2")
            print("Hay una cuenta global a la que se suma el valor de cada carta")
            print("El jugador que llegue a 99 o se pase, pierde")
            print("El que pierde queda eliminado y los otros juegan de nuevo con la cuenta en 0")
            print("Las letras valen 10 y las cartas numéricas tienen el valor de su número")
            print("Los comodines te dan la opción de elegir su valor o un valor diferente predeterminado")
            print("Estos son los comodines con su valor normal y su valor de comodín:")
            print("El 'As' vale 1 o -1")
            print("El 6 vale 6 o lleva la cuenta hasta 60 sin importar en qué número esté")
            print("El 9 vale 9 o 0")
            print("El 10 vale 10 o -10")
            print("El JOKER vale 11 o lleva la cuenta hasta 98")
            print("Para el juego solo se necesitan las teclas '1' y '2', evite usar otras distintas")
        elif juego == 2:
            print("Hay dos jugadores con un tablero cada uno")
            print("Los tableros tienen dimensión de 8X8")
            print("Filas y columnas se enumeran del 1 al 8")
            print("En el tablero muestra 0 donde no hay barcos")
            print("En el tablero muestra 1 donde hay barcos")
            print("Los barcos miden 4 casillas")
            print("Se colocan 4 barcos")
            print("Evite usar teclas diferentes a las pedidas")
        borrar_pantalla ()
    else:
        borrar_pantalla ()
        pass

def asignar_cartas (x):
    global banco
    global cartas
    banco = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "JOKER"]
    cartas = []
    for i in range (x):
        cartas.append ([])
        for j in range (2):
            cartas[i].append (random.choice (banco))

def valor_cuenta (a,b):
    valores = {"A":1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, "J":10, "Q":10, "K":10, "JOKER":11}
    comodin = {"A":-1, 9:0, 10:-10}
    reinicios = {6:60, "JOKER":98}
    if b in comodin.keys():
        turno = int (input ("¿Valor de la carta (1) o comodín (2)? "))
        if turno == 2:
            return a + comodin[b]
        else:
            return a + valores[b]
    elif b in reinicios.keys():
        turno = int (input ("¿Valor de la carta (1) o comodín (2)? "))
        if turno == 2:
            return reinicios[b]
        else:
            return a + valores[b]
    else:
        return a + valores[b]

def uso_carta (q,w):
    global banco
    global cartas
    global nombres
    global eliminados
    if eliminados[q] == True:
        return w
    else:
        print("La cuenta va en", w)
        print("Es el turno de", nombres[q])
        print("Estas son tus cartas:")
        print(cartas[q])
        seleccion = int (input ("¿Carta 1 o 2? "))
        if seleccion == 1:
            carta = cartas[q][0]
        elif seleccion == 2:
            carta = cartas[q][1]
        w = valor_cuenta (w,carta)
        print("La cuenta va en", w)
        cartas[q][seleccion - 1] = random.choice (banco)
        print("Tus nuevas cartas son:")
        print(cartas[q])
        borrar_pantalla ()
        return w

def asignar_nombres(x):
    global nombres
    global eliminados
    nombres = {}
    eliminados = {}
    for i in range (x):
        print("Ingrese el nombre del jugador", i + 1)
        nombres[i] = str (input ())
    for i in range (x):
        eliminados[i] = False
    borrar_pantalla ()

def juego_cartas (juego):
    global nombres
    global eliminados
    reglas (juego)
    jugadores = int (input ("Ingrese el número de jugadores que van a participar: "))
    asignar_nombres (jugadores)
    asignar_cartas (jugadores)

    for i in range (jugadores-1):
        turno = 0
        cuenta = 0
        while cuenta < 99:
            cuenta = uso_carta (turno, cuenta)
            if cuenta < 99:
                turno = (turno + 1) % jugadores
        print ("Qué lástima")
        print (nombres[turno], "ha perdido")
        print ("Ha sido eliminad@ del juego")
        borrar_pantalla ()
        eliminados[turno] = True

    for i in eliminados.keys():
        if eliminados[i] == False:
            print("¡ENHORABUENA!")
            print("¡", nombres[i], "HA GANADO!")

    print("Fin del juego")
    print("Redirigiendo al catálogo de videojuegos")
    borrar_pantalla ()

def generar_matriz (tupla):
    global tablero
    tablero = {}
    matrizUno = []
    for i in range(8):
        matrizUno.append ([])
        for j in range (8):
            matrizUno[i].append (0)
    matrizDos = []
    for i in range (8):
        matrizDos.append ([])
        for j in range (8):
            matrizDos[i].append (0)
    matrices = (matrizUno, matrizDos)
    for i in range (2):
        tablero[tupla[i]] = matrices [i]

def mostrar_tablero (jugador, matriz):
    print("   1 2 3 4 5 6 7 8")
    print("  +-+-+-+-+-+-+-+-+")
    for i in range (8):
        print(i+1, end = " |")
        for j in range (8):
            print (u"\u2588" if matriz[jugador][i][j] == 1 else " ", end="|")
        print()
    print("  +-+-+-+-+-+-+-+-+")

def barcos (h, matriz, numero):
    mostrar_tablero (h, matriz)
    print("A colocar el barco número", numero + 1)
    barco = int (input ("Barco horizontal (1) o vertical (2)? "))
    if barco == 1:
        fila = int (input("Fila: "))
        columna = int (input("Columna inicio: "))
        while columna > 5:
            print("Dimensiones del barco = 4, no encaja")
            columna = int (input("Columna inicio: "))
        for i in range (4):
            matriz[h][fila - 1][columna - 1 + i] = 1
    if barco == 2:
        columna = int (input("Columna: "))
        fila = int (input("Fila inicio: "))
        while fila > 5:
            print("Dimensiones del barco = 4, no encaja")
            fila = int (input("Fila inicio: "))
        for i in range (4):
            matriz[h][fila - 1 + i][columna - 1] = 1
    mostrar_tablero (h, matriz)
    borrar_pantalla ()

def colocar_barcos (tupla, matriz):
    for h in tupla:
        print("Así se ve el tablero de", h)
        for i in range (4):
            barcos (h, matriz, i)

def revisar_matrices (jugador,matriz):
    contador = []
    for i in range (8):
        for j in range (8):
            if matriz[jugador][i][j] == 1:
                contador.append ("Esto es un valor")
    if len(contador) == 0:
        return False
    else:
        return True

def disparar (jugador, lista, matriz, tupla, turno):
    print("Es el turno de", jugador)
    print("Tu tablero se ve así:")
    mostrar_tablero (jugador, matriz)
    if len(lista[jugador]) > 0:
        print("Casillas ya disparadas (Fila,Columna):")
        print(lista[jugador])
    print("Escoja la casilla a la que va a disparar:")
    fila = int (input ("Fila: "))
    columna = int (input ("Columna: "))
    if matriz[tupla[(turno + 1) % 2]][fila - 1][columna - 1] == 1:
        print("Has dado en el blanco!!!")
    else:
        print("Qué mala suerte, fallaste")
    matriz[tupla[(turno + 1) % 2]][fila - 1][columna - 1] = 0
    lista[jugador].append ((fila, columna))
    borrar_pantalla ()

def astucia_naval (juego):
    global tablero
    reglas (juego)
    plyrOne = str (input ("Nombre del jugador 1: "))
    plyrTwo = str (input ("Nombre del jugador 2: "))
    jugadores = (plyrOne, plyrTwo)
    generar_matriz (jugadores)
    colocar_barcos (jugadores, tablero)

    disparos = {}
    for i in range (2):
        disparos[jugadores[i]] = []

    hayBarcos = True
    while hayBarcos == True:
        for i in jugadores:
            if i == plyrOne:
                turno = 0
            elif i == plyrTwo:
                turno = 1
            hayBarcos = revisar_matrices (plyrTwo, tablero)
            if hayBarcos == True:
                disparar (i, disparos, tablero, jugadores, turno)
        if hayBarcos == True:
            hayBarcos = revisar_matrices (plyrOne, tablero)

    ganadorOne = revisar_matrices (plyrOne, tablero)
    if ganadorOne == True:
        print("ENHORABUENA!!!!")
        print("El jugador", plyrOne, "ha ganado!")
    else:
        print("ENHORABUENA!!!!")
        print("El jugador", plyrTwo, "ha ganado!")

    print("Fin del juego")
    print("Redirigiendo al catálogo de videojuegos")
    borrar_pantalla ()

def catalogo ():
    juego = 0
    while juego != 6:
        print("Bienvenid@ al catálogo de videojuegos")
        print()
        print(" (1) Juego de cartas '99' (2 o más jugadores)")
        print(" (2) Astucia Naval (2 jugadores)")
        print(" (3) - Próximamente disponible -")
        print(" (4) - Próximamente disponible -")
        print(" (5) - Próximamente disponible -")
        print(" (6) Salir del catálogo")
        print()
        juego = int (input ("Ingrese por favor el número de la opción que elige: "))

        if juego == 1:
            print("Juego de cartas '99'")
            juego_cartas (juego)

        elif juego == 2:
            print("Astucia Naval")
            astucia_naval (juego)

        elif juego == 6:
            print("Redirigiendo al menú principal")
            borrar_pantalla ()

        else:
            print("Juego no disponible por el momento")
            print("Prueba con algún otro")
            borrar_pantalla ()

def acerca_de ():
    print("El programa 'Videojuegos con Python' fue creado de cero")
    print("El propósito del programa es el entretenimiento como solución a una problemática actual")
    print("La problemática radica en el aislamiento que existe actualmente a nivel mundial")
    print("Con 'Videojuegos con Python, interuactuar através de un dispositivo es una experiencia diferente")
    print("El entretenimiento es garantizado a pesar de la distancia")
    print("Los juegos incluidos son juegos de mesa presenciales que fueron traducidos a Python3 exitosamente")
    print("Debido a la facilidad de acceso a un computador, el juego está al alcance de cualquiera")
    print("Debido al avance tecnológico, los juegos virtuales se han vuelto una de las principales fuentes de entretenimiento")
    print("El juego del 99 fue la actividad más común entre los creadores del programa antes del aislamiento")
    print("El diseño del juego fue entre los desarrolladores del proyecto y una amplia ayuda del ingeniero Héctor Lasso")
    print("El código de 'Astucia Naval' fue un parcial de programación elaborado por Nicolás Lasso Peña")
    print("A diferencia de la entrega en el parcial, el código fue modificado para optimización y calidad")
    print("Ningún juego fue inventado por los involucrados en el proyecto, solamente el código")
    print("El proyecto le pertenece a Nicolás Lasso Peña y a Santiago González")
    print("Agradecimientos a Juan Camilo Cardona, Ivan Giraldo y Juan David Suarez por compartir con nosotros '99' en la universidad")
    print("Agradecimientos a Héctor Lasso por su valiosa ayuda")
    print("Trabajo presentado a la Universidad Nacional de Colombia para el curso de programación dictado por Juan Diego Escobar")
    print("Versión 1.4.3 del 10 de Julio del 2020")
    x = input ("Presione enter para volver al menú principal")
    print("Redirigiendo al menú principal")
    borrar_pantalla ()


## Cuerpo del código ##
accion = 0
while accion != 3:
    print("VIDEOJUEGOS CON PYTHON")
    print("Bienvenid@ al menú principal")
    print()
    print(" (1) Ver catálogo de videojuegos")
    print(" (2) Acerca de 'Videojuegos con Python'")
    print(" (3) Salir")
    print()
    accion = int (input ("Ingrese por favor el número de la opción que elige: "))
    print("Redirigiendo...")
    borrar_pantalla ()

    if accion == 1:
        catalogo ()

    elif accion == 2:
        acerca_de ()

    elif accion == 3:
        print("Gracias por usar ejecutar mi programa")
        print("Que tengas un excelente día, vuelve pronto")
