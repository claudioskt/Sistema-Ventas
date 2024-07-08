from django import forms
from .models import Producto, Cliente

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'cantidad', 'precio']


class VentaForm(forms.Form):
    codigo_producto = forms.CharField()
    cantidad_vendida = forms.IntegerField()

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_razon_social_cliente', 'rut_cliente', 'direccion_cliente', 'giro_comercial_cliente'
                  , 'comuna_cliente', 'telefono_cliente', 'email_cliente']