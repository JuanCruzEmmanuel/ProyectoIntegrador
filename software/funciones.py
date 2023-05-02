# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 20:03:36 2022

@author: juanc
"""

"""Funciones"""
def DerIzq(lista,flag,flag2,u):
    
    gapPositivo = 3.8
    gapNegativo = 3.2
    maximo = max(lista)
    minimo = min(lista)
    if flag == 0:
        if flag2 ==0:
            if maximo >= gapPositivo and minimo <=gapNegativo :
                if lista.index(maximo)<lista.index(minimo):
                    print("Derecha")
                    return flag,flag2,u
                else:
                    print("Izquierda")
                    return flag,flag2,u
            if maximo <gapPositivo and minimo > gapNegativo:
                print("centrado")
                return flag,flag2,u
            if maximo >= gapPositivo and minimo > gapNegativo:
                print("Derecha")
                flag = 1
                u=len(lista)-lista.index(maximo)
                return flag,flag2,u
            if maximo < gapPositivo and minimo <=gapNegativo:
                print("izquierda")
                flag = 2
                u=len(lista)-lista.index(minimo)
                return flag,flag2,u
    if flag == 1: #Derecha
        if maximo >= gapPositivo and minimo <=gapNegativo :
            if lista.index(maximo)<lista.index(minimo):
                u+=lista.index(minimo)
                lista = lista[lista.index(minimo):]
                
                
                flag2 = 1
                flag = 0
                return flag,flag2,u
            else:
                u += len(lista)
                return flag, flag2, u
        if maximo < gapPositivo and minimo <=gapNegativo:
            u+=lista.index(minimo)
            flag2 = 1
            flag = 0
            return flag, flag2, u
            
        if maximo <gapPositivo and minimo > gapNegativo:
            print("mantiene")
            u += len(lista)
            return flag,flag2,u
    if flag == 2: #izquierda
        if maximo >= gapPositivo and minimo <=gapNegativo :
            if lista.index(minimo)<lista.index(maximo):
                u+=lista.index(maximo)
                lista = lista[lista.index(maximo):]
                flag2 = 1
                flag = 0
                return flag,flag2,u
            else:
                u += len(lista)
                return flag, flag2, u
        if maximo >= gapPositivo and minimo > gapNegativo:
            u+=lista.index(maximo)
            flag2 = 1
            flag = 0
            return flag, flag2, u
            
        if maximo <gapPositivo and minimo > gapNegativo:
            print("mantiene")
            u += len(lista)
            return flag,flag2,u
    return flag,flag2,u

def ArribaAbajo(lista,flag,flag2,u,mediaAritmetica):

    gapPositivo = 3.7
    gapNegativo = 3.2
    maximo = max(lista)
    i = lista.index(maximo)
    minimo = min(lista)
    der = list()
    if flag == 0:
        if flag2 ==0:
            if maximo >= gapPositivo and minimo <=gapNegativo :
                if lista.index(maximo)<lista.index(minimo):
                    xo = 0
                    c = 0
                    for x in lista[i-10:i+10]:
                        if c>0:
                            der.append(abs(x-xo))
                        xo = x
                        c+=1
                    if max(der)>4*mediaAritmetica: #aca creo que tengo que marcar abajo, y esas cosas
                        return flag, flag2, u       #porque si entro aca es por pestaneo pero hay mirada
                    else:                           #hacia abajo
                        
                        print("Arriba")
                        return flag,flag2,u
                else:
                    print("Abajo")
                    return flag,flag2,u
            if maximo <gapPositivo and minimo > gapNegativo:
                print("centrado")
                return flag,flag2,u
            if maximo >= gapPositivo and minimo > gapNegativo:
                    xo = 0
                    c = 0
                    for x in lista[i-10:i+10]:
                        if c>0:
                            der.append(abs(x-xo))
                        xo = x
                        c+=1
                    if max(der)>4*mediaAritmetica: 
                        return flag, flag2, u       
                                                    
                    else:
                        print("Arriba")
                        flag = 1
                        u=len(lista)-lista.index(maximo)
                        return flag,flag2,u
                    
            if maximo < gapPositivo and minimo <=gapNegativo:
                print("izquierda")
                flag = 2
                u=len(lista)-lista.index(minimo)
                return flag,flag2,u
    if flag == 1: #Derecha
        if maximo >= gapPositivo and minimo <=gapNegativo :
            if lista.index(maximo)<lista.index(minimo):
                u+=lista.index(minimo)
                lista = lista[lista.index(minimo):]
                flag2 = 1
                flag = 0
                return flag,flag2,u
            else:
                u += len(lista)
                return flag, flag2, u
        if maximo < gapPositivo and minimo <=gapNegativo:
            u+=lista.index(minimo)
            flag2 = 1
            flag = 0
            return flag, flag2, u
            
        if maximo <gapPositivo and minimo > gapNegativo:
            print("mantiene")
            u += len(lista)
            return flag,flag2,u
    if flag == 2: #izquierda
        if maximo >= gapPositivo and minimo <=gapNegativo :
            if lista.index(minimo)<lista.index(maximo):
                u+=lista.index(maximo)
                lista = lista[lista.index(maximo):]
                flag2 = 1
                flag = 0
                return flag,flag2,u
            else:
                u += len(lista)
                return flag, flag2, u
        if maximo >= gapPositivo and minimo > gapNegativo:
              xo = 0
              c = 0
              for x in lista[i-10:i+10]:
                  if c>0:
                      der.append(abs(x-xo))
                  xo = x
                  c+=1
              if max(der)>4*mediaAritmetica: 
                  return flag, flag2, u       
                                              
              else:
                  print("Arriba")
                  flag = 0
                  flag2 = 1
                  u+=lista.index(maximo)
                  return flag,flag2,u
          
        if maximo <gapPositivo and minimo > gapNegativo:
            print("mantiene")
            u += len(lista)
            return flag,flag2,u
    return flag,flag2,u
    






if __name__ =="__main__":
    
    print("este es el programa donde van las funciones principales")