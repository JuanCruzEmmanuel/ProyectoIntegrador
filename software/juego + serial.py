import serial
import time
import pygame, sys
from pygame.locals import *
import random

ser = serial.Serial("COM3", 9600)  # se estable conexion

####################reseteo arduino###################################
ser.setDTR(False)
time.sleep(0.5)
ser.flushInput()
ser.setDTR(True)
#################################FUNCIONES Y OBJETOS###############################################################

def AnalisisTiempoReal(linea, bandera):
    if linea >= 3.8:  # Se evalua si existe pulso positivo
        if bandera == 0:
            vector = 1
            bandera = 1
            return vector, bandera

        elif bandera == 1:
            vector = 1
            bandera = 1
            return vector, bandera


        elif bandera == 2:
            vector = 0
            bandera = 4
            return vector, bandera

        elif bandera == 4:
            vector = 0
            bandera = 4
            return vector, bandera

    if linea <= 3.2:
        if bandera == 0:
            vector = 2
            bandera = 2
            return vector, bandera

        if bandera == 2:
            vector = 2
            bandera = 2
            return vector, bandera



        elif bandera == 1:
            vector = 0
            bandera = 3
            return vector, bandera

        elif bandera == 3:

            vector = 0
            bandera = 3
            return vector, bandera

    if linea > 3.3 and linea < 3.7:
        if bandera == 0:  # no se realiza movimiento ocular
            vector = 0
            bandera = 0
            return vector, bandera



        elif bandera == 1:  # se encuentra en la meseta del pico positivo
            vector = 1
            bandera = 1
            return vector, bandera



        elif bandera == 2:  # se encuentra en la meseta del pico negativo
            vector = 2
            bandera = 2
            return vector, bandera


        elif bandera == 3:  # se resetea el positivo
            vector = 0
            bandera = 0

            return vector, bandera

        elif bandera == 4:  # se resetea el negativo
            vector = 0
            bandera = 0
            return vector, bandera

    return vector, bandera


