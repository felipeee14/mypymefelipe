from django.contrib.auth.models import Group, User #importa los modelos Group y user
from django.db import models #importa los metodos necesarios para trabajar con modellos

# Create your models here.
class Venta2(models.Model):
    
    nombreProducto = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre del producto')
    precioProducto = models.IntegerField(null=True, blank=True, verbose_name='Precio del Producto')
    cantidadProductos = models.IntegerField(null=True, blank=True, verbose_name='Cantidad de Productos')
    montoTotal = models.IntegerField(null=True, blank=True, verbose_name='Monto Total')
    estado = models.CharField(max_length=100, null=True, blank=True, default='En curso', verbose_name='Estado')   
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')
    bloqDes = models.CharField(max_length=100, null=True, blank=True, default='Activo', verbose_name='Activo/Inactivo') 

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']   
    def __str__(self):
        return self.nombreProducto

class Devolucion1(models.Model):
    
    idVenta = models.IntegerField(null=True, blank=True, verbose_name='ID de la Venta')
    motivoDev = models.CharField(max_length=100, null=True, blank=True, verbose_name='Motivo de la Devolucion')
    direccionDev = models.CharField(max_length=100, null=True, blank=True, verbose_name='Direccion del Cliente')
    correoDev = models.CharField(max_length=100, null=True, blank=True, verbose_name='Correo del Cliente')
    fechaDev = models.DateTimeField(auto_now_add=True,verbose_name='Fecha de la Devolucion')

    class Meta:
        verbose_name = 'Devolucion'
        verbose_name_plural = 'Devoluciones'
        ordering = ['id']   
    def _str_(self):
        return self.idVenta        