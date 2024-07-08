from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductoForm, Producto, ClienteForm, Cliente
from django.contrib import messages 
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa  
from .models import Boleta

def inicio(request):
    return render(request, 'paginas/inicio.html')

def ventas(request):
    query = request.GET.get('q')
    productos = Producto.objects.all()
    
    if query:
        productos = productos.filter(nombre__icontains=query)

    return render(request, 'ventas/ventas.html', {'productos': productos})



def obtener_producto(request):
    codigo = request.GET.get('codigo', '')

    # Validar que el código no esté vacío
    if not codigo:
        return JsonResponse({'error': 'El parámetro "codigo" es requerido.'}, status=400)

    # Buscar el producto por el código
    try:
        producto = get_object_or_404(Producto, codigo=codigo)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado.'}, status=404)

    # Preparar los datos del producto para la respuesta JSON
    data = {
        'nombre': producto.nombre,
        'precio': producto.precio,
    }
    
    return JsonResponse(data)

def buscar_clientes(request):
    if request.method == 'GET' and request.is_ajax():
        nombre_cliente = request.GET.get('nombre', '')
        clientes = Cliente.objects.filter(nombre_razon_social_cliente__icontains=nombre_cliente)
        results = [{'id': cliente.codigo_cliente, 'nombre': cliente.nombre_razon_social_cliente} for cliente in clientes]
        return JsonResponse({'clientes': results})
    return JsonResponse({'clientes': []})



def index(request):
    productos = Producto.objects.all()
    form = ProductoForm()
    
    # Obtener y mostrar el mensaje de éxito si está presente en la sesión
    mensaje = None
    if 'messages' in request.session:
        mensaje = request.session.pop('messages')
    
    return render(request, 'productos/index.html', {'productos': productos, 'form': form, 'mensaje': mensaje})

def crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El producto se agregó correctamente.')
            return redirect('index.html')  # Redirige a la lista de productos
    else:
        form = ProductoForm()
    return render(request, 'productos/crear.html', {'form': form})



def editar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado con éxito')
            return redirect('index.html')  # Asegúrate de que esta URL está correctamente configurada
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar.html', {'form': form, 'producto': producto})


def eliminar_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo =codigo)  # Cambia 'id' al campo correcto de tu modelo
    producto.delete()
    return redirect('index.html') 


def generar_pdf_productos(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="inventario_{datetime.datetime.now().strftime("%Y-%m-%d")}.pdf"'

    # Crear el documento PDF
    doc = SimpleDocTemplate(response, pagesize=letter)
    data = []

    # Estilos
    styles = getSampleStyleSheet()
    titulo_estilo = styles['Title']
    titulo_estilo.alignment = 1  # Centrado

    # Agregar título
    titulo = Paragraph("Inventario", titulo_estilo)
    data.append([titulo])

    # Obtener la lista de productos
    productos = Producto.objects.all()

    # Agregar los encabezados de la tabla
    encabezados = ['Código', 'Nombre', 'Cantidad', 'Precio']
    data.append(encabezados)

    # Agregar los productos a la tabla
    for producto in productos:
        data.append([producto.codigo, producto.nombre, producto.cantidad, producto.precio])

    # Establecer estilos para la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Crear la tabla y aplicar estilos
    tabla = Table(data)
    tabla.setStyle(style)

    # Agregar la tabla al documento
    doc.build([tabla])

    return response


def Lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/clientes.html', {'clientes': clientes})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El cliente se agrego correctamente.')
            return redirect('/clientes/')  # Redirige a la lista de productos
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear.html', {'form': form})

def eliminar_cliente(request, codigo_cliente):
    cliente = get_object_or_404(Cliente, ocdigo_cliente=codigo_cliente)
    cliente.delete()
    return redirect('clientes')

def editar_cliente(request, codigo_cliente):
    cliente= get_object_or_404(Cliente, codigo_cliente=codigo_cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente acualizado')
            return redirect('clientes')  # Asegúrate de que esta URL está correctamente configurada
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/editar.html', {'form': form, 'cliente': cliente})

def documentos(request):
    return render(request, 'paginas/documentos.html')