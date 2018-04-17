from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^reparacion/(?P<pk>\d+)/$', views.reparacion_detail, name='reparacion_detail'),
    re_path(r'^reparacion/new/$', views.reparacion_new, name='reparacion_new'),
    re_path(r'^reparacion/(?P<pk>\d+)/edit/$', views.reparacion_edit, name='reparacion_edit'),
]