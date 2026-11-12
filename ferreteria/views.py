from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Producto, Categoria, Compra, DetalleCompra
from decimal import Decimal
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Count, Sum, Avg
from .forms import ConsultaClienteForm

# Create your views here.

def inicio(request):
    # [:8] sirve para dejar solo los 8 primeros productos en la pagina de inicio.
    productos = Producto.objects.select_related('categoria').all()[:8]

    carrito = request.session.get('carrito', {})
    total_items_carrito = sum(carrito.values())

    context = {
        "productos": productos,
        "total_items_carrito": total_items_carrito
    }

    return render(request, 'inicio.html', context)

def catalogo(request):
    productos = Producto.objects.all()
    categoria = Categoria.objects.all()

    carrito = request.session.get('carrito', {})
    total_items_carrito = sum(carrito.values())

    context = {
        "productos": productos,
        "categoria": categoria,
        "total_items_carrito": total_items_carrito
    }

    return render(request, "catalogo.html", context)

def ver_carrito(request):
    carrito = request.session.get('carrito', {})

    items_carrito = []
    subtotal_neto = Decimal("0")

    for prod_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=prod_id)
            subtotal = producto.precio * cantidad
            subtotal_neto += subtotal

            items_carrito.append({
                "producto": producto,
                "cantidad": cantidad,
                "subtotal": subtotal
            })

        except Producto.DoesNotExist:
            continue

    total_iva = round(subtotal_neto * Decimal("0.19"))
    total_general = subtotal_neto + total_iva
    total_items_carrito = sum(carrito.values())

    context = {
        "items_carrito": items_carrito,
        "subtotal_neto": subtotal_neto,
        "total_iva": total_iva,
        "total_general": total_general,
        "total_items_carrito": total_items_carrito
    }

    return render(request, "carrito.html", context)

def agregar_al_carrito(request, producto_id):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        str_id = str(producto_id)
        cantidad = int(request.POST.get('cantidad', 1))

        carrito[str_id] = carrito.get(str_id, 0) + cantidad
        request.session['carrito'] = carrito
        request.session.modified = True

        total_items = sum(carrito.values())

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'total_items': total_items})

    return redirect('/ferreteria/carrito/')

def actualizar_carrito(request, producto_id):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        str_id = str(producto_id)
        cantidad = int(request.POST.get('cantidad', 1))

        if cantidad > 0:
            carrito[str_id] = cantidad
        else:
            carrito.pop(str_id, None)

        request.session['carrito'] = carrito
        request.session.modified = True

        total_items = sum(carrito.values())

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'total_items': total_items})

    return redirect('/ferreteria/carrito/')

def eliminar_del_carrito(request, producto_id):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        str_id = str(producto_id)

        if str_id in carrito:
            del carrito[str_id]
            request.session['carrito'] = carrito
            request.session.modified = True

        total_items = sum(carrito.values())

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'total_items': total_items})

    return redirect('/ferreteria/carrito/')

def vaciar_carrito(request):
    if request.method == 'POST':
        request.session['carrito'] = {}
        request.session.modified = True

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'total_items': 0})

    return redirect('/ferreteria/carrito/')

@transaction.atomic # Evita que se guarde una compra a medias si falla el código
def compra(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        
        if not carrito:
            return JsonResponse({'ok': False, 'mensaje': 'El carrito está vacío.'})

        usuario_actual = request.user 

        # 2. Crear el registro maestro de la Compra
        nueva_compra = Compra.objects.create(
            usuario=usuario_actual,
            estado='pagada',
            total=Decimal("0") 
        )

        subtotal_neto = Decimal("0")

        for prod_id, cantidad in carrito.items():
            try:
                producto = Producto.objects.get(id=int(prod_id))
                cantidad_int = int(cantidad)
                
                # Descontar stock
                producto.stock = max(0, producto.stock - cantidad_int)
                producto.save()

                # Calcular total
                subtotal = producto.precio * cantidad_int
                subtotal_neto += subtotal

                # Crear el registro del detalle en la BD
                DetalleCompra.objects.create(
                    compra=nueva_compra,
                    producto=producto,
                    cantidad=cantidad_int,
                    precio_unitario=producto.precio
                )

            except (Producto.DoesNotExist, ValueError):
                continue

        total_iva = round(subtotal_neto * Decimal("0.19"))
        nueva_compra.total = subtotal_neto + total_iva
        nueva_compra.save()

        # 5. Vaciar el carrito de la sesión
        request.session['carrito'] = {}
        request.session.modified = True

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'mensaje': 'Compra Exitosa registrada en la BD'})

    return redirect('/ferreteria/carrito/')

class ProductoCreateView(CreateView):
    model = Producto
    fields = ['nombre', 'categoria', 'imagen', 'precio', 'stock']
    template_name = 'producto_form.html'
    success_url = reverse_lazy('catalogo')

class ProductoUpdateView(UpdateView):
    model = Producto
    fields = ['nombre', 'categoria', 'imagen', 'precio', 'stock']
    template_name = 'producto_form.html'
    success_url = reverse_lazy('catalogo')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'producto_confirm_delete.html'
    success_url = reverse_lazy('catalogo')
    
def reporte_agrupado(request):
    # Reporte 1: Agrupa por categoría y calcula el total de stock y precio promedio
    resumen_categorias = Producto.objects.values('categoria__nombre').annotate(
        cantidad_productos=Count('id'),
        total_stock=Sum('stock'),
        precio_promedio=Avg('precio')
    ).order_by('categoria__nombre')
    
    return render(request, 'reporte_agrupado.html', {'reportes': resumen_categorias})

def reporte_stock_critico(request):
    # Reporte 2: Filtra productos con stock menor o igual a 5 (crítico) y los ordena
    productos_criticos = Producto.objects.filter(stock__lte=5).order_by('stock', 'nombre')
    
    return render(request, 'reporte_stock.html', {'productos': productos_criticos})

def contacto_cliente(request):
    # Funcionalidad con sesiones: Contador de visitas a la sección de contacto
    visitas = request.session.get('visitas_contacto', 0)
    request.session['visitas_contacto'] = visitas + 1

    if request.method == 'POST':
        form = ConsultaClienteForm(request.POST)
        if form.is_valid():
            form.save()
            # Puedes redirigir al inicio o mostrar un mensaje de éxito
            return redirect('/catalogo/') 
    else:
        form = ConsultaClienteForm()

    context = {
        'form': form,
        'visitas_contacto': request.session['visitas_contacto']
    }
    return render(request, 'contacto.html', context)