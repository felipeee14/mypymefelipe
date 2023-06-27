from django.conf.urls import url, include
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from proveedores import views
from .views import descarga_reporte

proveedores_patterns = [
    
    path('proveedores_main', views.proveedores_main,name='proveedores_main'),
    path('proveedores_crear', views.proveedores_crear,name='proveedores_crear'),
    path('proveedor_save/', views.proveedor_save,name='proveedor_save'),
    path('proveedor_list/', views.proveedor_list,name='proveedor_list'),
    path('proveedor_edit/<int:proveedor_id>/', views.proveedor_edit,name='proveedor_edit'),
    path('proveedor_delete/<int:proveedor_id>/', views.proveedor_delete,name='proveedor_delete'),
    path('proveedor_ver/<int:proveedor_id>/', views.proveedor_ver,name='proveedor_ver'),
    path('carga_masiva_proveedor/',views.carga_masiva_proveedor,name="carga_masiva_proveedor"),
    path('carga_masiva_proveedor_save/',views.carga_masiva_proveedor_save,name="carga_masiva_proveedor_save"),
    path('import_file_proveedor/',views.import_file_proveedor,name="import_file_proveedor"),
    path('descarga_reporte/',views.descarga_reporte,name="descarga_reporte"),


    #path('', views.listar_productos, name='listar_productos'),
    #path('agregar/', views.agregar_producto, name='agregar_producto'),
    #path('actualizar/<int:pk>/', views.actualizar_producto, name='actualizar_producto'),
    #path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
]