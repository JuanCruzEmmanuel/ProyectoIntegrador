"""Proyecto Integrador 2022 Noya-Albornoz"""
"""

    Primero se importan las librerias externas de python :
    -pygame = libreria que se encarga de manejar de manera sencilla programacion orientada a objetos
    enfocada en colisiones y herramientas relacionada al control de estos.
    -random = libreria enfocada al uso y manipulacion de numeros pseudoaleatorios, en este caso para que los
    objetos caigan de manera aleatorio por la pantalla.
    -time = controla el tiempo en segundos.
    -serial = controla el puerto serie para la recepcion de datos.
    -threading = la libreria mas importante, debido a que esta maneja distinto hilos para programacion en paralelo.
    -se importan desde pygame la carpeta * que habilita las superfunciones.
    -se desarrollo un programa aparte llamado button para controlar de manera externa botones al inicio del juego
"""

import pygame, sys, random, time, serial, threading
from pygame.locals import *
from button import Button

"""
    
"""
derecho = list()
izquierdo = list()
derecho_derecho = list()
izquierdo_izquierdo = list()

"""
    Inicia la comunicacion con el puerto serie, en este caso 
    particular utilizamos el COM6 y a 9600 baudios
    
    Una forma generica que se puede solucionar esto seria:
    
    ports = serial.tools.list_ports.comports()
    for puertos in ports:
        portList.append(str(puertos))
        print(str(puertos))
    selPuerto = input("seleccionar el puerto COM")
    ser = serial.Serial(selPuerto, 9600)
    
    Con esto se seleccionaria el puerto de manera manual en el caso de no saber cual es el disponible
"""
ser = serial.Serial("COM6", 9600)

####################reseteo arduino###################################
"""
    El reseteo del DTR cumple la funcion de resetear la memoria interna del puerto con el fin de que 
    no exita problema a la hora de reiniciar el programa, ya que sin esto el puerto tendria un error
    de "busy port" o "puerto ocupado
    una vez reseteado se debe volver a encender el buffer de almacenamiento del puerto con las intrucciones
    flushimput() y setdtr(true)"
    
"""

ser.setDTR(False)
time.sleep(0.5)
ser.flushInput()
ser.setDTR(True)

######################variables globales################################

"""
    Las variables globales en Python son aquellas definidas en el cuerpo principal del 
    programa fuera de cualquier función. Son accesibles desde cualquier punto del programa, 
    incluso desde dentro de funciones.
    
    En este caso particular FPS significa los cuadros por segundo de refresco, con esto se calcula 
    la velocidad de movimiento de los objetos en pantalla. Lo normal en un juego es colocarlo en 30 o 60 
    dependiendo de la taza de refrezco del monitor
    
    Las demas varibales son el tamaño de la ventana en donde se va a llevar acabo el juego. 1900px ancho y 
    960px de alto
    
    el set_mode coloca una pantalla de ese tamaño de px pero con un color en blanco. con el BG (background), se
    busca tener un fondo diseñado de manera propia, este se coloca mediante una ubicacion especifica que depende
    de la carpeta donde se ejecuta el programa en este caso "C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/fondo2.png"
    el convert() al final busca disminuir el uso de memoria innecesaria 
    
    Se vera el mensaje de "Menu" en la parte superior de la ventana
    
"""
fps = 60
pixelesAncho, pixelesAlto = 1900, 960
SCREEN = pygame.display.set_mode((1900, 960))
pygame.display.set_caption("Menu")
col = 0
BG = pygame.image.load("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/fondo2.png").convert()
aux = 1

"""
    -Se inicia el juego con el comando pygame.init()
    -el pygame.font.Font toma una fuente previamente descargada y se utiliza dentro de la ventana del juego
    este recibe dos argumentos, por un lado la ubicacion de la fuente y por otro lado el tamaño de fuente.
"""

pygame.init()
font = pygame.font.Font("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/font.ttf", 32)
font2 = pygame.font.Font("C:/Users/juanc/Desktop/ProyectoIntegrador/Asset/font.ttf", 180)

umbCent = list()
umbDer = list()
umbIzq = list()
start = 0
funcionando = str()
flag = 0
sgn = "cen"
reseteo = "no"
amedir = "pass"

