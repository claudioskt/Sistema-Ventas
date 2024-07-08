from django.db import models
import locale

# Create your models here.

class Producto(models.Model):
    codigo = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=50)
    cantidad = models.PositiveSmallIntegerField()
    precio = models.IntegerField(default=0)

    def __str__(self):
        texto= "{0} ({1})- ${2}"
        return texto.format(self.nombre, self.cantidad, self.precio)
    

class Cliente(models.Model):
    codigo_cliente = models.AutoField(primary_key=True)
    nombre_razon_social_cliente = models.CharField(max_length=255)
    rut_cliente = models.CharField(max_length=12, unique=True)
    direccion_cliente = models.CharField(max_length=255)
    giro_comercial_cliente = models.CharField(max_length=255)
    comuna_cliente = models.CharField(max_length=255)
    telefono_cliente = models.CharField(max_length=20, blank=True, null=True)
    email_cliente = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f'{self.nombre_razon_social_cliente} ({self.codigo_cliente})'
    

class Boleta(models.Model):
    fecha_emision = models.DateField(auto_now_add=True)
    tipo_pago = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)