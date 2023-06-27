from django.urls import path
from . import views

cotizacion_urlpatterns = [
    path('cotizaciones_main/', views.cotizaciones_main, name='cotizaciones_main'),
    path('crear_cotizacion/', views.crear_cotizacion, name='crear_cotizacion'),
    path('lista_cotizacion/', views.lista_cotizacion, name='lista_cotizacion'),
    path('cotizacion_save', views.cotizacion_save, name='cotizacion_save')
]