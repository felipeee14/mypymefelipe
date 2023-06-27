from django.shortcuts import render
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, GroupManager, User
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.urls import reverse
import json
import pandas as pd
import xlwt
from datetime import datetime
from django.http import HttpResponse
import traceback
import os


from registration.models import Profile
from proveedores.models import Proveedor
# Create your views here.
@login_required
def proveedores_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/proveedores_main.html'
    return render(request,template_name,{'profiles':profiles})

@login_required
def proveedores_crear(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/proveedores_crear.html'
    return render(request,template_name,{'profiles':profiles})

login_required
def proveedor_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        proveedor_name = request.POST.get('proveedor_name')
        proveedor_mail = request.POST.get('proveedor_mail')       
        proveedor_phone= request.POST.get('proveedor_phone')
        if proveedor_name == '' or proveedor_mail == '' or proveedor_phone ==  '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('proveedores_main')

        proveedor_save = Proveedor(
            proveedor_name=proveedor_name,
            proveedor_mail=proveedor_mail,
            proveedor_phone=proveedor_phone,

        )
        proveedor_save.save()
        messages.add_message(request, messages.INFO, 'Proveedor ingresado con éxito')
        return redirect('proveedores_main')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')
    
@login_required
def proveedor_list(request, page=None, search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if page is None:
        page = request.GET.get('page')
    else:
        page = page

    if request.GET.get('page') is None:
        page = page
    else:
        page = request.GET.get('page')

    if search is None:
        search = request.GET.get('search')
    else:
        search = search

    if request.GET.get('search') is None:
        search = search
    else:
        search = request.GET.get('search')

    if request.method == 'POST':
        search = request.POST.get('search')
        page = None

    if search is None or search == "None":
        p_count = Proveedor.objects.filter(proveedor_name='a').count()
        p_list_array = Proveedor.objects.all().order_by('proveedor_name')
    else:
        p_count = Proveedor.objects.filter(proveedor_name='a').filter(proveedor_name__icontains=search).count()
        p_list_array = Proveedor.objects.all().filter(proveedor_name__icontains=search).order_by('proveedor_name')

    p_list = []
    for p in p_list_array:
        p_list.append({
            'id': p.id,
            'proveedor_name': p.proveedor_name,
            'proveedor_mail': p.proveedor_mail,
            'proveedor_phone': p.proveedor_phone,
        })

    paginator = Paginator(p_list, 5)
    p_list_paginate = paginator.get_page(page)

    template_name = 'proveedores/proveedor_list.html'
    return render(request, template_name, {'template_name': template_name, 'p_list_paginate': p_list_paginate, 'paginator': paginator, 'page': page})


@login_required
def proveedor_ver(request, proveedor_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedor_data = Proveedor.objects.get(pk=proveedor_id)
    template_name = 'proveedores/proveedor_ver.html'
    return render(request, template_name, {'profile': profile, 'proveedor_data': proveedor_data,})

@login_required
def proveedor_edit(request, proveedor_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    
    if request.method == 'POST':

        proveedor_name = request.POST.get('proveedor_name')
        proveedor_mail = request.POST.get('proveedor_mail')
        proveedor_phone = request.POST.get('proveedor_phone')
        
        proveedor.proveedor_name = proveedor_name
        proveedor.proveedor_mail = proveedor_mail
        proveedor.proveedor_phone = proveedor_phone
        proveedor.save()
        
        return redirect('proveedor_ver', proveedor_id=proveedor.id)
    else:
        proveedor_data = proveedor.objects.get(pk=proveedor_id)
        
        template_name= 'proveedores/proveedor_ver.html'
        
        return render(request, template_name, {'proveedor_data': proveedor_data})


def proveedor_delete(request, proveedor_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    proveedor.delete()
    messages.success(request, 'Proveedor eliminado correctamente')
    return redirect(reverse('proveedor_list'))
    

@login_required
def carga_masiva_proveedor(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/carga_masiva_proveedor.html'
    return render(request,template_name,{'profiles':profile})

@login_required
def import_file_proveedor(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion_proveedors.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['proveedor_name','proveedor_mail','proveedor_phone']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(3):
            if col_num == 0:
                ws.write(row_num, col_num, 'ej: Nombre proveedor' , font_style)
            if col_num == 1:                           
                ws.write(row_num, col_num, 'abc@gmail.com' , font_style)
            if col_num == 2:                           
                ws.write(row_num, col_num, '55642334' , font_style)
    wb.save(response)
    return response  

@login_required
def carga_masiva_proveedor_save(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        #try:
        print(request.FILES['myfile'])
        data = pd.read_excel(request.FILES['myfile'])
        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():    
            proveedor_name = str(item[1])            
            proveedor_mail = str(item[2])
            proveedor_phone = str(item[3])
            proveedor_save = Proveedor(
                proveedor_name = proveedor_name,            
                proveedor_mail = proveedor_mail,
                proveedor_phone = proveedor_phone,
  
                )
            proveedor_save.save()
        messages.add_message(request, messages.INFO, 'Carga masiva finalizada, se importaron '+str(acc)+' registros')
        return redirect('carga_masiva_proveedor')
    
@login_required
def descarga_reporte(request):
    try:    
        profiles = Profile.objects.get(user_id = request.user.id)
        if profiles.group_id != 1:
         messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
         return redirect('check_group_main')
    
        style_2 = xlwt.easyxf('font: name Time New Roman, color-index black; font: bold on')

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        response=HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ListaProveedores.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Proveedores')

        row_num = 0
        columns = ['Nombre', 'Mail', 'Telefono']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num] ,font_style)

        proveedores = Proveedor.objects.all().order_by('proveedor_name')

        for row in proveedores:
            row_num += 1
            for col_num in range(3):
                if col_num == 0:
                    ws.write(row_num, col_num, row.proveedor_name, style_2)
                if col_num == 1:
                    ws.write(row_num, col_num, row.proveedor_mail, style_2)   
                if col_num == 2:
                    ws.write(row_num, col_num, row.proveedor_phone, style_2)

        
        wb.save(response)
        return response
    except Exception:
            traceback.print_exc()
            messages.add_message(request, messages.ERROR, 'Se produjo un error al generar el archivo Excel. Por favor, inténtelo de nuevo más tarde.')
            return redirect('proveedor_list')
#