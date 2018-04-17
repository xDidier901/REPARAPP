from django.shortcuts import render, get_object_or_404
from .models import Cliente
from .models import Equipo
from .models import Reparacion
from django.shortcuts import redirect
from .forms import ReparacionForm
from .forms import EquipoForm
from .forms import ClienteForm


# Create your views here.

########################## Vistas de Reparaciones ##########################
def index(request):
    reparaciones = Reparacion.objects.order_by('fecha_llegada')
    return render(request, 'reparapp/index.html', {'reparaciones': reparaciones})

def reparacion_detail(request, pk):
    reparacion = get_object_or_404(Reparacion, pk=pk)
    return render(request, 'reparapp/reparacion_detail.html', {'reparacion': reparacion})

def reparacion_new(request):
    title = 'Agregar Reparación'
    if request.method == "POST":
        form = ReparacionForm(request.POST)
        if form.is_valid():
            reparacion = form.save(commit=False)
            reparacion.empleado = request.user
            reparacion.completada= False
            reparacion.save()
            return redirect('reparacion_detail', pk=reparacion.pk)
    form = ReparacionForm()
    return render(request, 'reparapp/reparacion_edit.html', {'form': form})

def reparacion_edit(request, pk):
    title = 'Editar Reparación'
    reparacion = get_object_or_404(Reparacion, pk=pk)
    if request.method == "POST":
        form = ReparacionForm(request.POST, instance=reparacion)
        if form.is_valid():
            reparacion = form.save(commit=False)
            reparacion.save()
            return redirect('reparacion_detail', pk=reparacion.pk)
    else:
        form = ReparacionForm(instance=reparacion)
    return render(request, 'reparapp/reparacion_edit.html', {'form': form})

def reparacion_remove(request, pk):
    reparacion = get_object_or_404(Reparacion, pk=pk)
    reparacion.delete()
    return redirect('index')


########################## Vistas de Equipos ##########################

def equipo_list(request):
    equipos = Equipo.objects.order_by('pk')
    return render(request, 'reparapp/equipo_list.html', {'equipos': equipos})

def equipo_detail(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    return render(request, 'reparapp/equipo_detail.html', {'equipo': equipo})

def equipo_new(request):
    title = 'Agregar Equipo'
    if request.method == "POST":
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.save()
            return redirect('equipo_detail', pk=equipo.pk)
    form = EquipoForm()
    return render(request, 'reparapp/equipo_edit.html', {'form': form})

def equipo_edit(request, pk):
    title = 'Editar Equipo'
    equipo = get_object_or_404(Equipo, pk=pk)
    if request.method == "POST":
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.save()
            return redirect('equipo_detail', pk=equipo.pk)
    else:
        form = EquipoForm(instance=equipo)
    return render(request, 'reparapp/equipo_edit.html', {'form': form})

def equipo_remove(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    equipo.delete()
    return redirect('equipo_list')


########################## Vistas de Clientes ##########################

def cliente_list(request):
    clientes = Cliente.objects.order_by('pk')
    return render(request, 'reparapp/cliente_list.html', {'clientes': clientes})

def cliente_detail(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    equipos = Equipo.objects.filter(cliente_id=pk)
    return render(request, 'reparapp/cliente_detail.html', {'cliente': cliente, 'equipos': equipos})

def cliente_new(request):
    title = 'Agregar Cliente'
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()
            return redirect('cliente_detail', pk=cliente.pk)
    form = ClienteForm()
    return render(request, 'reparapp/cliente_edit.html', {'form': form})

def cliente_edit(request, pk):
    title = 'Editar Cliente'
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()
            return redirect('cliente_detail', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'reparapp/cliente_edit.html', {'form': form})

def cliente_remove(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect('cliente_list')