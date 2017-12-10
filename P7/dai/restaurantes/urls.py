from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^login$', views.login, name='login'),
  url(r'^comprobacion_login$', views.comprobacion_login, name='comprobacion_login'),
  url(r'^logout$', views.logout, name='logout'),
  url(r'^registro$', views.registro, name='registro'),
  url(r'^comprobacion_registro$', views.comprobacion_registro, name='comprobacion_registro'),
  url(r'^usuario$', views.usuario, name='usuario'),
  url(r'^edicion$', views.editar_usuario, name='edicion'),
  url(r'^blank$', views.blank, name='blank'),
  url(r'^ejemplo$', views.ejemplo, name='ejemplo'),
  url(r'^ultima$', views.ultima, name='ultima'),
  url(r'^restauranteAjax$', views.restauranteAjax, name='restauranteAjax'),
  url(r'^get-restaurants/(?P<tipo_cocina>[a-zA-Z]+)/(?P<barrio>[a-zA-Z]+)$', views.search_restaurants),
  url(r'^get-restaurants/(?P<tipo_cocina>[a-zA-Z]+)/(?P<barrio>[a-zA-Z]+)/(?P<numero_restaurantes>\d+)$', views.get_restaurants),
  url(r'^formulario$', views.formulario, name='formulario'),
  url(r'^nuevo_restaurante/$', views.nuevo_restaurante),
]