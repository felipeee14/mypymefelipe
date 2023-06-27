from django.shortcuts import render, redirect
from .models import Cotizacion
from inventario.models import Product, Category
from proveedores.models import Proveedor
from registration.models import Profile
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Cotizacion, ProductCotizacion
from inventario.models import Product
from proveedores.models import Proveedor

def cotizaciones_main(request):
    cotizaciones = Cotizacion.objects.all()
    return render(request, 'cotizacion/cotizaciones_main.html', {'cotizaciones': cotizaciones})


def find_product_cotizacion_by_id(product_cotizaciones, product_id):
    for product_cotizacion in product_cotizaciones:
        if product_cotizacion.product.id == product_id:
            return product_cotizacion
    return None
def replace_product_cotizacion_by_id(product_cotizaciones, product_id, new_product_cotizacion):
    for index, product_cotizacion in enumerate(product_cotizaciones):
        if product_cotizacion.product.id == product_id:
            product_cotizaciones[index] = new_product_cotizacion
            break


def crear_cotizacion(request):
    # Obtener la lista de clientes
    client_list = Proveedor.objects.all().order_by('proveedor_name')
    product_list = Product.objects.all().order_by('product_name')
    cart_items = []
    def addProductQuantity(id):
        target_product_cotizacion = find_product_cotizacion_by_id(cart_items, id)
        target_product_cotizacion.quantity +=1
        replace_product_cotizacion_by_id(cart_items,id,target_product_cotizacion)


    if request.method == 'POST':
        # Obtener los datos del formulario
        proveedor_id = request.POST.get('provider')
        product_id = request.POST.get('product')
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_state = request.POST.get('product_state')
        category_id = request.POST.get('category_name')

        # Crear o recuperar el proveedor seleccionado
        proveedor = Proveedor.objects.get(id=proveedor_id)
        product = Product.objects.get(id=product_id)


        # Crear la cotización y guardarla en la base de datos
        cotizacion = Cotizacion.objects.create(
            proveedor=proveedor,
            total=0  # El precio total se calculará más adelante
        )
        target_product_cotizacion = find_product_cotizacion_by_id(cart_items, product_id)

        if target_product_cotizacion is None:
            # Se encontró el objeto ProductCotizacion con el ID buscado
            product_cotizacion = ProductCotizacion.objects.create(
                cotizacion=cotizacion,
                product=product,
                quantity=1,
                monto_total=product.product_price
            )
            cart_items.append(product_cotizacion)
        # Redireccionar a la lista de cotizaciones

    return render(request, 'cotizacion/crear_cotizacion.html', {'client_list': client_list, 'product_list': product_list,"cart_items":cart_items,"addProductQuantity":addProductQuantity})



def lista_cotizacion(request):
    cotizaciones = Cotizacion.objects.all()
    return render(request, 'cotizacion/lista_cotizacion.html', {'cotizaciones': cotizaciones})

def cotizacion_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        proveedor_id = request.POST.get('provider')
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')       
        product_state = request.POST.get('product_state')
        product_category_id = request.POST.get('category_name') 
        if product_name == '' or product_price == '' or product_state == '' or product_category_id == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('crear_cotizacion')
        category =Category.objects.get(id=product_category_id)
        proveedor = Proveedor.objects.get(id=proveedor_id)
        producto_save = Product(
            product_name=product_name,
            product_price=product_price,
            product_state=product_state,
            product_category=category,
        )
        cotizacion_save.save()
        messages.add_message(request, messages.INFO, 'Producto ingresado con éxito')
        return redirect('cotizaciones_main')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')
    