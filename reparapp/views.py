from django.shortcuts import render, get_object_or_404
from .models import Cliente
from .models import Equipo
from .models import Reparacion
from django.shortcuts import redirect
from .forms import ReparacionForm


# Create your views here.


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

