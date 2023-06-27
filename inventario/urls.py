from django.conf.urls import url, include
from django.urls import path
from inventario import views
from django.views.decorators.csrf import csrf_exempt

inventario_patterns = [
    
    #Productos
    path('inventario_main', views.inventario_main,name='inventario_main'),
    path('crear_producto/',views.crear_producto,name='crear_producto'),
    path('producto_list/',views.producto_list,name='producto_list'),
    path('producto_save/',views.producto_save,name='producto_save'),
    path('producto_ver/<product_id>/',views.producto_ver,name='producto_ver'),
    path('producto_edit/<int:product_id>/', views.producto_edit, name='producto_edit'),
    path('producto_delete/<int:product_id>/', views.producto_delete, name='producto_delete'),
    path('carga_masiva_producto/',views.carga_masiva_producto,name="carga_masiva_producto"),
    path('carga_masiva_producto_save/',views.carga_masiva_producto_save,name="carga_masiva_producto_save"),
    path('import_file_producto/',views.import_file_producto,name="import_file_producto"),
   
    path('descarga_reporte_producto/',views.descarga_reporte_producto,name="descarga_reporte_producto"),
    path('reportes_main_productos/',views.reportes_main_productos,name="reportes_main_productos"),
    path('reporte_producto_filtro/',views.reporte_producto_filtro,name="reporte_producto_filtro"),

    #Categorias
    path("crear_category/",views.crear_category, name="crear_category"),
    path('category_list/',views.category_list,name='category_list'),
    path("category_save/",views.category_save, name="category_save"),
    path('category_ver/<category_id>/',views.category_ver,name='category_ver'),
    path('category_edit/<int:category_id>/', views.category_edit, name='category_edit'),
    path('category_delete/<int:category_id>/', views.category_delete, name='category_delete'),
    path('carga_masiva_category/',views.carga_masiva_category,name="carga_masiva_category"),
    path('carga_masiva_category_save/',views.carga_masiva_category_save,name="carga_masiva_category_save"),
    path('import_file_category/',views.import_file_category,name="import_file_category"),

    #Insumos
    path('insumos_main/',views.insumos_main,name="insumos_main"),
    path('crear_insumos/', views.crear_insumos ,name='crear_insumos'),
    path('insumos_ver/', views.insumos_ver ,name='insumos_ver'),
    path('insumos_list/', views.insumos_list,name='insumos_list'),

    path('insumos_save/',views.insumos_save,name='insumos_save'),
    path('insumos_ver/<insumos_id>/',views.insumos_ver,name='insumos_ver'),
    path('insumos_edit/<int:insumos_id>/', views.insumos_edit, name='insumos_edit'),
    path('insumos_delete/<int:insumos_id>/', views.insumos_delete, name='insumos_delete'),
    path('descarga_reporte_insumo/',views.descarga_reporte_insumo,name="descarga_reporte_insumo"),
    path('reportes_main_insumo/',views.reportes_main_insumo,name="reportes_main_insumo"),
    path('reporte_insumo_filtro/',views.reporte_insumo_filtro,name="reporte_insumo_filtro"),

    path('correo1/',views.correo1,name="correo1"),


    ]