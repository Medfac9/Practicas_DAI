# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_file, Response, session, request, redirect, url_for, jsonify
from flask_session import Session
import os
import shelve
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()

@app.route('/')
def index():
    if not session.get("esta_logueado"):
        return render_template("index.html")
    else:
        session["ultima"] = "Inicio"
        return render_template("index.html", logueado = True)

@app.route('/login', methods=["GET", "POST"])
def login():
    if not session.get("esta_logueado"):
        return render_template("login.html")
    else:
        session["ultima"] = "Login"
        return render_template("index.html", logueado = True)

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session["esta_logueado"] = False
    session.clear()
    return render_template("index.html")

@app.route('/blank', methods=["GET", "POST"])
def blanca():
    if not session.get("esta_logueado"):
        session["ultima"] = "Página en blanco"
        return render_template("blank.html")
    else:
        session["ultima"] = "Página en blanco"
        return render_template("blank.html", logueado = True)

@app.route('/ejemplo', methods=["GET", "POST"])
def ejemplo():
    if not session.get("esta_logueado"):
        session["ultima"] = "Página de ejemplo"
        return render_template("ejemplo.html")
    else:
        session["ultima"] = "Página de ejemplo"
        return render_template("ejemplo.html", logueado = True)

@app.route('/ultima', methods=["GET", "POST"])
def ultima():
    if not session.get("esta_logueado"):
        return render_template("index.html")
    else:
        return render_template("ultima.html", logueado = True)


@app.route('/registro', methods=["GET", "POST"])
def registro():
    if not session.get("esta_logueado"):
        return render_template("registro.html")
    else:
        return render_template("index.html", logueado = True)

@app.route('/usuario', methods=["GET", "POST"])
def usuario():
    if not session.get("esta_logueado"):
        return render_template("index.html")
    else:
        session["ultima"] = "Usuario"
        return render_template("usuario.html", logueado = True)

@app.route('/comprobacion_login', methods=["POST"])
def comprobacion_login():
    bd = shelve.open("bd.db", writeback=True)
    correo = request.form["email"]
    contrasenia = request.form["password"]
    if correo in bd:
        if contrasenia == bd[correo]:
            session["esta_logueado"] = True
            session["email"] = correo
            session["pass"] = contrasenia
        else:
            return render_template("login.html", contrasenia_error = True)
    else:
        return render_template("login.html", usuario_error = True)

    bd.close()
    return render_template("index.html")

@app.route('/comprobacion_registro', methods=["POST"])
def comprobacion_registro():
    bd = shelve.open("bd.db", writeback=True)
    if not session.get("esta_logueado"):
        if (len(request.form["password"]) == 0):
            return render_template("registro.html", contrasenia_error = True)
        else:
            correo = request.form["email"]
            contrasenia = request.form["password"]
            bd[correo] = contrasenia
            bd.close()
            return render_template("index.html", exito_registro = True)
    else:
        return render_template("index.html")

@app.route('/edicion', methods=["POST"])
def editar_usuario():
    bd = shelve.open("bd.db", writeback=True)
    if not session.get("esta_logueado"):
        if (len(request.form["password"]) == 0):
            return render_template("registro.html", contrasenia_error = True)
        else:
            correo = request.form["email"]
            contrasenia = request.form["password"]
            bd[correo] = contrasenia
            bd.close()
            return render_template("index.html", exito_registro = True)
    else:
        if (len(request.form["password"]) == 0):
            return render_template("usuario.html", contrasenia_error = True)
        else:
            correo = request.form["email"]
            contrasenia = request.form["password"]
            bd[correo] = contrasenia
            bd.close()
            session["email"] = correo
            session["pass"] = contrasenia
            return render_template("usuario.html", exito_edicion = True)

@app.route('/restaurante', methods=["GET", "POST"])
def restaurante():
    if not session.get("esta_logueado"):
        session["ultima"] = "Página de restaurante"
        return render_template("restaurante.html")
    else:
        session["ultima"] = "Página de restaurante"
        return render_template("restaurante.html", logueado = True)

