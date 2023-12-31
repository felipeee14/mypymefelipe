# Generated by Django 2.0.2 on 2023-04-21 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proveedor_name', models.CharField(max_length=100)),
                ('proveedor_mail', models.CharField(max_length=100)),
                ('proveedor_phone', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['proveedor_name'],
            },
        ),
    ]
