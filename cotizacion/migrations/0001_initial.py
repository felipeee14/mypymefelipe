# Generated by Django 2.0.2 on 2023-06-27 05:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proveedores', '0003_producto'),
        ('inventario', '0016_auto_20230627_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proveedores.Proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCotizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('monto_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cotizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='cotizacion.Cotizacion')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Product')),
            ],
        ),
    ]
