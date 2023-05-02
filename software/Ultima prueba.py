# ---------------------------------------------------------------------------------------------
# Imports and Inits

import sys
import threading
import serial, pygame, time
import sqlite3 as sql
import scipy.signal
from pygame.locals import *

"""-------------------------------Variables Globales-----------------------------------"""


Pw, Ph = 1920, 1080  # tamaño de la pantalla
fps = 120  # Cantaidad de cuadros por segundos
glob = 0
glob2 = 0
xad = 0
xai = 0
up = 15
un = -15
xb = 0
xbi = 0
m = 0
m2 = 0
hd = 0  # Historial, me va a determinar que valor usar
hi = 0
reset = "no"
funcionando = str()
b, a = scipy.signal.butter(3, 15, fs=450)  # Mis variables de filtrado
derecho = list()
izquierdo = list()
derecho_derecho = list()
izquierdo_izquierdo = list()

ser = serial.Serial("COM6", 9600)

####################reseteo arduino###################################

ser.setDTR(False)
time.sleep(0.5)
ser.flushInput()
ser.setDTR(True)

"""---------------------------------------------FUNCIONES----------------------------------------------"""


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
            l.append(1)
    return len(l), h


def analisis2(sig, h, xa, xb, m):
    global reset
    up = 3
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

    return len(v),h


def lectura():
    global glob, glob2, xad, xai, hd, hi, xb, \
        xbi, derecho, derecho_derecho, \
        izquierdo, izquierdo_izquierdo, m, m2, funcionando, reset
    while True:
        linea = ser.readline().decode("utf-8")
        if linea[0] == "a":
            derecho.append(float(linea[2:6]))
        elif linea[0] == "b":
            izquierdo.append(float(linea[2:6]))

        finaliza = time.time()
        if finaliza - empieza > 3 and 3.1 > finaliza-empieza:
            funcionando = "OK"
            derecho = list()
            izquierdo = list()

        if funcionando == "OK":
            if len(derecho) > 20:
                filtrada = scipy.signal.filtfilt(b, a, derecho)
                for x in filtrada:
                    derecho_derecho.append(30 * (x * vnD[0] - vnD[1]))
                filtrada = scipy.signal.filtfilt(b, a, izquierdo)
                for x in filtrada:
                    izquierdo_izquierdo.append(30 * (x * vnI[0] - vnI[1]))
                glob, hd = analisis2(derecho_derecho, hd, xad, xb, m)
                glob2, hi = analisis2(izquierdo_izquierdo, hi, xai, xbi, m2)

                derecho = list()
                izquierdo = list()
                derecho_derecho = list()
                izquierdo_izquierdo = list()


def BBDD():  # Base de datos

    conn = sql.connect("Control.db")
    print("Se conecto a la BBDD")

    cursor = conn.cursor()
    cursor.execute("select nombre,indice from sujeto")

    datos = cursor.fetchall()
    for persona in datos:
        print(persona)

    cursor.close()
    conn.close()

    id = int(input("Ingrese el sujeto_ID "))

    for persona in datos:
        if id == persona[1]:
            print("seleccion a ", persona[0])
    return id


"""--------------------------------------------CLASS----------------------------------------------------"""


class Derecha(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()
        self.image = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/x2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (3 * (Pw // 4), Ph // 2)

        self.velocidad = 0

    def update(self, varGlob):
        self.velocidad = 0

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a]:
            self.velocidad = -5
        if teclas[pygame.K_d]:
            self.velocidad = 5

        self.rect.x += self.velocidad
        self.rect.x -= 0.05 * varGlob


class Izquierda(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/cuadrado.png")

        self.rect = self.image.get_rect()

        self.rect.center = ((Pw // 4), Ph // 2)

        self.velocidad = 0

    def update(self, varGlob):

        self.velocidad = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:
            self.velocidad = 5
        if teclas[pygame.K_d]:
            self.velocidad = -5
        self.rect.x += self.velocidad
        self.rect.x += 0.05 * varGlob


# -----------------------------------------------------------------------------------------------------------
# Empiza el programa

i = BBDD()  # Selecciono el ID

conn = sql.connect("Control.db")  # Me conecto a la base de datos

myCursor = conn.cursor()  # creo un cursor de la base de datos
myCursor.execute(f"SELECT * FROM Control WHERE ID ={i}")  # Selecciono los valores guardados
val = myCursor.fetchall()  # SE GUARDA TODOS LOS VALORES EN UNA TUPLA (VD+, VI+, VD-, VI-, CENTRO)
conn.close()  # SE CIERRA LA BASE DE DATOS
vnD = [2 / (val[0][0] - val[0][2]), 2 * val[0][4] / (val[0][0] - val[0][2])]  # TENSION NORMALIZADA OJO DERECHO
vnI = [2 / (val[0][1] - val[0][3]), 2 * val[0][4] / (val[0][1] - val[0][3])]
empieza = time.time()
t = threading.Thread(target=lectura)
t.daemon = True
t.start()

# -----------------------------------------------------------------------------------------------------------

# Codigo del juego en si mismo
pygame.init()

pantalla = pygame.display.set_mode((Pw, Ph))

fondo = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/fondo2.png")

pygame.display.set_caption("Ortooptica")

derecha = Derecha()  # Se crea el objeto que mueve el ojo derecho

izquierda = Izquierda()  # Se crea el objeto que mueve el ojo izquierdo

while True:

    pantalla.blit(fondo, (0, 0))
    pantalla.blit(derecha.image, (derecha.rect.x, derecha.rect.y))
    pantalla.blit(izquierda.image, (izquierda.rect.x, izquierda.rect.y))
    derecha.update(glob)
    izquierda.update(glob2)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    pygame.time.Clock().tick(fps)