def find(name):
    db = client.test
    lista_tipos = []
    cursor = db.restaurants.distinct( name )
    for document in cursor:
        lista_tipos.append(document)

    return lista_tipos

@app.route('/comprobarRestaurantes', methods=['POST'])
def devuelveRestaurantes():
    opcion = request.form['opcion']

    if (opcion == 'Ciudad'):
        return render_template("restaurante.html", varCiudad=True, lista_ciudades=find('borough'))

    if (opcion == 'Puntuacion'):
        return render_template("restaurante.html", varPuntuacion=True, lista_puntuaciones=find('grades.grade'))

    if (opcion == 'Cocina'):
        return render_template("restaurante.html", varCocina=True, lista_tipos=find('cuisine'))

@app.route('/comprobarCiudad', methods=['POST'])
def devuelveCiudad():
    opcion = request.form['opcion']
    db = client.test
    lista = []
    cursor = db.restaurants.distinct( "name", { "borough": opcion } )
    for document in cursor:
        lista.append(document)

    return render_template("restaurante.html",checked=opcion, lista=lista, varCiudad=True, lista_ciudades=find('borough'))

@app.route('/comprobarPuntuacion', methods=['POST'])
def devuelvePuntuacion():
    opcion = request.form['opcion']
    db = client.test
    lista = []
    cursor = db.restaurants.distinct( "name", { "grades.grade": opcion } )
    for document in cursor:
        lista.append(document)

    return render_template("restaurante.html",checked=opcion, lista=lista, varPuntuacion=True, lista_puntuaciones=find('grades.grade'))

@app.route('/comprobarCocina', methods=['POST'])
def devuelveCocina():
    opcion = request.form['opcion']
    db = client.test
    lista = []
    cursor = db.restaurants.distinct( "name", { "cuisine": opcion } )
    for document in cursor:
        lista.append(document)

    return render_template("restaurante.html",checked=opcion, lista=lista, varCocina=True, lista_tipos=find('cuisine'))

@app.route('/restauranteAjax')
def restauranteAjax():
    tipos_cocina_disponibles = get_restaurants_values('cuisine')
    barrios_disponibles = get_restaurants_values('borough')
    if not session.get("esta_logueado"):
        session["ultima"] = "Página de restaurante ajax"
        return render_template("restauranteAjax.html", content=5, tipos_cocina=tipos_cocina_disponibles, barrios = barrios_disponibles)
    else:
        session["ultima"] = "Página de restaurante ajax"
        return render_template("restauranteAjax.html", content=5, tipos_cocina=tipos_cocina_disponibles, barrios = barrios_disponibles, logueado = True)

def get_restaurants_values(restaurant_info):
    db = client.test
    cursor = db.restaurants.distinct(restaurant_info)
    return cursor

@app.route('/get-restaurants/<cocina>/<barrio>')
def get_restaurants(cocina,barrio):
    return search_restaurants2(cocina,barrio)

@app.route('/get-restaurants/<cocina>/<barrio>/<numero_restaurantes>')
def get_restaurants2(cocina,barrio,numero_restaurantes):
    return search_restaurants2(cocina,barrio,int(numero_restaurantes))

def search_restaurants(tipo_cocina, barrio, skip=0):
    db = client.test
    cursor = db.restaurants.find({"cuisine": tipo_cocina, "borough": barrio}).limit(10).skip(skip)
    return cursor

def search_restaurants2(tipo_cocina, barrio, skip=0):
    db = client.test
    cursor = db.restaurants.find({"cuisine": tipo_cocina, "borough": barrio}).limit(10).skip(skip)
    data = []
    for restaurante in cursor:
        print(restaurante)
        data.append({"name" : restaurante["name"],
            "address" : restaurante["address"]["street"],
            "grade" : restaurante["grades"][0]["grade"]
        })
    return jsonify(data)

app.secret_key = 'bagw0sah9^xoa$2_*#yat1hl71yjf*p$8dn)9oyhb))$=5qfuh'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # 0.0.0.0 para permitir conexiones
                                         #         desde cualquier sitio.
                                         #         Ojo, peligroso: solo
                                         #         en modo debug