"""

    La funcion control se accede desde la funcion daemon "lectura", esta recibe la informacion de la señal derecha e 
    izquierda para controlar la canasta del juego. 
    Esta funcion maneja una flag llamada "flag" que indicara el estado de la lectura. si la señal que se recibe es cero
    entonces la flag se encuentra en cero y el control estara dispuesto a realizar un movimiento izquierda o derecha.
    si se realiza un movimiento hacia la derecha la flag obtiene el valor de "1" y la canasta se movera hacia la derecha
    por las caracteristicas fisiologicas de la señal ocular puede existir una meseta sobre la señal base o realizar un
    movimiento opuesto al inicial (en este caso un pico negativo). Por lo que si en la proxima itereacion el flag es 1
    y se registra una meseta, entonces la canasta se seguira moviendo hacia la derecha asi hasta que reciba el registro
    de un pico negativo, en este caso reinicia el flag a cero.
    El mismo criterio se efectua para el movimiento hacia la izquierda, en este caso cambia el flag de "0" a "2" y este
    no se reinicia (se seguira moviendo hacia la izquierda) hasta recibir una señal de pico positivo donde se detiene.

"""


def control(lista):
    global flag, sgn, umbral3, umbral1, umbral2inf, umbral2sup, reseteo
    if reseteo == "no":
        if flag == 0:

            if max(lista) >= max(umbDer) - 0.1 * max(umbDer):
                if min(lista) > min(umbIzq) + 0.1 * min(umbIzq):
                    flag = 1
                    sgn = "der"
                else:
                    flag = 0
                    sgn = "cen"
            elif min(lista) <= min(umbIzq) + 0.1 * min(umbIzq):
                if max(lista) < max(umbDer) - 0.1 * max(umbDer):
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
            elif max(lista) > max(umbDer) - 0.1 * max(umbDer):
                flag = 0
                sgn = "cen"
                reseteo = "si"
            elif min(lista)  < min(umbIzq) + 0.1 * min(umbIzq):
                flag = 0
                sgn = "cen"
                reseteo = "si"

        elif flag == 2:

            if max(lista)<= umbral2sup:
                if umbral2inf <= min(lista):
                    flag = 2
                    sgn = "izq"
            elif max(lista) > max(umbDer) - 1 * max(umbDer):
                flag = 0
                sgn = "cen"
                reseteo = "si"

            elif min(lista)< min(umbIzq) + 0.1 * min(umbIzq):
                flag = 0
                sgn = "cen"
                reseteo = "si"

    elif reseteo == "si":
        reseteo = "no"
        sgn = "cen"
        flag = 0


"""
   -La lectura es la funcion que se encuentra en threading. Esta posee dos partes, una enfocada a la lectura para calib
    y otra enfocada para el control. 
   -Para la calibracion debe recibir la señal desde la funcion circulo_para_calibrar() y obtener una señal de .start = 0
    con esto, estaremos en la primer porcion de la funcion. Con esto en mente, la calibracion envia las flag de centrado
    derecha y de izquierda, con esto almacena la informacion en distintas listas; "umbCent", "umbDer" y "umbIzq" 
    que luego se accede en la funcion "control" para depurar estos valores y controlar el juego.
   -La lectura en general siempre realiza lo siguiente. Lee desde puerto serie previamente abierto, y realizar una doble
    decodificacion, una primera que hace referencia a si proviene del ojo derecho (a) o del ojo izquierdo (b) y luego 
    decodificado con el .decode("utf-8") que es el formato mas conocido en trasmisiones de datos.
    
   -Cuando la calibracion finaliza, .start = 1, se accede a la segunda porcion de la funcion lectura, que se encarga del
   control. En este caso lo importante de entender es que se leen porciones de 60 datos y se actualizan para volver a 
   llenar las listas. luego se envia ambas señales derecha e izquierda a la funcion control.

"""


def lectura():
    global derecho, derecho_derecho, izquierdo, izquierdo_izquierdo, funcionando, umbCent, umbDer, umbIzq

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


