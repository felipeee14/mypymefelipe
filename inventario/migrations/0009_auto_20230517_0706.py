# Generated by Django 2.0.2 on 2023-05-17 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0008_auto_20230517_0702'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorys',
            options={'ordering': ['category_name'], 'verbose_name': 'Category', 'verbose_name_plural': 'Category'},
        ),
        migrations.RenameField(
            model_name='categorys',
            old_name='categorys_name',
            new_name='category_name',
        ),
        migrations.RenameField(
            model_name='insumos',
            old_name='product_category',
            new_name='insumos_category',
        ),
    ]
