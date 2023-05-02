import pygame, sys, random, time, serial, threading
from pygame.locals import *
from button import Button

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

# variables globales
fps = 60
pixelesAncho, pixelesAlto = 1900, 960
SCREEN = pygame.display.set_mode((1900, 960))
pygame.display.set_caption("Menu")
col = 0
BG = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/fondo2.png").convert()
aux = 1
pygame.init()

font = pygame.font.Font("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/font.ttf", 32)
font2 = pygame.font.Font("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/font.ttf", 180)
umbral1 = 4.1
umbral3 = 3.35
umbral2sup = 3.9
umbral2inf = 3.5
umbCent = list()
umbDer = list()
umbIzq = list()
start = 0
funcionando = str()
flag = 0
sgn = "cen"
reseteo = "no"
amedir = "pass"


def control(lista):
   global flag, sgn, umbral3, umbral1, umbral2inf, umbral2sup, reseteo
   if reseteo == "no":
       if flag == 0:

           if max(lista) >= max(umbDer)-0.1*max(umbDer):
               if min(lista) > min(umbIzq)+0.1*min(umbIzq):
                   flag = 1
                   sgn = "der"
               else:
                   flag = 0
                   sgn = "cen"
           elif min(lista) <= min(umbIzq)+0.1*min(umbIzq):
               if max(lista) < max(umbDer)-0.1*max(umbDer):
                   flag = 2
                   sgn = "izq"
               else:
                   flag = 0
                   sgn = "cen"
           else:
               flag = 0
               sgn = "cen"

       elif flag == 1:

           if max(lista) <= umbral2sup:
               if umbral2inf <= min(lista):
                   flag = 1
                   sgn = "der"
           elif max(lista) > max(umbDer)-0.1*max(umbDer):
               flag = 0
               sgn = "cen"
               reseteo ="si"
           elif min(lista) < min(umbIzq)+0.1*min(umbIzq):
               flag = 0
               sgn = "cen"
               reseteo ="si"

       elif flag == 2:

           if max(lista) <= umbral2sup:
               if umbral2inf <= min(lista):
                   flag = 2
                   sgn = "izq"
           elif max(lista) > max(umbDer)-1*max(umbDer):
               flag = 0
               sgn = "cen"
               reseteo ="si"

           elif min(lista) < min(umbIzq)+0.1*min(umbIzq):
               flag = 0
               sgn = "cen"
               reseteo = "si"

   elif reseteo == "si":
       reseteo = "no"
       sgn = "cen"
       flag = 0


def lectura():
   global derecho, derecho_derecho, izquierdo, izquierdo_izquierdo, funcionando,umbCent,umbDer,umbIzq

   while True:
       while amedir == "centrado":
           linea = ser.readline().decode("utf-8")
           if linea[0] == "a":
               umbCent.append(float(linea[2:6]))
       while amedir == "derecha":
           linea = ser.readline().decode("utf-8")
           if linea[0] == "a":
               umbDer.append(float(linea[2:6]))
       while amedir == "izquierda":
           linea = ser.readline().decode("utf-8")
           if linea[0] == "a":
               umbIzq.append(float(linea[2:6]))

       while amedir == "pass":
           pass


       while amedir == "none":
           linea = ser.readline().decode("utf-8")
           if linea[0] == "a":
               derecho.append(float(linea[2:6]))
           elif linea[0] == "b":
               izquierdo.append(float(linea[2:6]))

           if len(derecho) > 60:
               control(derecho)

               derecho = list()
               izquierdo = list()
               derecho_derecho = list()
               izquierdo_izquierdo = list()


def get_font(size):  # Regresa el presionar start para commentary
   return pygame.font.Font("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/font.ttf", size)


def show_score(i):
   score = font.render("Score :" + str(i), True, (255, 255, 255))
   SCREEN.blit(score, (50, 50))


def Countdown(tiempo):
   if tiempo >= 0:
       conteo = font2.render(str(tiempo), True, (255, 255, 255))
       SCREEN.blit(conteo, (1600 / 2, 800 / 2))
   else:
       pass


def circulos_pantalla_calibracion():
   global aux, amedir
   t = 5
   sprites = pygame.sprite.Group()
   circulo = calibracion()
   sprites.add(circulo)
   while True:
       if circulo.start == 0:
           if t > -2:
               SCREEN.blit(BG, (0, 0))
               Countdown(t)
               tiempo = int(pygame.time.get_ticks() / 1000)
               if aux == tiempo:
                   t = 5 - (aux - 1)
                   aux += 1
           else:
               if circulo.mesure == "centrada":
                   amedir = "centrado"
               elif circulo.mesure == "derecha":
                   amedir = "derecha"
               elif circulo.mesure == "izquierda":
                   amedir = "izquierda"
               SCREEN.blit(BG, (0, 0))
               circulo.update()
               sprites.draw(SCREEN)
       else:
           jugar()
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()

       pygame.display.flip()  # comando necesario para actualizar