class barra(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # En este objeto, se le asocia de manera directa esta imagen
        self.imagen = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/barra.png").convert_alpha()
        # las dimensiones son:
        self.ancho, self.alto = self.imagen.get_size()
        # posiciones de la barra :
        self.x = pxw / 2 - self.ancho / 2
        self.y = pxh - self.alto / 2 - 20

        self.dirx = 0

    def mover(self):
        self.x += self.dirx
        if self.x <= 0:
            self.x = 0
        if self.x + self.ancho >= pxw:
            self.x = pxw - self.ancho

    def golpear(self, pelota):
        if (
                pelota.x <= self.x + self.ancho
                and pelota.x >= self.x
                and pelota.y + pelota.alto >= self.y
                and pelota.y <= self.y + self.alto
        ):
            pelota.y = self.y - self.alto - 5
            pelota.diry = - pelota.diry
            pygame.mixer.Sound("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/sonido1.mp3.mp3").play()

class pelota(pygame.sprite.Sprite):

    def __init__(self, fichero):
        super().__init__()
        self.imagen = pygame.image.load(fichero).convert_alpha()

        self.ancho, self.alto = self.imagen.get_size()
        self.rect = self.imagen.get_rect()
        self.x = pxw / 2 - self.ancho / 2
        self.y = pxh / 2 - self.alto / 2

        self.dirx = random.choice([-5, 5])
        self.diry = random.choice([-5, 5])

        self.final = 0

    def mover(self):
        self.x += self.dirx
        self.y += self.diry

    def rebotar(self):
        if self.x <= 0:
            self.dirx = -self.dirx
        if self.x + self.ancho >= pxw:
            self.dirx = -self.dirx
        if self.y <= 0:
            self.diry = -self.diry
        if self.y + self.alto >= pxh:
            self.final += 1

class bloque(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.imagen = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/bloque.png").convert_alpha()

        self.ancho, self.alto = self.imagen.get_size()

        self.x = 0
        self.y = 0

    def colision(self, pelota):
        if (
                pelota.x <= self.x + self.ancho
                and pelota.x >= self.x
                and self.alto > pelota.y
        ):
            pelota.y = self.alto + 5
            pelota.diry = - pelota.diry

            self.imagen = pygame.Surface((0, 0))
            self.ancho = 0
            self.alto = 0


##############################SECCION DE VARIABLES GLOBALES#################################################
bandera = 0
vector = 0
pxw,pxh = 564,1003
fps = 45
############################################################################################################


def main():
    bandera = 0
    vector = 0
    pxw, pxh = 564, 1003
    fps = 60
    pygame.init()
    enemigos = pygame.sprite.Group()  # Creo esto para que todos los bloques tengan las mismas propiedades
    pantalla = pygame.display.set_mode((pxw, pxh))
    #################################FONDO

    fondo = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/fondo1.jpg")

    ###########################pelota

    pelota1 = pelota("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/bola.png")
    barra1 = barra()
    bloque1 = bloque()
    bloque2 = bloque()
    bloque2.x = bloque1.x + bloque1.ancho
    bloque3 = bloque()
    bloque3.x = bloque2.x + bloque2.ancho
    bloque4 = bloque()
    bloque4.x = bloque3.x + bloque3.ancho

    enemigos.add(bloque1)
    pygame.display.set_caption("Juego 1")

    gameover = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/gameover.png")

    while True:
        linea = ser.readline().decode("utf-8")
        if linea != " " or linea != "":
            linea = float(linea)  # se convierte los valores en punto flotante
            if linea >= 3.85:  # Se evalua si existe pulso positivo
                if bandera == 0:
                    vector = 1
                    bandera = 1


                elif bandera == 1:
                    vector = 1
                    bandera = 1



                elif bandera == 2:
                    vector = 0
                    bandera = 4


                elif bandera == 4:
                    vector = 0
                    bandera = 4

            if linea <= 3.1:
                if bandera == 0:
                    vector = 2
                    bandera = 2

                if bandera == 2:
                    vector = 2
                    bandera = 2




                elif bandera == 1:
                    vector = 0
                    bandera = 3


                elif bandera == 3:

                    vector = 0
                    bandera = 3

            if linea < 3.60 and linea > 3.40:

                if bandera == 0:  # no se realiza movimiento ocular
                    vector = 0
                    bandera = 0






                elif bandera == 1:  # se encuentra en la meseta del pico positivo
                    vector = 1
                    bandera = 1




                elif bandera == 2:  # se encuentra en la meseta del pico negativo
                    vector = 2
                    bandera = 2



                elif bandera == 3:  # se resetea el positivo
                    vector = 0
                    bandera = 0



                elif bandera == 4:  # se resetea el negativo
                    vector = 0
                    bandera = 0

        print(linea,bandera)
        pelota1.mover()
        pelota1.rebotar()
        barra1.mover()
        barra1.golpear(pelota1)
        bloque1.colision(pelota1)
        bloque2.colision(pelota1)
        bloque3.colision(pelota1)
        bloque4.colision(pelota1)
        pantalla.blit(fondo, (0, 0))
        pantalla.blit(pelota1.imagen, (pelota1.x, pelota1.y))
        pantalla.blit(barra1.imagen, (barra1.x, barra1.y))
        pantalla.blit(bloque1.imagen, (bloque1.x, bloque1.y))
        pantalla.blit(bloque2.imagen, (bloque2.x, bloque2.y))
        pantalla.blit(bloque3.imagen, (bloque3.x, bloque3.y))
        pantalla.blit(bloque4.imagen, (bloque4.x, bloque4.y))
        if pelota1.final >= 1:
            pantalla.blit(gameover, (0, pxh / 2))

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    barra1.dirx = 10  # velocidad de movimiento
                if event.key == pygame.K_a:
                    barra1.dirx = -10

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    barra1.dirx = 0
                if event.key == pygame.K_a:
                    barra1.dirx = 0

        if vector == 0:
            barra1.dirx = 0

        if vector == 1:
            barra1.dirx = 5

        if vector == 2:
            barra1.dirx = -5




        pygame.display.update()  # comando necesario para actualizar
        pygame.time.Clock().tick(fps)

main()











