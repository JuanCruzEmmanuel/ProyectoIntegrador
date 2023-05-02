# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 02:33:45 2022

@author: juanc
"""

import serial, time
import numpy as np
from matplotlib import pyplot as plt
import scipy.signal
from scipy.interpolate import interp1d


ser = serial.Serial("COM6", 9600)
####################reseteo arduino###################################
ser.setDTR(False)
time.sleep(0.5)
ser.flushInput()
ser.setDTR(True)
######################################################################
inicio = time.time()
datosderecho = list()
datosizquierdo = list()
print("mirar")
n = 1
SampleRate = 0
tiempo = 0
while True:
    linea = ser.readline().decode("utf-8")
    if linea[0] == "a":
        datosderecho.append(float(linea[2:6]))
    elif linea[0] == "b":
        datosizquierdo.append(float(linea[2:6]))

    final = time.time()
    if final - inicio >= 10:
        tiempo = final-inicio
        break

ser.close()
b,a = scipy.signal.butter(3, 15, fs=450)
filtrada = scipy.signal.filtfilt(b, a, datosderecho)
filtNor = list()
filtrada2 = scipy.signal.filtfilt(b, a, datosizquierdo)
for x in filtrada:
    filtNor.append(30*(x*2.134198254645935-7.3036616157590695))
filtNor = np.array(filtNor)
filnor = -1*filtNor
x = np.linspace(0,len(filtNor),len(filtNor))
x3 = np.linspace(1,len(datosderecho),len(datosderecho))
x4 =np.linspace(1,len(datosizquierdo),len(datosizquierdo))
x2 = np.linspace(1,len(filtrada2),len(filtrada2))
peaks, _ = scipy.signal.find_peaks(filnor, height=15,width=(1,40))
Peaks, _ = scipy.signal.find_peaks(filtNor, height=0,width=(1,40))
#plt.ylim(-100,100)
#plt.plot(x, filtNor, label = "Derecho")
#plt.plot(peaks, filtNor[peaks], "x")
#plt.plot(Peaks, filtNor[Peaks], "o")
plt.plot(x3,datosderecho,"g",label = "Derecha")
#plt.plot(x4,datosizquierdo,"red",label = "Izquierda")
if len(peaks)>0:
    print("no esta vacia")
else:
    print("Vacia mi viejo")

print(max(datosderecho),min(datosderecho))
#plt.plot(x2,filtrada2,label = "izquierdo")
plt.legend()
plt.show()

ser.close()


    