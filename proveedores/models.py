from django.db import models
from django.contrib.auth.models import Group, User 

class Proveedor(models.Model):
    proveedor_name = models.CharField(max_length= 100)
    proveedor_mail = models.CharField(max_length= 100)
    proveedor_phone = models.CharField(max_length= 100)



    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['proveedor_name']
    
    def __str__(self):
        return self.proveedor_name

class OrdenCompra(models.Model):
    proveedor = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)
    # Otros campos que necesites

    def __str__(self):
        return f'Orden de compra {self.id}'
    
    from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    proveedor = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField() 