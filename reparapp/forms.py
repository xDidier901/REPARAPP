from django import forms
from .models import Cliente, Equipo, Reparacion

class ReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields = ['equipo', 'descripcion','completada']


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombre','apellido','correo','telefono',)

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = '__all__'