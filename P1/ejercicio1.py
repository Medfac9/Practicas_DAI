#!/usr/bin/env python3

import random

print("Bienvenido, vamos a jugar")

alto = 'El numero introducido es mayor que el numero buscado'
bajo = 'El numero introducido es menor que el numero buscado'
x = random.randint(1, 100)
numero = int(input("Introduzca un numero: "))

while numero != x:
    if numero > x:
        print(bajo)
    else:
        print(alto)
    numero = int(input("Introduzca otro numero: "))
print("Enhorabuena, encontraste el numero")
