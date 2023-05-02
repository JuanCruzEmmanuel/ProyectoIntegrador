import sqlite3 as sql
import serial, time
import scipy.signal
import numpy as np


def crearBD():
    conn = sql.connect("Control.db")
    conn.commit()
    conn.close()


def crearTabla():
    conn = sql.connect("Control.db")
    cursor = conn.cursor()
    cursor.execute(

        """CREATE TABLE sujeto( 
                    nombre text, 
                    apellido text, 
                    edad text, 
                    indice integer
                    ) """
    )
    conn.commit()
    conn.close()


def insertarFila(nombre, apellido, edad, indice):
    conn = sql.connect("Control.db")
    cursor = conn.cursor()
    instruccion = f"INSERT INTO sujeto VALUES ('{nombre}','{apellido}','{edad}',{indice})"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()


def subir():
    ser = serial.Serial("COM6", 9600)
    ####################reseteo arduino###################################

    ser.setDTR(False)
    time.sleep(0.5)
    ser.flushInput()
    ser.setDTR(True)

    muestra = list()

    n, n2, n3 = 3, 3, 3
    datosderecho = list()
    datosizquierdo = list()
    cen = list()
    v30D = list()
    v30I = list()
    vn30D = list()
    vn30I = list()
    print("centrado")
    inicio = time.time()
    while n != 0:
        linea = ser.readline().decode("utf-8")
        # print(linea)
        if linea[0] == "a":
            datosderecho.append(float(linea[2:6]))
        elif linea[0] == "b":
            datosizquierdo.append(float(linea[2:6]))
        final = time.time()
        if final - inicio >= 2:
            b, a = scipy.signal.butter(3, 15, fs=450)
            filtrada = scipy.signal.filtfilt(b, a, datosderecho)
            cen.append(np.mean(filtrada))
            datosderecho = list()
            datosizquierdo = list()
            n -= 1
            inicio = time.time()
    inicio = time.time()
    print("mirar a 30°")
    while n2 != 0:
        linea = ser.readline().decode("utf-8")
        if linea[0] == "a":
            datosderecho.append(float(linea[2:6]))
        elif linea[0] == "b":
            datosizquierdo.append(float(linea[2:6]))
        final = time.time()
        if final - inicio >= 3:
            b, a = scipy.signal.butter(3, 15, fs=450)

            filtrada = scipy.signal.filtfilt(b, a, datosderecho)
            filtrada2 = scipy.signal.filtfilt(b, a, datosizquierdo)
            v30D.append(max((filtrada)))
            v30I.append(max(filtrada2))
            datosderecho = list()
            datosizquierdo = list()
            n2 -= 1
            print("mirar a 30°")
            inicio = time.time()

    inicio = time.time()
    print("mirar a -30°")
    while n3 != 0:
        linea = ser.readline().decode("utf-8")
        if linea[0] == "a":
            datosderecho.append(float(linea[2:6]))
        elif linea[0] == "b":
            datosizquierdo.append(float(linea[2:6]))
        final = time.time()
        if final - inicio >= 3:
            b, a = scipy.signal.butter(3, 15, fs=450)

            filtrada = scipy.signal.filtfilt(b, a, datosderecho)
            filtrada2 = scipy.signal.filtfilt(b, a, datosizquierdo)
            vn30D.append(min((filtrada)))
            vn30I.append(min(filtrada2))
            datosderecho = list()
            datosizquierdo = list()
            n3 -= 1
            inicio = time.time()
            print("mirar a -30°")

    conn = sql.connect("Control.db")
    cursor = conn.cursor()
    i = 1
    instruccion = f"INSERT INTO Control VALUES ({np.mean(v30D)},{np.mean(v30I)},{np.mean(vn30D)},{np.mean(vn30I)},{np.mean(cen)},{i})"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

    ser.close()


if __name__ == "__main__":
    # crearBD()
    # crearTabla()
    #insertarFila("Gustavo", "Albornoz", "26", 2)
    subir()
