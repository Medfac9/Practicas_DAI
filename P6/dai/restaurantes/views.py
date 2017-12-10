from django.shortcuts import render, HttpResponse
from .models import restaurantes
from django.http import JsonResponse
from django.core import serializers

# Create your views here.

def index(request):
    return render(request,'index.html',{})

def login(request):
    return render(request,'login.html',{})

def comprobacion_login(request):
    return render(request,'index.html',{})

def logout(request):
    return render(request,'index.html',{})

def blank(request):
    return render(request,'blank.html',{})
    
def ejemplo(request):
    return render(request,'ejemplo.html',{})

def ultima(request):
    return render(request,'ultima.html',{})

def registro(request):
    return render(request,'registro.html',{})

def comprobacion_registro(request):
    return render(request,'index.html',{})

def usuario(request):
    return render(request,'usuario.html',{})

def editar_usuario(request):
    return render(request,'usuario.html',{})

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