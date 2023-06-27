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
from .forms import ProductForm
from django.urls import reverse
from registration.models import Profile
from inventario.models import Product, Category,Insumos
import json
import pandas as pd
import xlwt
import traceback
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import os 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 



# Create your views here.
@login_required
def inventario_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/inventario_main.html'
    return render(request,template_name,{'profiles':profiles})

@login_required
def crear_producto(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    category_list = Category.objects.all().order_by('category_name')
    template_name = 'inventario/crear_producto.html'
    return render(request,template_name,{'profile':profile,'category_list':category_list})

@login_required
def producto_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')       
        product_state = request.POST.get('product_state')
        product_category_id = request.POST.get('category_name') 
        if product_name == '' or product_price == '' or product_state == '' or product_category_id == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('crear_producto')
        category =Category.objects.get(id=product_category_id)
        producto_save = Product(
            product_name=product_name,
            product_price=product_price,
            product_state=product_state,
            product_category=category,
        )
        producto_save.save()
        messages.add_message(request, messages.INFO, 'Producto ingresado con éxito')
        return redirect('inventario_main')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')


    
@login_required
def producto_ver(request, product_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    product_data = Product.objects.get(pk=product_id)
    category_list = Category.objects.all()
    selected_category = product_data.product_category
    template_name = 'inventario/producto_ver.html'
    return render(request, template_name, {'profile': profile, 'product_data': product_data, 'category_list': category_list, 'selected_category': selected_category})



    
@login_required
def producto_list(request, page=None, search=None):
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
        p_count = Product.objects.filter(product_name='a').count()
        p_list_array = Product.objects.all().order_by('product_name')
    else:
        p_count = Product.objects.filter(product_name='a').filter(product_name__icontains=search).count()
        p_list_array = Product.objects.all().filter(product_name__icontains=search).order_by('product_name')

    p_list = []
    for p in p_list_array:
        p_list.append({
            'id': p.id,
            'product_name': p.product_name,
            'product_price': p.product_price,
            'product_state': p.product_state,
            'category_name': p.product_category.category_name, # aquí se obtiene el category_name asociado al producto
        })

    paginator = Paginator(p_list, 5)
    p_list_paginate = paginator.get_page(page)

    template_name = 'inventario/producto_list.html'
    return render(request, template_name, {'template_name': template_name, 'p_list_paginate': p_list_paginate, 'paginator': paginator, 'page': page})


@login_required
def producto_edit(request, product_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':

        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_state = request.POST.get('product_state')
        product_category_id = request.POST.get('product_category')
        
        product.product_name = product_name
        product.product_price = product_price
        product.product_state = product_state
        product.product_category_id = product_category_id
        product.save()
        
        return redirect('producto_ver', product_id=product.id)
    else:
        product_data = Product.objects.get(pk=product_id)
        categories = Category.objects.all()
        
        template_name= 'inventario/producto_ver.html'
        
        return render(request, template_name, {'product_data': product_data, 'categories': categories})

    

def producto_delete(request, product_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Producto eliminado correctamente')
    return redirect(reverse('producto_list'))


    
@login_required
def carga_masiva_producto(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/carga_masiva_producto.html'
    return render(request,template_name,{'profiles':profile})

@login_required
def import_file_producto(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion_productos.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Product_name','product_price','product_state','product_image']
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
                ws.write(row_num, col_num, 'ej: Nombre producto' , font_style)
            if col_num == 1:                           
                ws.write(row_num, col_num, '1000' , font_style)
            if col_num == 2:                           
                ws.write(row_num, col_num, 'Nuevo' , font_style)
    wb.save(response)
    return response  

@login_required
def carga_masiva_producto_save(request):
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
            product_name = str(item[1])            
            product_price = int(item[2])
            product_state = str(item[3])
            producto_save = Product(
                product_name = product_name,            
                product_price = product_price,
                product_state = product_state,
  
                )
            producto_save.save()
        messages.add_message(request, messages.INFO, 'Carga masiva finalizada, se importaron '+str(acc)+' registros')
        return redirect('carga_masiva_producto')
    
@login_required
def descarga_reporte_producto(request):
    try:    
        profiles = Profile.objects.get(user_id = request.user.id)
        if profiles.group_id != 1:
         messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
         return redirect('check_group_main')
    
        style_2 = xlwt.easyxf('font: name Time New Roman, color-index black; font: bold on')

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        response=HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ListaProductos.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Productos')

        row_num = 0
        columns = ['Nombre', 'Precio', 'Estado','Categoria']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num] ,font_style)

        productos = Product.objects.all().order_by('product_name')

        for row in productos:
            row_num += 1
            for col_num in range(4):
                if col_num == 0:
                    ws.write(row_num, col_num, row.product_name, style_2)
                if col_num == 1:
                    ws.write(row_num, col_num, row.product_price, style_2)   
                if col_num == 2:
                    ws.write(row_num, col_num, row.product_state, style_2)
                if col_num == 3:
                    ws.write(row_num, col_num, str(row.product_category), style_2)

        
        wb.save(response)
        return response
    except Exception:
            traceback.print_exc()
            messages.add_message(request, messages.ERROR, 'Se produjo un error al generar el archivo Excel. Por favor, inténtelo de nuevo más tarde.')
            return redirect('producto_list')

@login_required
def reportes_main_productos(request):
    try:
        profiles = Profile.objects.get(user_id = request.user.id)
        if profiles.group_id != 1:
            messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
            return redirect('check_group_main')
        
        template_name = 'inventario/reportes_main_productos.html'
        return render(request,template_name)
    except:
        messages.add_message(request, messages.INFO, 'Error al acceder al pagina de reportes')
        return redirect('producto_list')


@login_required
def reporte_producto_filtro(request):
    try:
        profiles = Profile.objects.get(user_id=request.user.id)
        if profiles.group_id != 1:
            messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
            return redirect('check_group_main')

        if request.method == 'POST':
            producto = request.POST.get('product_name')
            if len(producto) == 0:
                messages.add_message(request, messages.INFO, 'El producto no puede estar vacío')
                return redirect('reportes_main_productos')
            producto_count = Product.objects.filter(estado='Activo').filter(product_name__icontains=producto).count()
            if producto_count < 1:
                messages.add_message(request, messages.INFO, 'No existe producto con la cadena buscada')
                return redirect('reportes_main')

            style_1 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on', num_format_str='#,##0.00')
            style_2 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on')
            

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="ReporteProductos.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Productos')

            row_num = 0
            columns = ['Nombre', 'Precio', 'Estado', 'Categoria']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], style_2)

            productos_array = Product.objects.filter(estado='Activo').filter(product_name__icontains=producto)
            for row in productos_array:
                row_num += 1
                for col_num in range(4):
                    if col_num == 0:
                        ws.write(row_num, col_num, row.product_name, style_2)
                    if col_num == 1:
                        ws.write(row_num, col_num, row.product_price, style_2)
                    if col_num == 2:
                        ws.write(row_num, col_num, row.product_state, style_2)
                    if col_num == 3:
                        ws.write(row_num, col_num, str(row.product_category), style_2)

            wb.save(response)
            return response
        else:
            messages.add_message(request, messages.INFO, 'Error')
            return redirect('check_group_main')
    except:
        messages.add_message(request, messages.INFO, 'Error al generar el reporte')
        return redirect('reportes_main_productos')
   


############################ CATEGORIAS ###############################


def crear_category(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/crear_category.html'
    return render(request,template_name,{'profile':profile})

@login_required
def category_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        category_name = request.POST.get('category_name')  
        if category_name == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('crear_category')
        category_save = Category(
            category_name = category_name
            )
        category_save.save()
        messages.add_message(request, messages.INFO, 'Categoria ingresada con éxito')
        return redirect('inventario_main')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')
    
@login_required
def category_ver(request,category_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    category_data = Category.objects.get(pk=category_id)
    template_name = 'inventario/category_ver.html'
    return render(request,template_name,{'profile':profile,'category_data':category_data})

    
@login_required
def category_list(request,page=None,search=None):
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
    c_list = []
    if search == None or search == "None":
        c_count = Category.objects.filter(category_name='a').count()
        c_list_array = Category.objects.all().order_by('category_name')
        for c in c_list_array:
            c_list.append({'id':c.id,'category_name':c.category_name})
    else:
        c_count = Category.objects.filter(category_name='a').filter(category_name__icontains=search).count()
        c_list_array = Category.objects.all().filter(category_name__icontains=search).order_by('category_name')
        for c in c_list_array:
            c_list.append({'id':c.id,'category_name':c.category_name})
    paginator = Paginator(c_list, 5) 
    c_list_paginate= paginator.get_page(page)   
    template_name = 'inventario/category_list.html'
    return render(request,template_name,{'template_name':template_name,'c_list_paginate':c_list_paginate,'paginator':paginator,'page':page})

@login_required
def category_edit(request, category_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':

        category_name = request.POST.get('category_name')



        category.category_name = category_name

        category.save()


        
        return redirect('category_ver', category_id=category.id)
    else:
        category_data = Category.objects.get(pk=category_id)

        template_name= 'inventario/category_ver.html'
        return render(request, template_name, {'category_data': category_data})
    

def category_delete(request, category_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, 'Categoria eliminado correctamente')
    return redirect(reverse('category_list'))

@login_required
def carga_masiva_category(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/carga_masiva_category.html'
    return render(request,template_name,{'profiles':profile})

@login_required
def import_file_category(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion_categorias.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Category_name']
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
                ws.write(row_num, col_num, 'ej: Nombre Categoria' , font_style)
    wb.save(response)
    return response  

@login_required
def carga_masiva_category_save(request):
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
            category_name = str(item[1])            
            category_save = Category(
                category_name = category_name,            

  
                )
            category_save.save()
        messages.add_message(request, messages.INFO, 'Carga masiva finalizada, se importaron '+str(acc)+' registros')
        return redirect('carga_masiva_producto') 
    





############################ INSUMOS ###############################
@login_required
def insumos_main(request):
    profiles = Profile.objects.get(user_id = request.user.id)
    if profiles.group_id != 1 and profiles.group_id != 2:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'inventario/insumos_main.html'
    return render(request,template_name,{'profiles':profiles})

@login_required
def crear_insumos(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    category_list = Category.objects.all().order_by('category_name')
    template_name = 'inventario/crear_insumos.html'
    return render(request,template_name,{'profile':profile,'category_list':category_list})

@login_required
def insumos_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        insumos_name = request.POST.get('insumos_name')
        insumos_price = request.POST.get('insumos_price')       
        insumos_state = request.POST.get('insumos_state')
        insumos_category_id = request.POST.get('category_name')
        if insumos_name == '' or insumos_price == '' or insumos_state == '' or insumos_category_id == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('crear_insumos')
        
        category = Category.objects.get(id=insumos_category_id)
        insumos_save = Insumos(
            insumos_name=insumos_name,
            insumos_price=insumos_price,
            insumos_state=insumos_state,
            insumos_categorys=category,  # Asigna la categoría al campo insumos_category

        )
        insumos_save.save()
        messages.add_message(request, messages.INFO, 'Insumo ingresado con éxito')
        return redirect('inventario_main')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')
@login_required
def insumos_ver(request, insumos_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    insumos_data = Insumos.objects.get(pk=insumos_id)
    category_list = Category.objects.all()
    selected_category = insumos_data.insumos_categorys
    template_name = 'inventario/insumos_ver.html'
    return render(request, template_name, {'profile': profile, 'insumos_data': insumos_data, 'category_list': category_list, 'selected_category': selected_category})



    
@login_required
def insumos_list(request, page=None, search=None):
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
        p_count = Insumos.objects.filter(insumos_name='a').count()
        p_list_array = Insumos.objects.all().order_by('insumos_name')
    else:
        p_count = Insumos.objects.filter(insumos_name='a').filter(insumos_name__icontains=search).count()
        p_list_array = Insumos.objects.all().filter(insumos_name__icontains=search).order_by('insumos_name')

    p_list = []
    for p in p_list_array:
        p_list.append({
            'id': p.id,
            'insumos_name': p.insumos_name,
            'insumos_price': p.insumos_price,
            'insumos_state': p.insumos_state,
            'category_name': p.insumos_categorys.category_name, # aquí se obtiene el category_name asociado al producto
        })

    paginator = Paginator(p_list, 5)
    p_list_paginate = paginator.get_page(page)

    template_name = 'inventario/insumos_list.html'
    return render(request, template_name, {'template_name': template_name, 'p_list_paginate': p_list_paginate, 'paginator': paginator, 'page': page})
@login_required


def insumos_edit(request, insumos_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    insumos = get_object_or_404(Insumos, id=insumos_id)
    
    if request.method == 'POST':

        insumos_name = request.POST.get('insumos_name')
        insumos_price = request.POST.get('insumos_price')
        insumos_state = request.POST.get('insumos_state')
        insumos_category_id = request.POST.get('insumos_category')

        insumos.insumos_name = insumos_name
        insumos.insumos_price = insumos_price
        insumos.insumos_state = insumos_state
        insumos.insumos_category_id= insumos_category_id
        insumos.save()
        
        return redirect('insumos_ver', insumos_id=insumos.id)
    else:
        insumos_data = Insumos.objects.get(pk=insumos_id)
        categories = Category.objects.all()
        
        template_name= 'inventario/insumo_ver.html'
        
        return render(request, template_name, {'insumos_data': insumos_data, 'categories': categories})

    

def insumos_delete(request, insumos_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    insumos = get_object_or_404(Insumos, id=insumos_id)
    insumos.delete()
    messages.success(request, 'Insumo eliminado correctamente')
    return redirect(reverse('insumos_list'))

@login_required
def descarga_reporte_insumo(request):
    try:    
        profiles = Profile.objects.get(user_id = request.user.id)
        if profiles.group_id != 1:
         messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
         return redirect('check_group_main')
    
        style_2 = xlwt.easyxf('font: name Time New Roman, color-index black; font: bold on')

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        response=HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ListaInsumos.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Insumos')

        row_num = 0
        columns = ['Nombre', 'Precio', 'Estado','Categoria']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num] ,font_style)

        insumos = Insumos.objects.all().order_by('insumos_name')

        for row in insumos:
            row_num += 1
            for col_num in range(4):
                if col_num == 0:
                    ws.write(row_num, col_num, row.insumos_name, style_2)
                if col_num == 1:
                    ws.write(row_num, col_num, row.insumos_price, style_2)   
                if col_num == 2:
                    ws.write(row_num, col_num, row.insumos_state, style_2)
                if col_num == 3:
                    ws.write(row_num, col_num, str(row.insumos_categorys), style_2)

        
        wb.save(response)
        return response
    except Exception:
            traceback.print_exc()
            messages.add_message(request, messages.ERROR, 'Se produjo un error al generar el archivo Excel. Por favor, inténtelo de nuevo más tarde.')
            return redirect('insumos_list')
    
@login_required
def reportes_main_insumo(request):
    try:
        profiles = Profile.objects.get(user_id = request.user.id)
        if profiles.group_id != 1:
            messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
            return redirect('check_group_main')
        
        template_name = 'inventario/reportes_main_insumo.html'
        return render(request,template_name)
    except:
        messages.add_message(request, messages.INFO, 'Error al acceder al pagina de reportes')
        return redirect('insumos_list')


@login_required
def reporte_insumo_filtro(request):
    try:
        profiles = Profile.objects.get(user_id=request.user.id)
        if profiles.group_id != 1:
            messages.add_message(request, messages.INFO, 'Intenta ingresar a un área para la que no tiene permisos')
            return redirect('check_group_main')

        if request.method == 'POST':
            insumos = request.POST.get('insumos_name')
            if len(insumos) == 0:
                messages.add_message(request, messages.INFO, 'El producto no puede estar vacío')
                return redirect('reportes_main_insumo')
            insumos_count = Insumos.objects.filter(estado='Activo').filter(insumos_name__icontains=insumos).count()
            if insumos_count < 1:
                messages.add_message(request, messages.INFO, 'No existe producto con la cadena buscada')
                return redirect('reportes_main:insumo')

            style_1 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on', num_format_str='#,##0.00')
            style_2 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on')
            

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="ReporteInsumos.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Insumos')

            row_num = 0
            columns = ['Nombre', 'Precio', 'Estado', 'Categoria']
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], style_2)

            insumos_array = Insumos.objects.filter(estado='Activo').filter(insumos_name__icontains=insumos)
            for row in  insumos_array:
                row_num += 1
                for col_num in range(4):
                    if col_num == 0:
                        ws.write(row_num, col_num, row.insumos_name, style_2)
                    if col_num == 1:
                        ws.write(row_num, col_num, row.insumos_price, style_2)
                    if col_num == 2:
                        ws.write(row_num, col_num, row.insumos_state, style_2)
                    if col_num == 3:
                        ws.write(row_num, col_num, str(row.insumos_category), style_2)

            wb.save(response)
            return response
        else:
            messages.add_message(request, messages.INFO, 'Error')
            return redirect('check_group_main')
    except:
        messages.add_message(request, messages.INFO, 'Error al generar el reporte')
        return redirect('reportes_main_insumo')



    ########################## email #######################################
@login_required
def correo1(request):
    #llamos al metodo que envia el correo
    send_mail_ejemplo2(request,'correo.mypyme@gmail.com','')
    messages.add_message(request, messages.INFO, 'correo enviado')
    return redirect('inventario_main')   
@login_required
def send_mail_ejemplo2(request,mail_to,data_1):
    #Ejemplo que permite enviar un correo agregando un excel creado con info de la bd


    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))#directorio base del proyecto en el servidor
    BASE_PATH = os.path.join(BASE_DIR,"core","static","core")#lugar donde se guarda el archivo
    file_name = "Estado_Ventas.xls"#trate de que no se muy largo
    file_send = BASE_PATH+"/"+file_name
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('diosito salvame')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True   
    columns = ['Nombre','Precio','estado','categoria']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
        style_2 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on')
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    time_format = xlwt.XFStyle()
    time_format.num_format_str = 'hh:mm:ss'   
    insumos = Insumos.objects.all().order_by('insumos_name')

    for row in insumos:
        row_num += 1
        for col_num in range(4):
            if col_num == 0:
                ws.write(row_num, col_num, row.insumos_name, style_2)
            if col_num == 1:
                ws.write(row_num, col_num, row.insumos_price, style_2)   
            if col_num == 2:
                ws.write(row_num, col_num, row.insumos_state, style_2)
            if col_num == 3:
                ws.write(row_num, col_num, str(row.insumos_categorys), style_2)                                         
    wb.save(file_send)  
    #fin archivo
    from_email = settings.DEFAULT_FROM_EMAIL #exporta desde el settings.py, el correo de envio por defecto
    subject = "Ventas Mypyme"    
    html_content = """
                    <html>
                        <head>
                            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                        </head>
                        <body>
                            <h3>Estimad@</h3>
                            <p>Le adjuntamos el excel con los insumos en la bodega """+str(data_1)+"""  .</p>
                            <p>Se despide cordialmente MyPyme .</p>
                            <p><small>Correo generado automáticamente, por favor no responder.<small></p>
                        </body>
                    </html>            
                """
    msg = EmailMultiAlternatives(subject, html_content, from_email, [mail_to])
    msg.content_subtype = "html"
    msg.attach_alternative(html_content, "text/html")

    msg = EmailMultiAlternatives(subject, html_content, from_email, [mail_to])
    msg.content_subtype = "html"
    archivo_adjunto = open(file_send,'rb')
    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto    
    adjunto_MIME.add_header('Content-Disposition',"attachment; filename= %s" % file_name)
    # Y finalmente lo agregamos al mensaje
    msg.attach(adjunto_MIME)


    msg.send()


