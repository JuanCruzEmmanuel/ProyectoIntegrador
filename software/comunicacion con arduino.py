# -*- coding: utf-8 -*-
"""
Created on Wed May 11 01:13:23 2022

@author: juanc
"""

"""En esta seccion de codigo se vera la conexion via serie con arduino"""

import serial.tools.list_ports
import matplotlib.pyplot as plt
import numpy as np

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portList = []
"""lo que busco hacer en esta seccion es poder ver todos los puertos
    disponibles y que hay en cada uno de estos"""
    
    
for puertos in ports:
    portList.append(str(puertos))
    print(str(puertos))
    
    
"""Al crear esta variable, yo decido mediante consola cual puerto voy a
    usar en funcion a mis necesidades"""
    
selPuerto = input("seleccionar el puerto COM")

for puntero in range(0, len(portList)):
    if portList[puntero].startswith("COM"+str(selPuerto)):
        puerto = "COM"+str(selPuerto)

"""Abro el puerto con los valores seleccionados"""
                  

serialInst.baudrate = 9600
serialInst.port = puerto
# serialInst.timeout = 1
serialInst.open()

while True:
        
    if serialInst.in_waiting:
        
        linea = serialInst.readline().decode("utf-8").rstrip("\n\r")
        print(linea)
        
serial.Serial("puerto",9600).close()       
exit()

    
                  




        

        



