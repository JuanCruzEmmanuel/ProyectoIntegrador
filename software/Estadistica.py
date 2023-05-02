"""
    librerias importadas:
    serial = encargada de apertura y lectura puerto serie
    time = controla la variable tiempo a partir de una fecha ya estipulada
    scipy.signal = aplica filtros a la señal
    pandas = crea y controla dataframes
    numpy = libreria de matrices y matematicas avanzadas
    matplotlib = libreria encargada de los graficos
    sqlite3 = encargada de la creacion y manipulacion de base de datos
"""
import serial, time
import scipy.signal
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sqlite3 as sql

"""
    Esta es la funcion que se utiliza en la funcion "aplicar" que aplica el modelo lineal a los datos.
    Se conecta a la base de datos "Ajuste.db". Debe recibir 5 parametros, la cantidad de exactos obtenidos, la flexib
    la cantidad de errores, el id de prueba y la letra que hace referencia el angulo teorico medido.
    Una vez estos se envien, la funcion se encarga de rellenar la informacion util en su respectivo angulo teorico y
    referenciandolo con el ID.
"""

def insertarFila2(exc, flex, error, ID, Letra):
    conn = sql.connect("Ajuste.db")
    cursor = conn.cursor()
    if Letra == "A" or Letra == "a":
        instruccion = f"INSERT INTO Cinco VALUES (5,{exc},{flex},{error},{ID})"
        cursor.execute(instruccion)
    if Letra == "B" or Letra == "b":
        instruccion = f"INSERT INTO Diez VALUES (10,{exc},{flex},{error},{ID})"
        cursor.execute(instruccion)
    if Letra == "C" or Letra == "c":
        instruccion = f"INSERT INTO Quince VALUES (15,{exc},{flex},{error},{ID})"
        cursor.execute(instruccion)
    if Letra == "D" or Letra == "d":
        instruccion = f"INSERT INTO Veinte VALUES (20,{exc},{flex},{error},{ID})"
        cursor.execute(instruccion)
    if Letra == "E" or Letra == "e":
        instruccion = f"INSERT INTO Veinticinco VALUES (25,{exc},{flex},{error},{ID})"
        cursor.execute(instruccion)
    if Letra == "F" or Letra == "f":
        instruccion = f"INSERT INTO Treinta VALUES (30,{exc},{flex},{error},{ID})"
        cursor.execute(instruccion)
    conn.commit()
    conn.close()



"""
    InsertarFila es la funcion que se utiliza en medicion para rellanar la base de datos "Estadistica.db", esta recibe
    4 parametros, el valor maximo del angulo observado, el valor minimo del angulo observado, el ID referente a la
    persona de estudio y por ultimo la letra que hace referencia a la base de datos especifica dentro de Estadistica.db
    Una vez llamada la funcion, esta se conecta directamente a la base de datos principal, y rellena la informacion
    necesaria. hecho esto cierra la base de datos para que no haya problema

"""

def insertarFila(maximo, minimo, ID, Letra):
    conn = sql.connect("Estadistica.db")
    cursor = conn.cursor()
    if Letra == "A" or Letra =="a":
        instruccion = f"INSERT INTO CincoPositivoD VALUES ({maximo},{minimo},{ID})"
        cursor.execute(instruccion)
    if Letra == "B" or Letra =="b":
        instruccion = f"INSERT INTO DiezPositivoD VALUES ({maximo},{minimo},{ID})"
        cursor.execute(instruccion)
    if Letra == "C" or Letra == "c":
        instruccion = f"INSERT INTO QuincePositivoD VALUES ({maximo},{minimo},{ID})"
        cursor.execute(instruccion)
    if Letra == "D" or Letra =="d":
        instruccion = f"INSERT INTO VeintePositivoD VALUES ({maximo},{minimo},{ID})"
        cursor.execute(instruccion)
    if Letra == "E" or Letra =="e":
        instruccion = f"INSERT INTO VeintiCincoPositivoD VALUES ({maximo},{minimo},{ID})"
        cursor.execute(instruccion)
    if Letra == "F" or Letra =="f":
        instruccion = f"INSERT INTO TreintaPositivoD VALUES ({maximo},{minimo},{ID})"
        cursor.execute(instruccion)
    conn.commit()
    conn.close()
    print("listo")



