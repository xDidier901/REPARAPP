from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    #Reparaciones
    re_path(r'^reparacion/(?P<pk>\d+)/$', views.reparacion_detail, name='reparacion_detail'),
    re_path(r'^reparacion/new/$', views.reparacion_new, name='reparacion_new'),
    re_path(r'^reparacion/(?P<pk>\d+)/edit/$', views.reparacion_edit, name='reparacion_edit'),
    re_path(r'^reparacion/(?P<pk>\d+)/remove/$', views.reparacion_remove, name='reparacion_remove'),

    #Equipos
    re_path(r'^equipo/$', views.equipo_list, name='equipo_list'),
    re_path(r'^equipo/(?P<pk>\d+)/$', views.equipo_detail, name='equipo_detail'),
    re_path(r'^equipo/new/$', views.equipo_new, name='equipo_new'),
    re_path(r'^equipo/(?P<pk>\d+)/edit/$', views.equipo_edit, name='equipo_edit'),
    re_path(r'^equipo/(?P<pk>\d+)/remove/$', views.equipo_remove, name='equipo_remove'),

    #Clientes
    re_path(r'^cliente/$', views.cliente_list, name='cliente_list'),
    re_path(r'^cliente/(?P<pk>\d+)/$', views.cliente_detail, name='cliente_detail'),
    re_path(r'^cliente/new/$', views.cliente_new, name='cliente_new'),
    re_path(r'^cliente/(?P<pk>\d+)/edit/$', views.cliente_edit, name='cliente_edit'),
    re_path(r'^cliente/(?P<pk>\d+)/remove/$', views.cliente_remove, name='cliente_remove'),
]