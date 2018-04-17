from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField  # Librería externa

# MODELOS PARA REALIZAR LAS MIGRACIONES PARA CREAR LAS TABLAS EN LA BASE DE DATOS

# Instalar librería para el campo de PhoneNumberField().
# Instalar estado dentro del entorno virtual: pip install django-phonenumber-field
# https://github.com/stefanfoulis/django-phonenumber-field

# MODELO DE CLIENTE
class Cliente(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=40)
    correo = models.EmailField()
    telefono = PhoneNumberField()

    def __str__(self):
        return (self.nombre + " " + self.apellido)


# MODELO DE EQUIPO
class Equipo(models.Model):

    # Lista de sistemas operativos
    # En la parte izquierda se define como se guardará en la BD
    # y en de la derecha como saldrá en el combobox
    SISTEMAS_OPERATIVOS = (
        ('W10', 'Windows 10'),
        ('W8', 'Windows 8'),
        ('W7', 'Windows 7'),
        ('WV', 'Windows Vista'),
        ('WXP', 'Windows XP'),
        ('LINUX', 'LINUX'),
        ('OS', 'Mac OS'),
        ('UNIX', 'UNIX'),
        ('WV', 'Windows Vista'),
        ('O', 'Otro'),
    )
    # Default
    INDEFINIDO = 'INDEFINIDO'

    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    sistema_operativo = models.CharField(
        max_length=10,
        choices=SISTEMAS_OPERATIVOS,
        default=INDEFINIDO,
    )

    def __str__(self):
        return (self.modelo + " - " + self.cliente.apellido)

# MODELO DE REPARACION
class Reparacion(models.Model):
    empleado = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    equipo = models.ForeignKey('Equipo', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    fecha_llegada = models.DateField(auto_now_add=True)
    fecha_salida = models.DateField(blank=True, null=True)
    completada = models.BooleanField()

    def completarReparacion(self):
        self.fecha_salida = timezone.now()
        self.save()

    def __str__(self):
        return ("Reparación No." + str(self.pk) + " - " + str(self.fecha_llegada))
