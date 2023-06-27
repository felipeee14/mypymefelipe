from django.urls import path
from ejemplos import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
ejemplos_urlpatterns = [
    path('ejemplos_main/',views.ejemplos_main,name="ejemplos_main"),
    path('ejemplos_habilidad_add/',views.ejemplos_habilidad_add,name="ejemplos_habilidad_add"),
    path('ejemplos_habilidad_save/',views.ejemplos_habilidad_save,name="ejemplos_habilidad_save"),
    path('ejemplos_habilidad_ver/<habilidad_id>/',views.ejemplos_habilidad_ver,name="ejemplos_habilidad_ver"),
    path('ejemplos_list_habilidades/',views.ejemplos_list_habilidades,name="ejemplos_list_habilidades"),
    path('ejemplos_carga_masiva/',views.ejemplos_carga_masiva,name="ejemplos_carga_masiva"),
    path('ejemplos_carga_masiva_save/',views.ejemplos_carga_masiva_save,name="ejemplos_carga_masiva_save"),
    path('import_file/',views.import_file,name="import_file"),

    #endPoints
    path('ejemplos_habilidad_add_rest/', views.ejemplos_habilidad_add_rest),  
    path('ejemplos_habilidad_list_rest/', views.ejemplos_habilidad_list_rest),  
    path('ejemplos_habilidad_get_element_rest/', views.ejemplos_habilidad_get_element_rest),  
    path('ejemplos_habilidad_update_element_rest/', views.ejemplos_habilidad_update_element_rest), 
    path('ejemplos_habilidad_del_element_rest/', views.ejemplos_habilidad_del_element_rest), 
    path('ejemplos_habilidad_list_date_rest/', views.ejemplos_habilidad_list_date_rest), 
    path('ejemplos_habilidad_list_range_date_rest/', views.ejemplos_habilidad_list_range_date_rest), 
    path('ejemplos_habilidad_list_contains/', views.ejemplos_habilidad_list_contains), 

    path("product_list_rest/",views.product_list_rest),
    path("product_edit_rest/",views.product_edit_rest),
    
    ]

    