from django.db import migrations
from decimal import Decimal

def cargar_datos_iniciales(apps, schema_editor):
    Categoria = apps.get_model('ferreteria', 'Categoria')
    Producto = apps.get_model('ferreteria', 'Producto')

    productos_json = [
        {"id": 1, "nombre": "Martillo Galponero 16oz", "categoria": "Herramientas Manuales", "precio": 89.90, "stock": 15, "imagen": "productos/martillo.jpg"},
        {"id": 2, "nombre": "Taladro Percutor 650W", "categoria": "Herramientas Eléctricas", "precio": 349.90, "stock": 8, "imagen": "productos/taladro.jpg"},
        {"id": 3, "nombre": "Sierra Circular 7-1/4", "categoria": "Herramientas Eléctricas", "precio": 599.90, "stock": 4, "imagen": "productos/sierra.jpg"},
        {"id": 4, "nombre": "Set Destornilladores 6 pcs", "categoria": "Herramientas Manuales", "precio": 64.90, "stock": 25, "imagen": "productos/destornillador.jpg"},
        {"id": 5, "nombre": "Alicate Universal 8 pulg", "categoria": "Herramientas Manuales", "precio": 52.90, "stock": 0, "imagen": "productos/alicate.jpg"},
        {"id": 6, "nombre": "Llave Francesa 10 pulg", "categoria": "Herramientas Manuales", "precio": 79.90, "stock": 12, "imagen": "productos/llave_francesa.jpg"},
        {"id": 7, "nombre": "Huincha de Medir 5m", "categoria": "Medición", "precio": 39.90, "stock": 30, "imagen": "productos/cinta_medir.jpg"},
        {"id": 8, "nombre": "Nivel de Burbuja 24 pulg", "categoria": "Medición", "precio": 84.90, "stock": 6, "imagen": "productos/nivel.jpg"},
        {"id": 9, "nombre": "Esmeril Angular 4-1/2 850W", "categoria": "Herramientas Eléctricas", "precio": 399.90, "stock": 0, "imagen": "productos/esmeril.jpg"},
        {"id": 10, "nombre": "Caja de Herramientas 19 pulg", "categoria": "Almacenamiento", "precio": 149.90, "stock": 10, "imagen": "productos/caja_herramientas.jpg"},
        {"id": 11, "nombre": "Juego Llaves Combinadas 8-19mm", "categoria": "Herramientas Manuales", "precio": 169.90, "stock": 7, "imagen": "productos/llaves_convinadas.jpg"},
        {"id": 12, "nombre": "Tornillo Drywall 6x1-5/8 100u", "categoria": "Fijaciones", "precio": 24.90, "stock": 50, "imagen": "productos/tornillos.jpg"},
        {"id": 13, "nombre": "Tarugo Nylon 8mm 50u", "categoria": "Fijaciones", "precio": 19.90, "stock": 40, "imagen": "productos/tarugo.jpg"},
        {"id": 14, "nombre": "Clavo Corriente 2-1/2 pulg 1kg", "categoria": "Fijaciones", "precio": 28.90, "stock": 0, "imagen": "productos/clavos.jpg"},
        {"id": 15, "nombre": "Pintura Látex Blanco 1 Galón", "categoria": "Pinturas", "precio": 189.90, "stock": 14, "imagen": "productos/pintura.jpg"},
        {"id": 16, "nombre": "Esmalte al Agua Gris 1 Galón", "categoria": "Pinturas", "precio": 229.90, "stock": 9, "imagen": "productos/esmalte.jpg"},
        {"id": 17, "nombre": "Brocha Cerda Natural 3 pulg", "categoria": "Accesorios Pintura", "precio": 27.90, "stock": 22, "imagen": "productos/brocha.jpg"},
        {"id": 18, "nombre": "Rodillo Antigoteo 23cm", "categoria": "Accesorios Pintura", "precio": 45.90, "stock": 18, "imagen": "productos/rodillo.jpg"},
        {"id": 19, "nombre": "Lija Madera Grano 120 (3u)", "categoria": "Abrasivos", "precio": 12.90, "stock": 60, "imagen": "productos/lija.jpg"},
        {"id": 20, "nombre": "Disco de Corte Metal 4-1/2", "categoria": "Abrasivos", "precio": 11.90, "stock": 0, "imagen": "productos/disco.jpg"},
        {"id": 21, "nombre": "Silicona Neutra Transparente 280ml", "categoria": "Adhesivos y Sellantes", "precio": 38.90, "stock": 16, "imagen": "productos/silicona.jpg"},
        {"id": 22, "nombre": "Cola Fría Profesional 1kg", "categoria": "Adhesivos y Sellantes", "precio": 49.90, "stock": 11, "imagen": "productos/cola_fria.jpg"},
        {"id": 23, "nombre": "Espuma Poliuretano 500ml", "categoria": "Adhesivos y Sellantes", "precio": 54.90, "stock": 5, "imagen": "productos/espuma.jpg"},
        {"id": 24, "nombre": "Cinta Aisladora Negra 20m", "categoria": "Electricidad", "precio": 9.90, "stock": 35, "imagen": "productos/cinta_aisladora.jpg"},
        {"id": 25, "nombre": "Cable Unipolar 1.5mm 100m Rojo", "categoria": "Electricidad", "precio": 249.90, "stock": 0, "imagen": "productos/cable_unipolar.jpg"},
        {"id": 26, "nombre": "Interruptor Simple Embutido", "categoria": "Electricidad", "precio": 18.90, "stock": 28, "imagen": "productos/interruptor.jpg"},
        {"id": 27, "nombre": "Enchufe Doble Volante", "categoria": "Electricidad", "precio": 21.90, "stock": 20, "imagen": "productos/enchufe_doble.jpg"},
        {"id": 28, "nombre": "Cerradura de Sobreponer Derecha", "categoria": "Cerrajería", "precio": 159.90, "stock": 6, "imagen": "productos/cerradura.jpg"},
        {"id": 29, "nombre": "Candado Bronce 50mm", "categoria": "Cerrajería", "precio": 64.90, "stock": 13, "imagen": "productos/candado.jpg"},
        {"id": 30, "nombre": "Guantes de Cabritilla Talla 9", "categoria": "Seguridad", "precio": 32.90, "stock": 25, "imagen": "productos/guantes.jpg"},
        {"id": 31, "nombre": "Lentes de Seguridad Claros", "categoria": "Seguridad", "precio": 18.90, "stock": 40, "imagen": "productos/lentes.jpg"},
        {"id": 32, "nombre": "Mascarilla N95 Carbón Activo", "categoria": "Seguridad", "precio": 21.90, "stock": 0, "imagen": "productos/mascarilla.jpg"},
        {"id": 33, "nombre": "Casco de Seguridad Blanco", "categoria": "Seguridad", "precio": 59.90, "stock": 10, "imagen": "productos/casco.jpg"},
        {"id": 34, "nombre": "Llave Grifería Monomando", "categoria": "Gasfitería", "precio": 219.90, "stock": 7, "imagen": "productos/llave_grifera.jpg"},
        {"id": 35, "nombre": "Tubo PVC Sanitario 110mm 3m", "categoria": "Gasfitería", "precio": 119.90, "stock": 15, "imagen": "productos/pvc.jpg"},
        {"id": 36, "nombre": "Teflón de Gas 3/4 pulg", "categoria": "Gasfitería", "precio": 8.90, "stock": 50, "imagen": "productos/teflon.jpg"},
        {"id": 37, "nombre": "Pistola para Silicona", "categoria": "Herramientas Manuales", "precio": 29.90, "stock": 12, "imagen": "productos/pistola_silicona.jpg"},
        {"id": 38, "nombre": "Carretilla Metálica 90L", "categoria": "Construcción", "precio": 449.90, "stock": 3, "imagen": "productos/carretilla.jpg"},
        {"id": 39, "nombre": "Pala Punta de Huevo con Mango", "categoria": "Construcción", "precio": 99.90, "stock": 0, "imagen": "productos/pala.jpg"},
        {"id": 40, "nombre": "Cincel Plano 10 pulg", "categoria": "Herramientas Manuales", "precio": 42.90, "stock": 9, "imagen": "productos/cincel.jpg"}
    ]

    for item in productos_json:
        categoria_obj, _ = Categoria.objects.get_or_create(nombre=item["categoria"])
        Producto.objects.update_or_create(
            id=item["id"],
            defaults={
                "nombre": item["nombre"],
                "categoria": categoria_obj,
                "precio": Decimal(str(item["precio"])),
                "stock": item["stock"],
                "imagen": item["imagen"],
            }
        )

def revertir_datos(apps, schema_editor):
    Categoria = apps.get_model('ferreteria', 'Categoria')
    Producto = apps.get_model('ferreteria', 'Producto')
    Producto.objects.all().delete()
    Categoria.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('ferreteria', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar_datos_iniciales, revertir_datos),
    ]