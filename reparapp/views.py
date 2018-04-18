from django.shortcuts import render, get_object_or_404
from .models import Cliente
from .models import Equipo
from .models import Reparacion
from django.shortcuts import redirect
from .forms import ReparacionForm
from .forms import EquipoForm
from .forms import ClienteForm

from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from django.views.generic import View
from django.http import HttpResponse
import time

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

########################## Reportes ##########################

class ReporteReparacionesPDF(View):

    def cabecera(self,pdf):
            #Utilizamos el archivo logo.png que está guardado en la carpeta media/imagenes
            archivo_imagen = settings.MEDIA_ROOT+'/imagenes/logo.png'
            #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
            pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)
            #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
            pdf.setFont("Helvetica", 16)
            #Dibujamos una cadena en la ubicación X,Y especificada
            pdf.drawString(230, 790, u"        REPARAPP     ")
            pdf.setFont("Helvetica", 14)
            pdf.drawString(200, 770, u"REPORTE DE REPARACIONES")
            pdf.setFont("Helvetica", 12)
            pdf.drawString( 450, 750, u"Fecha:"+time.strftime("%d/%m/%y"))
    def tabla(self,pdf,y):
            #Creamos una tupla de encabezados para neustra tabla
            encabezados = ('Equipo', 'Descripcion', 'Fecha_llegada','Fecha_salida','Reparado')
            #Creamos una lista de tuplas que van a contener a las reparaciones
            detalles = [(reparacion.equipo.modelo, reparacion.descripcion, reparacion.fecha_llegada,"Sin salida" if reparacion.fecha_salida is None else reparacion.fecha_salida ,"Si" if reparacion.completada else 'No') for reparacion in Reparacion.objects.order_by('fecha_llegada')]
            #Establecemos el tamaño de cada una de las columnas de la tabla
            detalle_orden = Table([encabezados] + detalles, colWidths=[4 * cm, 7 * cm, 2.5 * cm, 2.5 * cm,2 * cm])
            #Aplicamos estilos a las celdas de la tabla
            detalle_orden.setStyle(TableStyle(
            [
                    #La primera fila(encabezados) va a estar centrada
                    ('ALIGN',(0,0),(3,0),'CENTER'),
                    #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    #El tamaño de las letras de cada una de las celdas será de 10
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ]
            ))
            #Establecemos el tamaño de la hoja que ocupará la tabla
            detalle_orden.wrapOn(pdf, 800, 600)
            #Definimos la coordenada donde se dibujará la tabla
            detalle_orden.drawOn(pdf, 60,y)

    def get(self, request, *args, **kwargs):
            #Indicamos el tipo de contenido a devolver, en este caso un pdf
            response = HttpResponse(content_type='application/pdf')
            #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
            buffer = BytesIO()
            #Canvas nos permite hacer el reporte con coordenadas X y Y
            pdf = canvas.Canvas(buffer)
            #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
            self.cabecera(pdf)
            y = 600
            self.tabla(pdf, y)
            #Con show page hacemos un corte de página para pasar a la siguiente
            pdf.showPage()
            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response