"""
    -Este funcion se accede desde el main_menu() al precionar el "Button" con la expresion "jugar"
    -Se accede a una pantalla con un BG cargado previamente en las variables globales y colocado en pantalla mediante
    el comando .blitz en una posicion inicial (0,0), esto equivale a la esquina superior izquierda.
    -se crea una variable local "t" en la que manipula el tiempo en pantalla de los circulos de calibracion, modificando
    este se aumenta o reduce el tiempo de los circulos en pantalla
    -se crea un objeto llamado "circulo" que pertenece a la clase "calibracion", este objeto posee varias propiedades
    que nos parecieron interesantes para poder controlar de manera eficiente los valores del usuario. Por un lado
    posee una imagen propia que debe encontrarse en la carpeta donde se ejecuta el programa, si se modifica esta
    cambiaria la imagen que se proyecta en pantalla. Tambien en si misma posee un comando que indica que el circulo se
    inicializo llamado "self.start", que este se encuentra en cero en caso de no haberse inicializado la calibracion y 
    cuando es 1 significa que ya se realizo la calibracion, tambien posee un "self.mesure" que indica en que etapa de
    medicion se encuentra, posee 3 estados "centrado", "derecha" e "izquierda"
    -Los sprite en pygame sirven para poder manipular los objetos que interactuan en pantalla de manera mas facil, se 
    agrega el objeto circulo a lo clase sprite.
    
    Iniciando el ciclo while, se pregunta si se ha finalizado la calibracion (start =1), si esto no sucede, arranca
    un conteo decreciente desde 5 seg a 0 seg en la funcion "Countdown()" una vez esto finalizado arranca la calibracion
    propiamente dicha.
    
    amedir es una variable global que al modificarse actua sobre el objeto "circulo" y tambien actua sobre la funcion en 
    threading "lectura" para tomar los valores estadisticos de la persona. Luego con esta informacion se aplica el model
    y se maneja el videojuego.
    Sobre el objeto circulo modifica el estado ".mesure" y cambia la posicion que se encuentra en pantalla, este a su 
    vez tiene una funcion propia (self) que maneja el tiempo que se encuentra en cada estado.
    Una vez finalizado el ultimo estado (el objeto empieza centrado, cambia a la derecha, vuelve a centrado y finaliza
    en la izquierda) el self.start obtiene el valor de "1" y entra en el estado de "jugar" para iniciar el juego.
    
    
"""


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
            self.velocidad_x = -4
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


"""
   La funcion jugar se accede desde la funcion circulos_pantalla_calibrar() cuando el objeto circulo obtiene el 
  .start = 1, que significa que se ha realizado la calibracion.
   -la variable global amedir se vuelve a actualizar en el caso de que haya algun cambio dentro de esta funcion.
   -el set_mode recibe los pixeles de ancho y anto de la pantalla para poder ejecutarse, y muestra en la parte sup 
   el nombre "lateralidad - Albornoz y noya" debido al set_caption.
   -se crean distintos objetos, como es el caso de manzana que es de la clase "enemigo" y luego se agrega al grupo de
   enemigos gracias a la funcion .sprite.Group() de pygame para poder controlar las colisiones de manera mas facil.
   tambien se crean el objeto miCanasta de la clase "canasta" y este se agrega a un grupo llamado sprite para contr
   las colisiones con el grupo "enemigo" de manera mas facil.
   una vez dentro del ciclo while, el .blitz muestra en pantalla el BG. el show_score() es una funcion que muestra en
   pantalla el numero de colisiones que se han realizado. Este valor es importante porque va a servir para indicar 
   al usuario la facilidad o dificultad a la hora de poder mover los ojos.
   -el objeto manzana tiene propiedades propias (self) como su imagen, tamaño, velocidad de movimiento y tiene una 
   funcion propia llamada update() que actualiza en cada etapa al objeto. En este caso cada vez que el objeto llega a 
   su punto mas bajo o recibe una colision, aparece un nuevo objeto manzana de manera aleatoria por la pantalla. La vel
   de caida es constante y siempre reaparece a una altura igual a cero(parte superior de pantalla)
   -el objeto "miCanasta" posee propiedades propias(self) como su imagen, altura en la cual se desplaza (modificando el
   self.rect.center), lo mas importante es la funcion update(), en la cual recibe la señal desde la funcion "lectura"
   y determina la direccion de movimiento de la canasta. La velocidad de movimiento por el momento se mantiene
   constante, en un futuro aumentara en funcion al angulo de movimiento.
   la direccion la obtiene apartir de la flag "sig" que es una variable global pero solo modificable desde "lectura".
   -Por cada colision, la variable local col incrementa y se muestra en pantalla gracias a la funcion show_score y
   el display.flip() que actualiza la pantalla.
    
    
"""


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
                # pygame.quit()
                # sys.exit()

        pygame.display.flip()  # comando necesario para actualizar
        pygame.time.Clock().tick(fps)