""""
    Medicion se utiliza para la toma de datos. Se conecta a la base de datos llamada "Estadistica.db"
    El cursor es una funcion que utiliza el objeto .cursor() que viene en sqlite3 para dirigir la base de datos
    hacia un lugar especificio, este caso para ejecutarla. 
    Todo lo siguiente, es mostrar las personas en la base de datos, para saber con antemano su ID, seleccionado este
    en  sujeto_ID se selecciona el angulo a la que se va a mirar. Una vez tomada la medicion esto se repite cuantas
    veces sea necesario. tambien hay un boton para no guardar el dato en caso de ser un error muy grande como puede
    ser por movimientos de cables. Cada angulo tiene una duracion de 3 segundos.
    La conexion y la toma de datos se explica mejor en el programa del juego.
    Los datos de medicion van a la funcion InsertarFilas
"""



def medicion():

    conn = sql.connect("Estadistica.db")
    print("Se conecto a la base de datos Estadistica.db")

    cursor = conn.cursor()
    cursor.execute("select nombre,sujeto_ID from sujeto")

    datos = cursor.fetchall()
    for persona in datos:
        print(persona)

    cursor.close()
    conn.close()

    sujeto_ID = int(input("Ingrese el sujeto_ID "))

    for persona in datos:
        if sujeto_ID == persona[1]:
            print("seleccion a ", persona[0])


    datosderecho = list()
    datosizquierdo = list()

    print(
        "las opciones son: ",
        "A :  5 positivo||",
        "B : 10 positivo||",
        "C:  15 positivo||",
        "D : 20 positivo||",
        "E : 25 positivo||",
        "F : 30 positivo||"
    )
    a = input("Ingrese la opcion ")
    print("-----------------mirar--------------------")

    ser = serial.Serial("COM6", 9600)
    ####################reseteo arduino###################################

    ser.setDTR(False)
    time.sleep(0.5)
    ser.flushInput()
    ser.setDTR(True)
    ######################################################################
    conexion = True
    inicio = time.time()

    while conexion:
        linea = ser.readline().decode("utf-8")
        print(linea)
        if linea[0] == "a":
            datosderecho.append(float(linea[2:6]))
        elif linea[0] == "b":
            datosizquierdo.append(float(linea[2:6]))
        else:
            pass

        final = time.time()

        if final - inicio >= 3:
            print(
                "los datos a agregar es : ", max(datosderecho), " y", min(datosderecho))
            z = input("¿ Desea agregarlos s/n ? ")
            if z == "s":
                insertarFila(max(datosderecho),min(datosderecho), sujeto_ID, a)

            c = input("Desea continuar s/n ")
            if c == "s" or c == "S":
                print(
                    "las opciones son: ",
                    "A :  5 positivo",
                    "B : 10 positivo",
                    "C:  15 positivo",
                    "D : 20 positivo",
                    "E : 25 positivo",
                    "F : 30 positivo"
                )
                a = input("Ingrese la opcion : ")
                datosderecho = list()
                datosizquierdo = list()
                inicio = time.time()
                print("---------MIRAR-----------")
                ser.flushInput()
                linea = ser.readline().decode("utf-8")
            elif c == "n":
                break

    print("se salio")

    ser.close()



"""

    Se conecta a la base de datos "estadistica.db"
    Lo que se busca en esta funcion es leer los datos rellandos en la base de datos anterior, para ellos lo que se
    hace es obtener el numero ID maximo (en este caso debido que el ID empieza en 0 y se incrementa en +1 por cada
    sujeto de pruebas), asi que consiguiendo el valor mas grande, se sabe la cantidad de usuarios que se va a recorrer
    Los datos visualemente se ven mas agradable si la informacion se organiza en los llamados "data frame", entonces 
    se organiza los datos de la base de dato y se crea el dataframe con toda la informacion necesaria.
    Se crean 2 listas principales auxiliares, la primera llamada columnas (que ejercen de titulo de cabecera) y otra
    llamada tablas, que funcionan para redirigir la base de datos hacia ese puntero especifico para luego ordenarla 
    en el dataframe.
    una vez esto, la funcion pregunta si los datos lo quiere de manera completa o si quiere ver la distribucion 
    de los datos tomado.
    Si se elige la opcion "persona" aparecen los datos completo de las personas. con la media de valores referenciados
    a los angulos teoricos y el D.E de los datos tomados.
    Si se elige la opcion "distribucion" lo que se analiza es la distribucion de los datos entre las personas.
    Este ademas pide dos valores, el indice de tabla y el Id a analizar. En especifico para este nos falto aun mas datos
    para obtener resultados concluyentes. Es una herramientas util, pero cuando se tienen miles de datos.
    Por ultimo, "referencia" es similar al "persona" solo que aca se constrasta los valores medios con respecto a su 
    angulo de linealidad para ver cuanta variabilidad tienen estos de manera mas facil
    
"""




