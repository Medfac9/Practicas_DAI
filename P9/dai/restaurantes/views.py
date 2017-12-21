from django.shortcuts import render, HttpResponse
from .models import restaurantes
from django.http import JsonResponse
from django.core import serializers
from .forms import NameForm, Usuario
import json
from pymongo import MongoClient

# Create your views here.

def index(request):
    return render(request,'index.html',{})

def login(request):
    return render(request,'registration/login.html',{})

def comprobacion_login(request):
    if request.method == 'POST':
        form = Usuario(request.POST)
        if form.is_valid(): 
            datos = comprobarUsuario(request.POST["correo"], request.POST["contra"])
            if (datos):
                if (cursor):
                    context = {"datos": "Loggueado correctamente"}
                    return render(request, 'index.html', context)
                else:
                    context = {"datos": "No se ha loggueado correctamente"}
                    return render(request, 'registration/login.html', context)
            else:
                context = {"datos": "No existe esos datos"}
                return render(request, 'registration/login.html', context)
        else:
            context = {"datos": "Formulario invalido"}
            return render(request, 'registration/login.html', context)
    else:
        context = {"datos": "No es un metodo post"}
        return render(request, 'registration/login.html', context)  

def comprobarUsuario(correo, contra):
    if (restaurantes.find({"correo": correo})):
        if (restaurantes.find({"contra": contra})):
            return True
        else:
            return False
    else:
        return False

def logout(request):
    return render(request,'index.html',{})

def blank(request):
    return render(request,'blank.html',{})
    
def ejemplo(request):
    return render(request,'ejemplo.html',{})

def ultima(request):
    return render(request,'ultima.html',{})

def registro(request):
    return render(request,'registration/registro.html',{})

def grafico(request):
    if request.method == 'GET':
        getGrafico(request)
        return render(request, 'grafico.html')

def devuelveListaCompleta(restaurant_info):
    cursor = restaurantes.distinct(restaurant_info)
    lista_tipos = []
    for document in cursor:
        lista_tipos.append(document)

    return lista_tipos

def numeroRestaurantesCocina(tipo):
    return restaurantes.find({'cuisine': tipo}).count()

def getGrafico(request):
    datos = devuelveListaCompleta('cuisine')
    datos_grafico = dict()

    for i in range(0, len(datos)):
        datos_grafico[datos[i]] = numeroRestaurantesCocina(datos[i])

    return HttpResponse(json.dumps(datos_grafico), content_type="application/json")

def mapa(request):
    nombres_disponibles = get_restaurants_values('name')
    if request.method == 'GET':
        context = {
            'username' : request.user.username, 
            "nombres_disponibles": list(nombres_disponibles), 
            'lat' : 37.177336, 
            'lon' : -3.598557
        }
        return render(request, 'mapa.html', context)
    else:
        restaurante = request.POST['nombre']
        coordenadas = devuelveCoordenadas(restaurante)
        context = {
            "nombres_disponibles": list(nombres_disponibles),
            'lat': coordenadas[1], 
            'lon' : coordenadas[0]
            }
        return render(request, 'mapa.html', context)

def devuelveCoordenadas(nombre_restaurante):
    client = MongoClient()
    db = client.test
    lista_tipos = []
    cursor = db.restaurants.find({'name': nombre_restaurante})
    for restaurante in cursor:
        lista_tipos.append(restaurante["address"])
    return(lista_tipos[0]["coord"])

def comprobacion_resgistro(request):
    if request.method == 'POST':
        form = Usuario(request.POST)
        if form.is_valid(): 
            datos = comprobarUsuarioResgistro(request.POST["correo"], request.POST["contra"])
            if (datos):
                if (cursor):
                    context = {"datos": "Registrado correctamente"}
                    return render(request, 'index.html', context)
                else:
                    context = {"datos": "No se ha registrado correctamente"}
                    return render(request, 'registration/registro.html', context)
            else:
                context = {"datos": "No existe esos datos"}
                return render(request, 'registration/registro.html', context)
        else:
            context = {"datos": "Formulario invalido"}
            return render(request, 'registration/registro.html', context)
    else:
        context = {"datos": "No es un metodo post"}
        return render(request, 'registration/registro.html', context)  

def comprobarUsuarioResgistro(correo, contra):
    if (restaurantes.insert({"correo": correo, "contra" : contra})):
        return True
    else:
        return False

def comprobacion_registro(request):
    return render(request,'index.html',{})

def usuario(request):
    return render(request,'usuario.html',{})

def editar_usuario(request):
    return render(request,'usuario.html',{})

def formulario(request):
    return render(request,'formulario.html',{})

def restauranteAjax(request):
    tipos_cocina_disponibles = get_restaurants_values('cuisine')
    barrios_disponibles = get_restaurants_values('borough')
    context = {
      "tipos_cocina_disponibles": list(tipos_cocina_disponibles),
      "barrios_disponibles": list(barrios_disponibles)
    }
    return render(request,'restauranteAjax.html',context)

def get_restaurants_values(restaurant_info):
    cursor = restaurantes.distinct(restaurant_info)
    return cursor

def get_restaurants(request,tipo_cocina,barrio,numero_restaurantes):
    return search_restaurants(request,tipo_cocina,barrio,int(numero_restaurantes))

def search_restaurants(request,tipo_cocina, barrio,skip=0):
    cursor = restaurantes.find({"cuisine": tipo_cocina, "borough": barrio}).limit(10).skip(skip)
    data = []
    for restaurante in cursor:
            print(restaurante)
            data.append({"name" : restaurante["name"],
                "address" : restaurante["address"]["street"],
                "grade" : restaurante["grades"][0]["grade"]
            })
    return JsonResponse(data,safe=False)

def test_template(request):
    context = {}   # Aquí van la las variables para la plantilla
    return render(request,'test.html', context)

def nuevo_restaurante(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():                 
            #Meter en base de datos
            datos = crearRestaurante(request.POST["name"], request.POST["tipo"])
            if(datos):
                context = {"datos": "Se ha creado correctamente"}
                return render(request, 'formulario.html', context)
            else:
                context = {"datos": "No se ha creado correctamente"}
                return render(request, 'formulario.html', context)
        else:
            context = {"datos": "Algunos de los campos es incorrecto"}
            return render(request, 'formulario.html', context)

def crearRestaurante(nombre, tipo):
    if (restaurantes.insert({"cuisine": tipo, "name" : nombre})):
        return True
    else:
        return False

def modificar_restaurante(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():                 
            #Meter en base de datos
            datos = crearRestaurante(request.POST["name"], request.POST["tipo"])
            if(datos):
                context = {"datos": "Se ha modificado correctamente o modificado correctamente"}
                return render(request, 'formulario.html', context)
            else:
                context = {"datos": "No se ha modificado correctamente"}
                return render(request, 'formulario.html', context)
        else:
            context = {"datos": "Algunos de los campos es incorrecto"}
            return render(request, 'formulario.html', context)