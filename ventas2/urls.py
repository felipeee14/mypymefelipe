from django.urls import path
from ventas2 import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url, include


ventas2_urlpatterns = [
    path('ventas_main/',views.ventas_main,name="ventas_main"),
    path('ventas_venta_add/',views.ventas_venta_add,name="ventas_venta_add"),
    path('ventas_venta_save/',views.ventas_venta_save,name="ventas_venta_save"),
    path('ventas_venta_ver/<venta_id>/',views.ventas_venta_ver,name="ventas_venta_ver"),
    path('ventas_list_venta/',views.ventas_list_venta,name="ventas_list_venta"),
    path('ventas_venta_devolucion/',views.ventas_venta_devolucion,name="ventas_venta_devolucion"),
    path('base_ventas/',views.base_ventas,name="base_ventas"),
    path('ventas_venta_edit_estado/<venta_id>/',views.ventas_venta_edit_estado,name="ventas_venta_edit_estado"),
    path('ventas_venta_filtrar/',views.ventas_venta_filtrar,name="ventas_venta_filtrar"),

    #endPoints
    path('ventas_venta_add_rest/', views.ventas_venta_add_rest),  
    path('ventas_venta_list_rest/', views.ventas_venta_list_rest),
    path('ventas_venta_get_element_rest/', views.ventas_venta_get_element_rest),
    path('ventas_venta_update_element_rest/', views.ventas_venta_update_element_rest),
    path('ventas_venta_del_element_rest/', views.ventas_venta_del_element_rest),
    path('ventas_venta_list_date_rest/', views.ventas_venta_list_date_rest),
    path('ventas_venta_list_range_date_rest/', views.ventas_venta_list_range_date_rest),
    path('ventas_venta_list_contains/', views.ventas_venta_list_contains),
    path('ventas_devolucion_add_rest/', views.ventas_devolucion_add_rest),
    path('ventas_venta_update_estado_rest/', views.ventas_venta_update_estado_rest),
    
    path('pdf_cotizacion/', views.pdf_cotizacion, name='pdf_cotizacion'),
    path('dashboard_main/',views.dashboard_main,name="dashboard_main"),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('exportar_a_pdf/', views.exportar_a_pdf, name='exportar_a_pdf')


    ]

    