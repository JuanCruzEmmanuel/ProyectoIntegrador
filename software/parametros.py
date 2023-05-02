# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 21:41:32 2022

@author: juanc
"""

########Prueba de media, y longitud

import serial
import time
from matplotlib import pyplot as plt
import numpy as np

ser = serial.Serial("COM6",9600)

####################reseteo arduino###################################
ser.setDTR(False)
time.sleep(0.5)
ser.flushInput()
ser.setDTR(True)
x=3
x2=3
x3 = 3
datos = list()
var = list()
maximo = list()
minimo = list()
lineaBase = list()
ancho = list()
ancho2 = list()
tiempo = time.time()
while True: 
    print("mantengase fijo")
    while x3!=0:
        linea = ser.readline().decode("utf-8")
        if linea != " ":
            datos.append(float(linea))
            final = time.time()
            if final - tiempo >=1:
                lineaBase.append(sum(datos)/len(datos))
                x3 -=1
                tiempo= time.time()
                datos=list()
    print("Mirar derecha")
    while x!=0:
        linea = ser.readline().decode("utf-8")
        if linea != " ":
            datos.append(float(linea))
            final = time.time()
            if final - tiempo >=1.5:
                print("mirar Derecha")
                maximo.append(max(datos))
                x -=1
            
                tiempo= time.time()
                var =[x for x in datos if x > (sum(lineaBase)/len(lineaBase)+0.1*sum(lineaBase)/len(lineaBase))]
                ancho.append(len(var))
                datos=list()
    print("mirar izquierda")
    while x2!=0:
        linea = ser.readline().decode("utf-8")
        if linea != " ":
            datos.append(float(linea))
            final = time.time()
            if final - tiempo >=1.5:
                print("mirar Izquierda")
                minimo.append(min(datos))
                x2 -= 1
                tiempo = time.time()
                datos = list()
    break


print(maximo,"el promedio es ",sum(maximo)/len(maximo))
print(minimo,"el promedio es ",sum(minimo)/len(minimo))
print(ancho)
print("linea base es: ", sum(lineaBase)/len(lineaBase))

ser.close()    
        