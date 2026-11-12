from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=70)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="productos", blank=False, null=False)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        PAGADA = "pagada", "Pagada"
        CANCELADA = "cancelada", "Cancelada"

    usuario = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="compras"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.PENDIENTE
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "compras"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Compra {self.pk} - {self.usuario}"


class DetalleCompra(models.Model):
    compra = models.ForeignKey(
        Compra, on_delete=models.CASCADE, related_name="detalles"
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.PROTECT, related_name="detalles_compra"
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = "detalle_compra"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cantidad__gt=0),
                name="detalle_compra_cantidad_positiva",
            ),
            models.CheckConstraint(
                condition=models.Q(precio_unitario__gte=0),
                name="detalle_compra_precio_no_negativo",
            ),
        ]

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"


class ConsultaCliente(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        RESPONDIDA = "respondida", "Respondida"
        CERRADA = "cerrada", "Cerrada"

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="consultas",
        blank=True,
        null=True,
    )
    nombre = models.CharField(max_length=70)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    asunto = models.CharField(max_length=150)
    producto_interes = models.ForeignKey(
        Producto,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Producto de interés",
        related_name="consultas"
    )
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.PENDIENTE
    )

    class Meta:
        db_table = "consulta_cliente"
        ordering = ["-fecha"]

    def __str__(self):
        return self.asunto
