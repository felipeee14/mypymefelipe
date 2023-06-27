from django.db import models
from inventario.models import Product
from proveedores.models import Proveedor

from django.db import models

class Cotizacion(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Otros campos de cotización
    
    def __str__(self):
        return f"Cotización #{self.id}"


class ProductCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Producto: {self.product.product_name}, Cantidad: {self.quantity}, Monto total: {self.monto_total}"


