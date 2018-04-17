from django.contrib import admin
from .models import Equipo
from .models import Cliente
from .models import Reparacion

# Register your models here.
admin.site.register(Equipo)
admin.site.register(Cliente)
admin.site.register(Reparacion)