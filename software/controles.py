import numpy as np
import serial, time
import sqlite3 as sql
import scipy.signal


def BBDD():
    conn = sql.connect("Control.db")
    print("Se conecto a la BBDD")

    cursor = conn.cursor()
    cursor.execute("select nombre,indice from sujeto")

    datos = cursor.fetchall()
    for persona in datos:
        print(persona)

    cursor.close()
    conn.close()

    i = int(input("Ingrese el sujeto_ID "))

    for persona in datos:
        if i == persona[1]:
            print("seleccion a ", persona[0])
    return i


def analisis(sig, h, xa, xb, m):
    up = 20
    un = -20
    l = list()
    for xn in range(len(sig)):
        if sig[xn] > up:
            if xn == 0:
                xa = xn
            elif xn == len(sig) - 1:
                xb = xn
            else:
                if sig[xn - 1] > up:
                    if sig[xn + 1] > up:
                        pass
                    else:
                        xb = xn
                        xba = int((xa + xb) / 2)
                        m = sig[xba]
                        if h == 0:
                            h = m
                        else:
                            h = 0
                            xa = 0
                            xb = 0
                else:
                    xa = xn


        elif sig[xn] < un:

            if xn == 0:
                xa = xn
            elif xn == len(sig) - 1:
                xb = xn
            else:
                if sig[xn - 1] < un:
                    if sig[xn + 1] < un:
                        pass
                    else:
                        xb = xn
                        xba = int((xa + xb) / 2)
                        m = sig[xba]
                        if h == 0:
                            h = m
                        else:
                            h = 0
                            xa = 0
                            xb = 0
                else:
                    xa = xn
        if h > 0:
            print(1)
        elif h== 0:
            print(0)
        else:
            print(0)


def n(h):
    if h == 0:
        print(0)
    elif h > 0:
        print(1)
    else:
        print(0)


def analisis2(sig, h, xa, xb, m):
    up = 15
    un = -15
    v = list()
    for xn in range(len(sig)):
        if sig[xn] > up:
            if xn == 0:
                xa = xn
            elif xn == len(sig) - 1:
                xb = xn
            else:
                if sig[xn - 1] > up:
                    if sig[xn + 1] > up:
                        pass
                    else:
                        xb = xn
                        xba = int((xa + xb) / 2)
                        m = sig[xba]
                        if h == 0:
                            h = m
                        else:
                            h = 0
                            xa = 0
                            xb = 0
                else:
                    xa = xn


        elif sig[xn] < un:

            if xn == 0:
                xa = xn
            elif xn == len(sig) - 1:
                xb = xn
            else:
                if sig[xn - 1] < un:
                    if sig[xn + 1] < un:
                        pass
                    else:
                        xb = xn
                        xba = int((xa + xb) / 2)
                        m = sig[xba]
                        if h == 0:
                            h = m
                        else:
                            h = 0
                            xa = 0
                            xb = 0
                else:
                    xa = xn
        elif h < 0:
            v.append(1)



def control():
    ser = serial.Serial("COM6", 9600)
    ####################reseteo arduino###################################
    ser.setDTR(False)
    time.sleep(0.5)
    ser.flushInput()
    ser.setDTR(True)
    conexion = True
    i = BBDD()  # Selecciono el ID

    conn = sql.connect("Control.db")  # Me conecto a la base de datos

    myCursor = conn.cursor()  # creo un cursor de la base de datos
    myCursor.execute(f"SELECT * FROM Control WHERE ID ={i}")  # Selecciono los valores guardados
    val = myCursor.fetchall()  # SE GUARDA TODOS LOS VALORES EN UNA TUPLA (VD+, VI+, VD-, VI-, CENTRO)
    conn.close()  # SE CIERRA LA BASE DE DATOS
    vnD = [2 / (val[0][0] - val[0][2]), 2 * val[0][4] / (val[0][0] - val[0][2])]  # TENSION NORMALIZADA OJO DERECHO
    vnI = [2 / (val[0][1] - val[0][3]), 2 * val[0][4] / (val[0][1] - val[0][3])]  # TENSION NORMALIZADA OJO IZQUIERDO
    print(vnD, vnI)
    derecho = list()
    derecho_derecho = list()
    izquierdo = list()
    izquierdo_izquierdo = list()
    l = list()
    print("Mirar")
    salto = 1
    xa = 0
    xa2 = 0
    xb = 0
    xb2 = 0
    m = 0
    m2 = 0
    h = 0
    h2 = 0
    controlIzq = 0
    controlDer = 0
    inicio = time.time()

    while conexion:
        linea = ser.readline().decode("utf-8")
        if linea[0] == "a":
            derecho.append(float(linea[2:6]))
        elif linea[0] == "b":
            izquierdo.append(float(linea[2:6]))
        else:
            pass

        final = time.time()

        if final - inicio >= 1:
            if salto != 1:
                b, a = scipy.signal.butter(3, 15, fs=450)
                filtrada = scipy.signal.filtfilt(b, a, derecho)
                for x in filtrada:
                    derecho_derecho.append(30 * (x * vnD[0] - vnD[1]))
                filtrada2 = scipy.signal.filtfilt(b, a, izquierdo)
                for x in filtrada2:
                    izquierdo_izquierdo.append(30 * (x * vnI[0] - vnI[1]))

            # analisis(derecho_derecho, h, xa, xb, m)
            analisis(izquierdo_izquierdo, h2, xa2, xb2, m2)
            #print(controlIzq)
            # print(h2)
            izquierdo_izquierdo = list()
            salto = 0
            derecho = list()
            izquierdo = list()
            inicio = time.time()




entrar = input("¿ Desea entrar ? s/n ")
while entrar != "n":
    control()
    entrar = input("¿ Desea entrar ? s/n ")

print("salio")