"""
    -En "main_menu" se desarrollora el menu principal y es primera funcion que corre,
    del cual se accederan a las demas funciones.
    -Lo primero se utilizan las variables declaradas anteriormente como el BG y las fonts para utilizarlas
    -Una primera funcion que obtiene la posicion del mouse en todo momento llamada MENU_MOUSE_POS, este al hacer
    click activa un evento "get_event" y "checkforimput" si se encuentra en el rectangulo del boton. 
    - El play button y quit button poseen ambas caracteristicas similares y tamaños de rectangulos iguales, pero
    ubicacion distinta. Estos activan eventos distintos, uno empieza la calibracion y el otro cierra el programa.
    
    -El comando .blitz lo que hace es posiciona los elementos que posee en el argumento 
    en la pantalla, sin este estos no aparecerian 
    
    -la funcion principal de main_menu es seleccionar entre dos botones, el jugar y el de salir. con lo dicho anterior
    si el cursor se encuentra por arriba de estos botones y se realiza un click entra a la seccion de "event" o evento
    el de jugar lleva a la funcion circulos_pantalla_calibracion() mientras que el de salir cierra el juego.
    
    -por ultimo el display actualiza la pantalla con una taza de refresco de los FPS seleccionado en las variales
    globales
    
    
    por otro lado la funcion Button se realizo de manera externa, este se importa desde la carpeta donde se encuentra
    el programa ejecuntado y el codigo es el siguiente :
    class Button():
    
        def __init__(self, image, pos, text_input, font, base_color, hovering_color):
            self.image = image
            self.x_pos = pos[0]
            self.y_pos = pos[1]
            self.font = font
            self.base_color, self.hovering_color = base_color, hovering_color
            self.text_input = text_input
            self.text = self.font.render(self.text_input, True, self.base_color)
            if self.image is None:
                self.image = self.text
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    
        def update(self, screen):
            if self.image is not None:
                screen.blit(self.image, self.rect)
            screen.blit(self.text, self.text_rect)
    
        def checkForInput(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in 
            range(self.rect.top, self.rect.bottom):
                return True
            return False
    
        def changeColor(self, position):
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in 
            range(self.rect.top, self.rect.bottom):
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)
    
        
     con este programa realizado de manera externa nos ahorramos escribir mas lineas de codigo dentro del programa 
     principal. En este se crea un objeto "class" llamada "Button" en el cual se le incorportan las caracteristicas
     que pueden tener los botones, estas son el color "changeColor", el si se presiono "checkForImput"
     Como parametro principal, los "self" que recibe el boton son la imagen que este va a tener, la posicion en la
     pantalla, la fuente y el tamaño de fuente, y el texto que este va a tener. La funcion "update" es una funcion 
     que llevan todos los objetos en el caso de que estos se actualicen de manera externa y se sigan representando
     en pantalla.   
    
    -Un apartado propio se deberia abarcar a la hora del trhearing, ya que gracias a esto es posible que el juego
    controle por un lado la interfaz grafica(GUI) y por separado la lectura de la informacion (lectura), sin este
    el juego tendria crasheos (fallos) o directamente mediria o moveria el juego.
    Python maneja de varias manera el uso de distintos nucleos de trabajo, en este caso el mas eficiente para la lect
    fue el trheading, este se importa de manera externa y simplemente se crea el hilo de la siguiente forma:
    
    threading.Thread(target="funcion a donde se direcciona el hilo, en este caso lectura")
    t.daemon = True. existen muchas formas de crear los hilos, el tipo daemon prioriza la utilizacion de memoria 
    para partes de programa que el usuario no puede modificar, como la recepcion de informacion.
    

"""


def main_menu():
    # global empieza
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
                    # jugar()
                #    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                #        options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    ser.close()
                    sys.exit()

        pygame.display.update()


main_menu()