def estadistica():

    conn = sql.connect("Estadistica.db")
    IDMax = conn.cursor().execute("SELECT MAX(sujeto_ID) FROM sujeto").fetchone()
    idTotales = np.linspace(1, int(IDMax[0]), int(IDMax[0]))



    """-------------------- CREACION DEL DATAFRAME DE VISUALIZACION DE DATOS --------------------------"""

    columnas = [
        "Nombre",
        "5", "5_D.E.",
        "10", "10_D.E.",
        "15", "15_D.E.",
        "20", "20_D.E.",
        "25", "25_D.E.",
        "30", "30_D.E"]
    columnas2 = ["5",
                 "10",
                 "15",
                 "20",
                 "25",
                 "30",
                 ]




    total = list()

    tablas = [
            "CincoPositivoD",
            "DiezPositivoD",
            "QuincePositivoD",
            "VeintePositivoD",
            "VeintiCincoPositivoD",
            "TreintaPositivoD"
            ]

    opcion = input("Separacion por persona o analisis completo. persona / referencia / distribucion ")
    if opcion == "persona" or opcion == "Persona" or opcion == "PERSONA" or opcion == "p":
        dfEstadistica = pd.DataFrame(columns=columnas)
        GradyDesv = list()
        for id in idTotales:
            nombre = pd.read_sql(f"SELECT nombre FROM sujeto where sujeto_ID= {id}", conn)["nombre"].values.tolist()
            GradyDesv.append(nombre[0])
            for tabla in tablas:
                grados = pd.read_sql(f"SELECT max FROM {tabla} WHERE ID={id}", conn).values.tolist()
                if len(grados) == 0:
                    GradyDesv.append(np.nan)
                    GradyDesv.append(np.nan)
                else:
                    GradyDesv.append(np.mean(grados))
                    GradyDesv.append((np.std(grados)))
                if tabla == "TreintaPositivoD":
                    long = len(dfEstadistica)
                    dfEstadistica.loc[long] = GradyDesv
                    GradyDesv = list()

        print(dfEstadistica.to_markdown())
    elif opcion  == "distribucion":

        a = int(input("Seleccione la tabla: "))
        b = int(input("seleccion al sujeto: "))
        tablas = [
            "CincoPositivoD",
            "DiezPositivoD",
            "QuincePositivoD",
            "VeintePositivoD",
            "VeintiCincoPositivoD",
            "TreintaPositivoD"
        ]
        while a!= 9:
            g = list()
            dist = pd.read_sql(f"SELECT max FROM {tablas[a]} WHERE ID = {b}", conn).values.tolist()
            for x in dist:
                g.append(x[0])
            plt.hist(g, 5)
            plt.show()
            a = int(input("Seleccione la tabla: "))
            b = int(input("seleecion al sujeto : "))
    elif opcion == "referencia" or opcion == "ref":
        dfEstadistica = pd.DataFrame(columns=columnas)
        referenciado = list()
        for id in idTotales:
            nombre = pd.read_sql(f"SELECT nombre FROM sujeto where sujeto_ID= {id}", conn)["nombre"].values.tolist()
            referenciado.append(nombre[0])
            g = pd.read_sql(f"SELECT max FROM TreintaPositivoD WHERE ID={id}", conn).values.tolist()
            referencia = float(np.mean(g))
            for tabla in tablas:
                valores = list()
                grados = pd.read_sql(f"SELECT max FROM {tabla} WHERE ID={id}", conn).values.tolist()
                for x in grados:
                    valores.append((x[0]*30/referencia))
                referenciado.append(np.mean(valores))
                referenciado.append(np.std(valores))
                if tabla == "TreintaPositivoD":
                    long = len(dfEstadistica)
                    dfEstadistica.loc[long] = referenciado
                    referenciado = list()

        print(dfEstadistica.to_markdown())
        a = input("¿ Quiere graficar los datos normalizados ? s/n ")
        while a!= "n":
            y = list()
            i = int(input("Seleccione indice: "))
            fila = dfEstadistica.iloc[i].tolist()
            for c in range(len(fila)):
                if c % 2 != 0:
                    y.append(fila[c])
            x = [5,10,15,20,25,30]
            plt.axis([0, 35, 20, 40])
            plt.plot(x, y, label=fila[0])
            plt.legend()
            plt.show()
            a = input("¿ Quiere graficar los datos normalizados ? s/n ")

        print("Adios")

    conn.close()


