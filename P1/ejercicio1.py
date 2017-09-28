#!/usr/bin/env python3

import random

print("Bienvenido, vamos a jugar")

alto = 'El numero introducido es mayor que el numero buscado'
bajo = 'El numero introducido es menor que el numero buscado'
x = random.randint(1, 100)
cont = 0

numero = int(input("Introduzca un numero: "))

while numero != x and cont < 10:
    if numero > x:
        print(alto)
    else:
        print(bajo)
    numero = int(input("Introduzca otro numero: "))
    cont += 1

if cont >= 10:
    print("Has tardado mucho, el numero era: ", x)
else:
    print("Enhorabuena, encontraste el numero")
