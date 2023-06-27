from django.db import models
from django.contrib.auth.models import Group, User 

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['category_name']
    
    def __str__(self):
        return self.category_name

def custom_upload_to(instance, filename):
    return 'product/' + filename

class Product(models.Model):
    product_name = models.CharField(max_length=100, null=True, blank=True)
    product_price = models.IntegerField(null=True, blank=True)
    product_image = models.CharField(max_length=240, null=True, blank=True)
    product_state = models.CharField(max_length=100, null=True, blank=True, default='No')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=False)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['product_name']
    
    def __str__(self):
        return self.product_name

class Insumos(models.Model):
    insumos_name = models.CharField(max_length=100, null=True, blank=True)
    insumos_price = models.IntegerField(null=True, blank=True)
    insumos_image = models.CharField(max_length=240, null=True, blank=True)
    insumos_state = models.CharField(max_length=100, null=True, blank=True, default='No')
    insumos_categorys = models.ForeignKey(Category, on_delete=models.CASCADE,default=1, null=False)

    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'
        ordering = ['insumos_name']
    
    def __str__(self):
        return self.insumos_name
