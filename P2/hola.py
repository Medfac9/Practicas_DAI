# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_file, Response
import os
from mandelbrot import renderizaMandelbrotBonito
import random

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("html.html")

@app.route('/user/<username>')          # Captura una parte del URL
def mostrarPerfilUsuario(username):     # y la pasa como parámetro a la función

    # Mostrar el perfil de usuario
    return 'Usuario %s' % username

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html")

@app.route('/grafico/<x1>/<x2>/<y1>/<y2>/<pixeles>/<iteraciones>/<paletas>')     # /grafico/2.0/5.4/4.0/2.0/200/100/2
def parametros(x1, x2, y1, y2, pixeles,iteraciones, paletas):
    fichero = "./foto.png"
    if(paletas == 1):
        paleta = [(15,99,32),(53,23,65),(89,32,56)]
    elif(paletas == 2):
        paleta = [(145,9,3),(21,124,126),(255,0,43)]
    else:
        paleta = [(15,99,32),(111,32,54),(87,32,76)]

    renderizaMandelbrotBonito(float(x1), float(y1), float(x2), float(y2), int(pixeles), int(iteraciones), fichero, paleta, 3)
    return send_file(fichero, mimetype = "image/png")

@app.route('/grafico/')
def sin_parametros():
    numero = random.randint(0,3)
    if (numero == 0):
        valor1 = random.randint(0,100)
        valor2 = random.randint(0,100)
        valor3 = random.randint(0,100)
        return('''<html>
            <body>
            <svg width="100" height="100">
              <circle cx="%d" cy="%d" r="%d" stroke="red" stroke-width="4" fill="yellow"/>
            </svg>
            </body>
            </html>''' % (valor1, valor2, valor3))
    elif (numero == 1):
        valor1 = random.randint(0,100)
        valor2 = random.randint(0,100)
        valor3 = random.randint(0,100)
        valor4 = random.randint(0,100)
        return('''<html>
            <body>
            <svg width="100" height="100">
              <line x1="%d" x2="%d" y1="%d" y2="%d" stroke="red" stroke-width="4" fill="yellow"/>
            </svg>
            </body>
            </html>''' % (valor1, valor2, valor3, valor4))
    elif (numero == 2):
        valor1 = random.randint(0,100)
        valor2 = random.randint(0,100)
        valor3 = random.randint(0,100)
        valor4 = random.randint(0,100)
        return('''<html>
            <body>
            <svg width="100" height="100">
              <rect x="%d" x="%d" height="%d" width="%d" stroke="green" stroke-width="4" fill="yellow"/>
            </svg>
            </body>
            </html>''' % (valor1, valor2, valor3, valor4))
    elif (numero == 3):
        valor1 = random.randint(0,100)
        valor2 = random.randint(0,100)
        valor3 = random.randint(0,100)
        valor4 = random.randint(0,100)
        return('''<html>
            <body>
            <svg width="100" height="100">
              <line x1="%d" x2="%d" y1="%d" y2="%d" stroke="green" stroke-width="4" fill="red"/>
            </svg>
            </body>
            </html>''' % (valor1, valor2, valor3, valor4))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # 0.0.0.0 para permitir conexiones
                                         #         desde cualquier sitio.
                                         #         Ojo, peligroso: solo
                                         #         en modo debug
