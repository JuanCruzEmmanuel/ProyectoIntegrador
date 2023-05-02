import pygame, sys, time, serial, scipy.signal
import sqlite3 as sql
from pygame.locals import *
import os.path

from sympy.physics.quantum.cartesian import Px

ser = serial.Serial("COM6", 9600)

####################reseteo arduino###################################
ser.setDTR(False)
time.sleep(0.5)
ser.flushInput()
ser.setDTR(True)
#################################FUNCIONES Y OBJETOS###############################################################
Pw, Ph = 1920, 1080  # tamaño de la pantalla
fps = 120  # Cantaidad de cuadros por segundos


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

        if h > 0:
            v.append(1)

    return len(v), h


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

    return len(v), h


i = BBDD()  # Selecciono el ID


class Derecha(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()
        self.image = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/x2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (3 * (Pw // 4), Ph // 2)

        self.velocidad = 0

    def update(self):
        self.velocidad = 0

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a]:
            self.velocidad = -5
        if teclas[pygame.K_d]:
            self.velocidad = 5

        self.rect.x += self.velocidad


class Izquierda(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/cuadrado.png")

        self.rect = self.image.get_rect()

        self.rect.center = ((Pw // 4), Ph // 2)

        self.velocidad = 0

    def update(self, controlIzquierda):

        self.velocidad = 0
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:
            self.velocidad = 5
        if teclas[pygame.K_d]:
            self.velocidad = -5
        if controlIzquierda == "a":
            self.velocidad = 0.1
        if controlIzquierda =="b":
            self.velocidad = 0
        self.rect.x += self.velocidad




def main():
    conn = sql.connect("Control.db")  # Me conecto a la base de datos

    myCursor = conn.cursor()  # creo un cursor de la base de datos
    myCursor.execute(f"SELECT * FROM Control WHERE ID ={i}")  # Selecciono los valores guardados
    val = myCursor.fetchall()  # SE GUARDA TODOS LOS VALORES EN UNA TUPLA (VD+, VI+, VD-, VI-, CENTRO)
    conn.close()  # SE CIERRA LA BASE DE DATOS
    vnD = [2 / (val[0][0] - val[0][2]), 2 * val[0][4] / (val[0][0] - val[0][2])]  # TENSION NORMALIZADA OJO DERECHO
    vnI = [2 / (val[0][1] - val[0][3]), 2 * val[0][4] / (val[0][1] - val[0][3])]  # TENSION NORMALIZADA OJO IZQUIERDO
    derecho = list()
    derecho_derecho = list()
    izquierdo = list()
    izquierdo_izquierdo = list()
    salto = 1
    xa = 0
    xa2 = 0
    xb = 0
    xb2 = 0
    m = 0
    m2 = 0
    h = 0
    h2 = 0
    pygame.init()
    pantalla = pygame.display.set_mode((Pw, Ph))

    fondo = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/fondo2.png")

    pygame.display.set_caption("Ortooptica")

    derecha = Derecha()

    izquierda = Izquierda()

    while True:
        #################################################
        linea = ser.readline().decode("utf-8")
        if linea[0] == "a":
            derecho.append(float(linea[2:6]))
        elif linea[0] == "b":
            izquierdo.append(float(linea[2:6]))
        else:
            pass

        if len(izquierdo) > 20:
            b, a = scipy.signal.butter(3, 15, fs=450)
            filtrada = scipy.signal.filtfilt(b, a, derecho)
            for x in filtrada:
                derecho_derecho.append(30 * (x * vnD[0] - vnD[1]))
            filtrada2 = scipy.signal.filtfilt(b, a, izquierdo)
            for x in filtrada2:
                izquierdo_izquierdo.append(30 * (x * vnI[0] - vnI[1]))

            # controlDer = analisis2(derecho_derecho, h, xa, xb, m)
            # controlIzq, h2 = analisis(izquierdo_izquierdo, h2, xa2, xb2, m2)

            #####################################################################################
            up = 20
            un = -20
            for xn in range(len(izquierdo_izquierdo)):
                if izquierdo_izquierdo[xn] > up:
                    if xn == 0:
                        xa = xn
                    elif xn == len(izquierdo_izquierdo) - 1:
                        xb = xn
                    else:
                        if izquierdo_izquierdo[xn - 1] > up:
                            if izquierdo_izquierdo[xn + 1] > up:
                                pass
                            else:
                                xba = int((xa + xn) / 2)
                                m = izquierdo_izquierdo[xba]
                                if h == 0:
                                    h = m
                                else:
                                    h = 0
                                    xa = 0
                        else:
                            xa = xn


                elif izquierdo_izquierdo[xn] < un:

                    if xn == 0:
                        xa = xn
                    elif xn == len(izquierdo_izquierdo) - 1:
                        xb = xn
                    else:
                        if izquierdo_izquierdo[xn - 1] < un:
                            if izquierdo_izquierdo[xn + 1] < un:
                                pass
                            else:
                                xb = xn
                                xba = int((xa + xb) / 2)
                                m = izquierdo_izquierdo[xba]
                                if h == 0:
                                    h = m
                                else:
                                    h = 0
                                    xa = 0
                                    xb = 0
                        else:
                            xa = xn

                if h > 0:
                    izquierda.update("a")
                elif h == 0:
                    izquierda.update("b")
                else:
                    izquierda.update("b")

            #####################################################################################

            izquierdo_izquierdo = list()

            derecho = list()
            izquierdo = list()

        #################################################
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(derecha.image, (derecha.rect.x, derecha.rect.y))
        pantalla.blit(izquierda.image, (izquierda.rect.x, izquierda.rect.y))

        derecha.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        pygame.time.Clock().tick(fps)


main()