"""
    Aplicar es la ultima funcion que se diseño en este programa, en este si bien a simplevista puede parecer el mas
    largo de los otros, esto se debe a que la comunicacion serie con arduino se hizo mas facil desde esta, ya que hay
    que mezclar medicion con estadistica.
    
    En resumen nuevamente se conecta a la base de datos, esto si se desea se puede evitar pero se debe calibrar previa-
    -mente. Si se selecciona la opcion utilizando la base de datos nuevamente se hace lo previamente nombrado de 
    seleccionar mediante Id a la persona y con ello poder se obtine la V30 (valor maximo) y se calcula la 
    vn (valor normalizado) en este caso se uso de manera empirica el valor central que es de 3.66(en este primer estudio
    se conecta con la señal de arduino y se empieza a recibir datos ahora convertidos directamente a grados.
    En caso de no seleccionar la base de datos se necesitan realizar 3 mediciones, centrada para la V0, a v30 y V-30.
    luego nuevamente se debe crear la tension normalizada V0.
    Una vez realizada la conversion se empiezan a tomar mediciones con estos convertidos directamente a angulos y se 
    compara con angulos teoricos, y los resultados se envian directo a la base de datos utilizando la funcion
    insertarfila2. Los resultados de esta prueba son los angulos exactos, flexibles y error. Una vez enviado se reinicia
    y se vuelve a la toma de datos para nuevas pruebas.
"""



