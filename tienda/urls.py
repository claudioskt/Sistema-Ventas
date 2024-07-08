

from django.urls import path
from .views import index, inicio, crear, eliminar_producto, editar_producto, generar_pdf_productos, ventas,obtener_producto,buscar_clientes, Lista_clientes,crear_cliente,eliminar_cliente,editar_cliente,documentos

urlpatterns = [
 path('', inicio, name='inicio'),
   path('documentos/',documentos, name='documentos'),
    path('productos/', index, name='index.html'),
    path('productos/crear/', crear, name='crear'),
    path('productos/editar/<str:codigo>/', editar_producto, name='editar_producto'),
    path('productos/eliminar/<str:codigo>/', eliminar_producto, name='eliminar_producto'),
    path('descargar-pdf/', generar_pdf_productos, name='descargar_productos_pdf'),
    path('ventas/',ventas, name='ventas'),
    path('obtener-producto/',obtener_producto, name='obtener_producto'),
    path('buscar-clientes/', buscar_clientes, name='buscar_clientes'),
    path('clientes/',Lista_clientes, name ='clientes'),
    path('clientes/crear/',crear_cliente, name ='crear'),
    path('clientes/editar/<str:codigo_cliente>/', editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<str:codigo_cliente>/', eliminar_cliente, name='eliminar_cliente'),






   ]




