import serial, time
import numpy as np
from matplotlib import pyplot as plt
import scipy.signal

inicio = time.time()
datosderecho = list()
datosizquierdo = list()
print("mirar")
n = 1
SampleRate = 0
tiempo = 0
historial = 0



def control():
    global historial
    b, a = scipy.signal.butter(3, 15, fs=450)
    filtrada = scipy.signal.filtfilt(b, a, datosderecho)
    filtNor = list()
    for x in filtrada:
        filtNor.append(30 * (x * 2.134198254645935 - 7.3036616157590695))
    filtNor = np.array(filtNor)
    filnor = -1 * filtNor
    peaks, _ = scipy.signal.find_peaks(filnor, height=15, width=(1, 40))
    Peaks, _ = scipy.signal.find_peaks(filtNor, height=0, width=(1, 40))
    if historial == 0:
        if len(peaks) > 0:
            if len(Peaks) > 0:
                if len(peaks) == len(Peaks):
                    historial = 0
                if len(peaks) > len(Peaks):
                    if len(peaks) ==1 + len(Peaks):
                        print("izquierda")
                        historial = 1
                    else:
                        print("Error")
                        historial = 0
                elif len(Peaks) > len(peaks):
                    print("Posible error")
                    historial = 2
            else:
                print("izquierda")
                historial = 1
        elif len(peaks) == 0 and len(Peaks) == 0:
            print("centrado")
            historial = 0
    elif historial ==1:

        if len(peaks)==0 and len(Peaks)==0:
            print("mantiene")
            historial = 1

        elif len(Peaks)>0:
            if len(peaks)>0:
                print("posible error")
                historial = 2
            elif len(peaks)==0:
                print("se centro")
                historial = 0





ser = serial.Serial("COM6", 9600)
####################reseteo arduino###################################
ser.setDTR(False)
time.sleep(0.5)
ser.flushInput()
ser.setDTR(True)
######################################################################

while True:
    linea = ser.readline().decode("utf-8")
    if linea[0] == "a":
        datosderecho.append(float(linea[2:6]))
    elif linea[0] == "b":
        datosizquierdo.append(float(linea[2:6]))

    final = time.time()
    if final - inicio >= 3:
        control()
        print(historial)
        if historial == 2:
            reseteo = time.time()
            reseteo2 = time.time()
            while reseteo2-reseteo < 3:
                reseteo2 = time.time()
            historial = 0
            print("se reseteo")
        datosderecho = list()
        datosizquierdo = list()
        inicio = time.time()