def aplicar():
    z = input("Desea evaluar usar la base de datos : s/n ")
    if z == "s" or z=="S" or z=="si":

        conn = sql.connect("Estadistica.db")
        print("Se conecto a la base de datos Estadistica.db")

        cursor = conn.cursor()
        cursor.execute("select nombre,sujeto_ID from sujeto")

        datos = cursor.fetchall()
        for persona in datos:
            print(persona)

        cursor.close()

        sujeto_ID = int(input("Ingrese el sujeto_ID "))
        v30 = np.mean(pd.read_sql(f"SELECT max FROM TreintaPositivoD WHERE ID={sujeto_ID}", conn).values.tolist())
        vn = [1/(v30-3.66), 3.66/(v30-3.66)]  # Esta en teoria es la tension normalizada de la persona en la bbdd

        ser = serial.Serial("COM6", 9600)
        ####################reseteo arduino###################################

        ser.setDTR(False)
        time.sleep(0.5)
        ser.flushInput()
        ser.setDTR(True)
        ######################################################################
        conexion = True
        inicio = time.time()
        datosderecho = list()
        datosizquierdo = list()
        print("mirar")
        while conexion:
            linea = ser.readline().decode("utf-8")
            if linea[0] == "a":
                datosderecho.append(float(linea[2:6]))
            elif linea[0] == "b":
                datosizquierdo.append(float(linea[2:6]))
            else:
                pass

            final = time.time()
            if final-inicio >= 3:
                grado = 30*( max(datosderecho)*vn[0]-vn[1])
                print(grado)

                datosderecho = list()
                datosizquierdo = list()
                print("mirar")
                inicio = time.time()
        conn.close()
    if z =="n":
        conn = sql.connect("Ajuste.db")         # conecta a la base de comparacion
        ser = serial.Serial("COM6", 9600)
        ser.setDTR(False)
        time.sleep(0.5)
        ser.flushInput()
        ser.setDTR(True)
        ######################################################################
        print("se va a medir los parametros")
        n,n2 = 3,3
        datosderecho = list()
        datosizquierdo = list()
        cen = list()
        v30 = list()
        print("centrado")
        inicio = time.time()
        while n!=0:
            linea = ser.readline().decode("utf-8")
            #print(linea)
            if linea[0] == "a":
                datosderecho.append(float(linea[2:6]))
            elif linea[0] == "b":
                datosizquierdo.append(float(linea[2:6]))
            final = time.time()
            if final - inicio >=2:
                b, a = scipy.signal.butter(3, 15, fs=450)
                filtrada = scipy.signal.filtfilt(b, a, datosderecho)
                cen.append(np.mean(filtrada))
                datosderecho = list()
                datosizquierdo =list()
                n-=1
                inicio = time.time()
        print("mirar a 30°")
        while n2!=0:
            linea = ser.readline().decode("utf-8")
            if linea[0] == "a":
                datosderecho.append(float(linea[2:6]))
            elif linea[0] == "b":
                datosizquierdo.append(float(linea[2:6]))
            final = time.time()
            if final - inicio >= 3:
                b, a = scipy.signal.butter(3, 15, fs=450)
                filtrada = scipy.signal.filtfilt(b, a, datosderecho)
                v30.append(max((filtrada)))
                datosderecho = list()
                datosizquierdo = list()
                n2 -= 1
                inicio = time.time()
                print("mirar a 30°")


        #Aca se crea la recta a comparar
        vn = [1 / (np.mean(v30) - np.mean(cen)), np.mean(cen) / (np.mean(v30) - np.mean(cen))]

        print(
            "las opciones son: ",
            "A :  5 positivo||",
            "B : 10 positivo||",
            "C:  15 positivo||",
            "D : 20 positivo||",
            "E : 25 positivo||",
            "F : 30 positivo||"
        )
        letra = input("Ingrese la opcion ")
        conexion = True
        numEnsayo = 10
        exacto = 0
        flexible = 0
        error = 0
        id = int(input("Ingrese el id: "))
        print("Mirar")
        inicio = time.time()
        while conexion:
            linea = ser.readline().decode("utf-8")
            if linea[0] == "a":
                datosderecho.append(float(linea[2:6]))
            elif linea[0] == "b":
                datosizquierdo.append(float(linea[2:6]))
            else:
                pass

            final = time.time()
            if final-inicio >= 4:
                b, a = scipy.signal.butter(3, 15, fs=450)
                filtrada = scipy.signal.filtfilt(b, a, datosderecho)
                grado = 30*(max(filtrada)*vn[0]-vn[1])
                if letra == "a" or letra == "A":
                    if abs(grado-5)<1:
                        exacto+=1
                    elif abs(grado-5)<5:
                        flexible +=1
                    else:
                        error+=1
                if letra == "b" or letra == "B":
                    if abs(grado-10)<1:
                        exacto+=1
                    elif abs(grado-10)<5:
                        flexible +=1
                    else:
                        error+=1
                if letra == "c" or letra == "C":
                    if abs(grado-15)<1:
                        exacto+=1
                    elif abs(grado-15)<5:
                        flexible +=1
                    else:
                        error+=1
                if letra == "d" or letra == "D":
                    if abs(grado-20)<1:
                        exacto+=1
                    elif abs(grado-20)<5:
                        flexible +=1
                    else:
                        error+=1
                if letra == "e" or letra == "E":
                    if abs(grado-25)<1:
                        exacto+=1
                    elif abs(grado-25)<5:
                        flexible +=1
                    else:
                        error+=1
                if letra == "f" or letra == "F":
                    if abs(grado-30)<1:
                        exacto+=1
                    elif abs(grado-30)<5:
                        flexible +=1
                    else:
                        error+=1

                datosderecho = list()
                datosizquierdo = list()
                numEnsayo -= 1
                if numEnsayo == 0:
                    numEnsayo = 10
                    print(exacto,flexible,error)
                    insertarFila2(exacto, flexible, error, id, letra)
                    exacto=0
                    flexible = 0
                    error = 0
                    print(
                        "las opciones son: ",
                        "A :  5 positivo||",
                        "B : 10 positivo||",
                        "C:  15 positivo||",
                        "D : 20 positivo||",
                        "E : 25 positivo||",
                        "F : 30 positivo||"
                        )
                    letra = input("Ingrese la opcion ")
                print("Mirar")
                inicio = time.time()

    pass


"""
    apertura del programa, la instruccion __name__=="__main__" se utiliza para programas que se ejecutan en si mismos
    pero las funciones creadas en este programa se pueden utilizar en otros programas importando este.
    Al iniciar se pide seleccionar que funcion va a utilizar de las 3, las cuales son:
    *   medicion,    que se encarga de la toma de datos de los usuarios.
    *   Estadistica, que se encarga de utilizar los valores realizados en medicion y estimar la media y desvio
    *   aplicar,     que se encarga de aplicar el modelo lineal y comparar con angulos teoricos.    
"""
if __name__ =="__main__":
    print("Hola este es el programa de estadistica")
    print("Desea medir o ver la estadistica")
    seleccion = input("seleccion m para medir o e para la estadistica o a de aplicar: ")
    while seleccion != "salir":
        if seleccion == "m":
            medicion()
        elif seleccion == "e":
            estadistica()
        elif seleccion == "a":
            aplicar()

        seleccion = input("seleccion m para medir o e para la estadistica o a de aplicar: ")
    print("Se salio")