class canasta(pygame.sprite.Sprite):

   def __init__(self):

       super().__init__()

       self.image = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/canasta2.png").convert()

       self.rect = self.image.get_rect()

       self.rect.center = (pixelesAncho // 2, pixelesAlto // 1.5)

       self.velocidad_x = 0

   def update(self, sig):

       self.velocidad_x = 0

       teclas = pygame.key.get_pressed()

       if teclas[pygame.K_a]:
           self.velocidad_x = -10
       if teclas[pygame.K_d]:
           self.velocidad_x = 10
       if sig == "der":
           self.velocidad_x = 4
       if sig == "izq":
           self.velocidad_x =-4
       if sig == "cen":
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

       self.rect.y += 1.5

       if self.rect.bottom > pixelesAlto:
           self.rect.x = random.randrange(pixelesAncho)
           if self.rect.x < 0:
               self.rect.x = 0 + self.rect.width
           elif self.rect.x > pixelesAncho:
               self.rect.x = pixelesAncho - self.rect.width
           self.rect.y = 0


class calibracion(pygame.sprite.Sprite):
   def __init__(self):

       super().__init__()

       self.image = pygame.image.load(
           "C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/circulo_calibracion.png").convert_alpha()
       self.rect = self.image.get_rect()
       self.rect.center = (900, 400)
       self.a = 0
       self.start = 0
       self.mesure = "centrada"

   def update(self):

       ti = pygame.time.Clock().tick(100)
       if ti > 9:
           self.a += 1
       if self.a == 500:
           self.rect.x += 800
           self.mesure = "derecha"
       elif self.a == 1000:
           self.rect.x -= 700
           self.mesure = "derecha"
       elif self.a == 1500:
           self.rect.x -= 700
           self.mesure = "izquierda"
       elif self.a == 2000:
           self.start = 1
           self.mesure = "none"


def jugar():
   global amedir
   pantalla = pygame.display.set_mode((pixelesAncho, pixelesAlto))
   pygame.display.set_caption("Lateralidad- Albornoz y Noya")
   sprites = pygame.sprite.Group()
   enemigos = pygame.sprite.Group()
   manzana = enemigo()
   miCanasta = canasta()
   sprites.add(miCanasta)
   enemigos.add(manzana)
   col = 0
   amedir = "none"
   while True:
       SCREEN.blit(BG, (0, 0))
       show_score(col)
       if manzana.rect.x - 10 <= miCanasta.rect.x <= manzana.rect.x + 10:
           pygame.mixer.music.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/sonido1.mp3.mp3")
           pygame.mixer.music.play(0)
       miCanasta.update(sgn)
       enemigos.update()
       colision = pygame.sprite.spritecollide(miCanasta, enemigos, False)
       if colision:  # Para que las frutas nuevos no salgan de la pantalla
           col += 1
           manzana.rect.x = random.randrange(pixelesAncho)
           if manzana.rect.x < 0:
               manzana.rect.x = 0 + manzana.rect.width
           elif manzana.rect.x > pixelesAncho:
               manzana.rect.x = pixelesAncho - manzana.rect.width
           manzana.rect.y = 0


       sprites.draw(pantalla)
       enemigos.draw(pantalla)

       for event in pygame.event.get():
           if event.type == QUIT:
               main_menu()

       pygame.display.flip()  # comando necesario para actualizar
       pygame.time.Clock().tick(fps)


def main_menu():
   global empieza
   while True:
       SCREEN.blit(BG, (0, 0))

       MENU_MOUSE_POS = pygame.mouse.get_pos()

       MENU_TEXT = get_font(100).render("MENU PRINCIPAL", True, "#b68f40")
       MENU_RECT = MENU_TEXT.get_rect(center=(950, 100))

       PLAY_BUTTON = Button(image=pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/Play Rect.png"),
                            pos=(950, 400),
                            text_input="JUGAR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
       # OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
       #                        text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
       QUIT_BUTTON = Button(image=pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/Quit Rect.png"),
                            pos=(950, 550),
                            text_input="SALIR", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

       SCREEN.blit(MENU_TEXT, MENU_RECT)

       for button in [PLAY_BUTTON, QUIT_BUTTON]:
           button.changeColor(MENU_MOUSE_POS)
           button.update(SCREEN)

       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
           if event.type == pygame.MOUSEBUTTONDOWN:
               if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                   empieza = time.time()
                   t = threading.Thread(target=lectura)
                   t.daemon = True
                   t.start()
                   circulos_pantalla_calibracion()
               #    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
               #        options()
               if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                   pygame.quit()
                   ser.close()
                   sys.exit()

       pygame.display.update()


main_menu()

