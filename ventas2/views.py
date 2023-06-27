from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from registration.models import Profile 
from django.db.models import Q
from django.shortcuts import render
import logging
from rest_framework import generics, viewsets
from rest_framework.decorators import (
	api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
import ventas2
from ventas2.models import Venta2, Devolucion1
from inventario.models import Product
from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO
import xhtml2pdf.pisa as pisa


from reportlab.pdfgen import canvas


#Funciones para templates
@login_required
def ventas_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/ventas_main.html'
    return render(request,template_name,{'profile':profile})

@login_required
def base_ventas(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/base_ventas.html'
    return render(request,template_name,{'profile':profile})

@login_required
def ventas_venta_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/ventas_add.html'
    return render(request,template_name,{'profile':profile})

@login_required
def ventas_venta_devolucion(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/ventas_devolucion.html'
    return render(request,template_name,{'profile':profile})

@login_required
def ventas_venta_edit_estado(request,venta_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    sale_count = Venta2.objects.filter(pk=venta_id).count()
    if sale_count <= 0:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    estado = request.POST.get('estado')
    venta = get_object_or_404(Venta2, pk = venta_id)
    venta.estado = estado
    venta.save()
    return redirect('ventas_list_venta')

@login_required
def ventas_venta_filtrar(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    nombre = request.POST.get('nombreProducto')
    filtro = Venta2.objects.filter(nombreProducto = nombre)
    context = {'ventas': filtro}
    return redirect(request, 'ventas_list_venta.html', context)

@login_required
def ventas_venta_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        montoTotal = 0
        nombreProducto = request.POST.get('nombreProducto')
        precioProducto = request.POST.get('precioProducto')
        cantidadProductos = request.POST.get('cantidadProductos')
        montoTotal = int(precioProducto) * int(cantidadProductos)
        estado = request.POST.get('estado')        
        if nombreProducto == '' or precioProducto == '' or cantidadProductos == '' or estado == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('ventas_venta_add')
        if estado == 'En curso' or estado == 'Finalizada' or estado == 'Cancelada':
            venta_save = Venta2(
                nombreProducto = nombreProducto,
                precioProducto = precioProducto,
                cantidadProductos = cantidadProductos,
                montoTotal = montoTotal,
                estado = estado,
                )
            venta_save.save()
            messages.add_message(request, messages.INFO, 'Venta creada con éxito')
            return redirect('ventas_list_venta')
        else:
            messages.add_message(request, messages.INFO, 'Ingrese un estado correcto')
            return redirect('ventas_venta_add')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def ventas_venta_ver(request,venta_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    venta_data = Venta2.objects.get(pk=venta_id)
    template_name = 'ventas/ventas_venta_ver.html'
    return render(request,template_name,{'profile':profile,'venta_data':venta_data})

@login_required
def ventas_list_venta(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if page == None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') == None:
        page = page
    else:
        page = request.GET.get('page') 
    if search == None:
        search = request.GET.get('search')
    else:
        search = search
    if request.GET.get('search') == None:
        search = search
    else:
        search = request.GET.get('search') 
    if request.method == 'POST':
        search = request.POST.get('search') 
        page = None
    h_list = []
    if search == None or search == "None":
        h_count = Venta2.objects.all()
        h_list_array = Venta2.objects.filter().order_by('estado')
        for h in h_list_array:
            h_list.append({'id':h.id,'nombreProducto':h.nombreProducto, 'cantidadProductos':h.cantidadProductos,'precioProducto':h.precioProducto, 'montoTotal': h.montoTotal, 'estado': h.estado})
    else:
        h_count = Venta2.objects.filter().filter(estado__icontains=search).count()
        h_list_array = Venta2.objects.filter().filter(estado__icontains=search).order_by('estado')
        for h in h_list_array:
            h_list.append({'id':h.id,'nombreProducto':h.nombreProducto,'cantidadProductos':h.cantidadProductos,'precioProducto':h.precioProducto, 'montoTotal': h.montoTotal, 'estado': h.estado})            
    paginator = Paginator(h_list, 1) 
    h_list_paginate= paginator.get_page(page)   
    template_name = 'ventas/ventas_list_venta.html'
    return render(request,template_name,{'template_name':template_name,'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page})


#ENDPOINT CREAR VENTA 
@api_view(['POST'])
def ventas_venta_add_rest(request, format=None):    
    if request.method == 'POST':
        montoTotal = 0
        nombreProducto = request.data['nombreProducto']
        precioProducto = request.data['precioProducto'] 
        cantidadProductos = request.data['cantidadProductos'] 
        estado = request.data['estado']
        montoTotal = precioProducto * cantidadProductos
        if precioProducto <= 0:
            return Response({'Msj': "El precio no puede ser 0"})
        if nombreProducto == '' or estado == '' or precioProducto == '' or cantidadProductos == '':
            return Response({'Msj': "Error los datos no pueder estar en blanco"})
        if estado == 'Finalizada' or estado == 'En curso' or estado == 'Cancelada':                 
            venta_save = Venta2(
                nombreProducto = nombreProducto,
                precioProducto = precioProducto,
                cantidadProductos = cantidadProductos,
                montoTotal = montoTotal,
                estado = estado,
                )
            venta_save.save()
            return Response({'Msj': "Venta creada"})
        else: 
            return Response({'Msj': "Ingrese un estado correcto"})
    else:
        return Response({'Msj': "Error método no soportado"})

#Listar ventas de por estado (En curso > Finalizada > Cancelada)
#ENDPOINT FILTRAR LISTADO DE VENTA
@api_view(['GET'])
def ventas_venta_list_rest(request, format=None):    
    if request.method == 'GET':
        venta_list =  Venta2.objects.all().order_by('estado')
        venta_json = []
        for v in venta_list:
            venta_json.append({'nombreProducto':v.nombreProducto,'precioProducto':v.precioProducto,'cantidadProductos':v.cantidadProductos ,'montoTotal':v.montoTotal,'estado':v.estado, 'fecha':v.created})
        return Response({'Listado': venta_json})
    else:
        return Response({'Msj': "Error método no soportado"})

#Buscar venta por ID
#ENDPOINT DEVOLUCION
@api_view(['POST'])
def ventas_venta_get_element_rest(request, format=None):    
    if request.method == 'POST':
        venta_json = []
        venta_id = request.data['venta_id'] 
        venta_array = Venta2.objects.get(pk = venta_id)
        venta_json.append(
            {'id': venta_array.id,
             'nombreProducto': venta_array.nombreProducto,
             'precioProducto': venta_array.precioProducto,
             'cantidadProductos': venta_array.cantidadProductos,
             'montoTotal': venta_array.montoTotal,
             'estado': venta_array.estado,})
        return Response({venta_array.montoTotal:venta_json})
    else:
        return Response({'Msj': "Error método no soportado"})

#Actualizar registros de la venta
#ENDPOINT AÑADIR/QUITAR PRODUCTOS/CAMBIAR EL ESTADO
@api_view(['POST'])
def ventas_venta_update_element_rest(request, format=None):    
    if request.method == 'POST':
        venta_json = []
        venta_id = request.data['venta_id'] 
        nombreProducto = request.data['nombreProducto']
        precioProducto = request.data['precioProducto']
        cantidadProductos = request.data['cantidadProductos']
        estado = request.data['estado']
        if precioProducto <= 0:
            return Response({'Msj': "El precio no puede ser 0"})
        if nombreProducto == '' or estado == '' or precioProducto == '' or cantidadProductos == '' :
            return Response({'Msj': "Error los datos no pueder estar en blanco"})
        if estado == 'Finalizada' or estado == 'En curso' or estado == 'Rechazada': 
            Venta2.objects.filter(pk = venta_id).update(nombreProducto=nombreProducto) 
            Venta2.objects.filter(pk = venta_id).update(precioProducto=precioProducto)
            Venta2.objects.filter(pk = venta_id).update(cantidadProductos=cantidadProductos)
            Venta2.objects.filter(pk = venta_id).update(montoTotal=precioProducto*cantidadProductos)
            Venta2.objects.filter(pk = venta_id).update(estado=estado)
            return Response({'Msj': "Venta editada con éxito"})
        else:
            return Response({'Msj': "Ingrese un estado correcto"})
    else:
        return Response({'Msj': "Error método no soportado"})

#Borrar una venta
#ENDPOINT DE UTILIDAD PARA TESTING
@api_view(['POST'])
def ventas_venta_del_element_rest(request, format=None):    
    if request.method == 'POST':
        venta_id = request.data['venta_id'] 
        Venta2.objects.filter(pk = venta_id).delete()
        return Response({'Msj': "Venta eliminada con éxito"})
    else:
        return Response({'Msj': "Error método no soportado"})

#Buscar por fecha de creacion
@api_view(['POST'])
def ventas_venta_list_date_rest(request, format=None):    
    if request.method == 'POST':
        created = request.data['created']
        venta_list_count =  Venta2.objects.filter(created=created).count()
        if venta_list_count > 0:
            venta_list = Venta2.objects.filter(created=created).order_by('estado')
            venta_json = []
            for v in venta_list:
                venta_json.append({'nombreProducto':v.nombreProducto,'precioProducto':v.precioProducto,'cantidadProductos':v.cantidadProductos ,'montoTotal':v.montoTotal,'estado':v.estado, 'fecha':v.created})
            return Response({'Listado': venta_json})
        else:
            return Response({'Msj': 'No existen ventas creadas el '+str(created)})
    else:
        return Response({'Msj': 'Error método no soportado'})

#Buscar por un rango de fecha de creacion
@api_view(['POST'])
def ventas_venta_list_range_date_rest(request, format=None):    
    if request.method == 'POST':
        initial = request.data['initial']
        final = request.data['final']
        venta_list_count =  Venta2.objects.filter(created__range=(initial, final)).count()
        if venta_list_count > 0:
            venta_list = Venta2.objects.filter(created__range=(initial, final)).order_by('estado')
            venta_json = []
            for v in venta_list:
                venta_json.append({'nombreProducto':v.nombreProducto,'precioProducto':v.precioProducto,'cantidadProductos':v.cantidadProductos ,'montoTotal':v.montoTotal,'estado':v.estado, 'fecha':v.created})
            return Response({'Listado': venta_json})
        else:
            return Response({'Msj': 'No existen ventas creadas entre el '+str(initial)+' al'+ str(final)})
    else:
        return Response({'Msj': 'Error método no soportado'})

#Buscar venta por id o estado
@api_view(['POST'])
def ventas_venta_list_contains(request, format=None):
    if request.method == 'POST':
        search = request.data['search']
        venta_list_count = Venta2.objects.filter(Q(id__icontains=search)|Q(estado__icontains=search)).distinct()
        if venta_list_count:
            venta_list = Venta2.objects.filter(Q(id__icontains=search)|Q(estado__icontains=search)).distinct()
            venta_json = []
            for v in venta_list:
                venta_json.append({'nombreProducto':v.nombreProducto,'precioProducto':v.precioProducto,'cantidadProductos':v.cantidadProductos ,'montoTotal':v.montoTotal,'estado':v.estado, 'fecha':v.created})
            return Response({'Listado':venta_json})
        else:
            return Response({'Msj': 'No existen ventas que concuerden en id o nombre con la cadena ingresada'})
    else:
        return Response({'Msj':'Error método no soportado'})

#ENDPOINT CREAR DEVOLUCION 
@api_view(['POST'])
def ventas_devolucion_add_rest(request, format=None):    
    if request.method == 'POST':
        motivoDev = request.data['motivoDev']
        direccionDev = request.data['direccionDev'] 
        fechaDev = request.data['fechaDev'] 
        correoDev = request.data['correoDev']
        if motivoDev == '' or direccionDev == '' or fechaDev == '' or correoDev == '':
            return Response({'Msj': "Error: Ingrese los datos correctos para realizar la devolución"})               
        devolucion_save = Devolucion1(
            motivoDev = motivoDev,
            direccionDev = direccionDev,
            fechaDev = fechaDev,
            correoDev = correoDev,
            )
        devolucion_save.save()
        return Response({'Msj': "Devolucion creada"})
    else:
        return Response({'Msj': "Error método no soportado"})

#ENDPOINT BLOQUEAR/DESBLOQUEAR VENTA
@api_view(['POST'])
def ventas_venta_update_estado_rest(request, format=None):
    if request.method == 'POST':
        ventas_id= request.data['ventas_id']
        ventas_list = Venta2.objects.filter(pk=ventas_id)
        if not ventas_list:
            return Response({'Msj':'No existe una venta con el id ingresado'})
        for v in ventas_list:
            if v.bloqDes == 'Activo':
                Venta2.objects.filter(pk=ventas_id).update(bloqDes='Inactivo')
            else:
                Venta2.objects.filter(pk=ventas_id).update(bloqDes='Activo')
        return Response({'Msj':'Venta actualizada con éxito'})
    else:
        return Response({'Msj':'Error método no soportado'})
    


    #####################EXpoortar pdf#############################
def crea_pdf(template_name, dic={}):
    template = get_template(template_name)
    html = template.render(dic)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)
    return HttpResponse(result.getvalue(), content_type='application/pdf')

@login_required
def pdf_cotizacion(request):
    venta = Venta2.objects.all()
    diccionario = []
    for venta2 in venta:
        venta_dict = {
            'nombreProducto': venta2.nombreProducto,
            'precioProducto': venta2.precioProducto,
            'cantidadProductos': venta2.cantidadProductos,
            'montoTotal': venta2.montoTotal,
            'estado': venta2.estado,
        }
        diccionario.append(venta_dict)

    pdf = crea_pdf('ventas/pdf_cotizacion.html', diccionario)
    return HttpResponse(pdf, content_type='application/pdf')



@login_required
def dashboard_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'ventas/dashboard_main.html'
    return render(request,template_name,{'profile':profile})


@login_required
def dashboard(request):

    estado_count = Venta2.objects.all().count()

    producto_count = Product.objects.all().count()

    rate_heroes_habilidad = producto_count / estado_count
    estado_total = estado_count
    cantidadProductos = Venta2.objects.filter(cantidadProductos =0).count()
    montoTotal = Venta2.objects.filter(montoTotal=0).count()
    estado = Venta2.objects.filter(estado=1).count()
    
    suma_habilidades = cantidadProductos + montoTotal + estado
    data_rate = round(float((suma_habilidades/estado_total)*100),1)
    data_set = [cantidadProductos,montoTotal,estado]
    data_label = ['Cantidad Producto','Monto Total ','Estado']
    data_color = ['#338AFF','#FA1A3C','#28B463']
    
    ventas_list = Venta2.objects.all()
    data_set_todos_niveles = []
    data_label_todos_niveles = []
    data_label_todos_niveles.append('Total')
    data_set_todos_niveles.append(estado_total)
    for i in ventas_list:
        data_label_todos_niveles.append('Nivel'+str(i.estado))
        data_set_todos_niveles.append(i.estado) 

    template_name = 'dashboard.html'
    return render(request,template_name,{'estado_count':estado_count,'producto_count':producto_count,'rate_heroes_habilidad':rate_heroes_habilidad,'data_rate':data_rate,'data_set':data_set,'data_label':data_label,'data_color':data_color,'data_set_todos_niveles':data_set_todos_niveles,'data_label_todos_niveles':data_label_todos_niveles})




def exportar_a_pdf(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)

    response = HttpResponse(contenttype='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cotizacion{cotizacion.id}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)
    p.drawString(50, 800, f'Nombre: {cotizacion.nombre}')
    p.drawString(50, 780, f'Email: {cotizacion.email}')
    p.drawString(50, 760, f'Descripción: {cotizacion.descripcion}')
    p.showPage()
    p.save()

    return response