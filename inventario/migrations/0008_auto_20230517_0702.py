# Generated by Django 2.0.2 on 2023-05-17 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0007_auto_20230517_0700'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categorys_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Categorys',
                'verbose_name_plural': 'Categoryss',
                'ordering': ['categorys_name'],
            },
        ),
        migrations.RemoveField(
            model_name='insumos',
            name='insumos_category',
        ),
        migrations.AddField(
            model_name='insumos',
            name='product_category',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.Categorys'),
        ),
    ]
