# Generated by Django 2.0.2 on 2023-06-08 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas2', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venta2',
            options={'ordering': ['id'], 'verbose_name': 'Venta', 'verbose_name_plural': 'Ventas'},
        ),
    ]