# Generated by Django 2.0.2 on 2023-06-27 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0014_auto_20230606_2317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['product_name'], 'verbose_name': 123, 'verbose_name_plural': 'Products'},
        ),
    ]
