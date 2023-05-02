import pygame, sys
from pygame.locals import *
import time
import random
import serial

ser = serial.Serial("COM6", 9600)

####################reseteo arduino###################################
ser.setDTR(False)
time.sleep(0.5)
ser.flushInput()
ser.setDTR(True)
#################################FUNCIONES Y OBJETOS###############################################################

fps = 120

pixelesAncho, pixelesAlto = 1900, 960


class canasta(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/canasta2.png").convert()

        self.rect = self.image.get_rect()

        self.rect.center = (pixelesAncho // 2, pixelesAlto // 1.5)

        self.velocidad_x = 0

    def update(self, vector):

        self.velocidad_x = 0

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a]:
            self.velocidad_x = -10
        if teclas[pygame.K_d]:
            self.velocidad_x = 10
        if vector == 1:
            self.velocidad_x = 10
        if vector == 2:
            self.velocidad_x = -10
        if vector == 0:
            self.velocidad_x = 0

        self.rect.x += self.velocidad_x
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > pixelesAncho:
            self.rect.right = pixelesAncho


class enemigo(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/manzana.png").convert()

        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(pixelesAncho)
        if self.rect.x < 0:
            self.rect.x = 0 + self.rect.width
        elif self.rect.x > pixelesAncho:
            self.rect.x = pixelesAncho - self.rect.width

    def update(self):

        self.rect.y += 3

        if self.rect.bottom > pixelesAlto:
            self.rect.x = random.randrange(pixelesAncho)
            if self.rect.x < 0:
                self.rect.x = 0 + self.rect.width
            elif self.rect.x > pixelesAncho:
                self.rect.x = pixelesAncho - self.rect.width
            self.rect.y = 0


def main():
    pygame.init()

    pantalla = pygame.display.set_mode((pixelesAncho, pixelesAlto))
    pygame.display.set_caption("Agarra Frutas")
    sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()
    manzana = enemigo()
    miCanasta = canasta()
    sprites.add(miCanasta)
    enemigos.add(manzana)
    bandera = 0
    vector = 0
    while True:
        linea = ser.readline().decode("utf-8")
        if linea != " " or linea != "":
            linea = float(linea)  # se convierte los valores en punto flotante
            if linea >= 4:  # Se evalua si existe pulso positivo
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

            if linea <= 2.8:
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

            if linea < 3.550 and linea > 3.450:

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

        miCanasta.update(vector)
        enemigos.update()
        colision = pygame.sprite.spritecollide(miCanasta, enemigos, False)
        if colision:
            manzana.rect.x = random.randrange(pixelesAncho)
            if manzana.rect.x < 0:
                manzana.rect.x = 0 + manzana.rect.width
            elif manzana.rect.x > pixelesAncho:
                manzana.rect.x = pixelesAncho - manzana.rect.width
            manzana.rect.y = 0

        pantalla.fill((0, 0, 0))
        sprites.draw(pantalla)
        enemigos.draw(pantalla)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()  # comando necesario para actualizar
        pygame.time.Clock().tick(fps)


main()
