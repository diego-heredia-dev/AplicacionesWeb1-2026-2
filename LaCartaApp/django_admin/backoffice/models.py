from django.db import models
from django.db.models import Q

class Restaurante(models.Model):
    nombre = models.CharField(max_length=120)
    ciudad = models.CharField(max_length=80)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = "restaurantes"
        db_table_comment = "Restaurantes registrados en La Carta"

    def __str__(self):
        return self.nombre


class Plato(models.Model):
    nombre = models.CharField(max_length=120)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    restaurante = models.ForeignKey(
        Restaurante,
        on_delete=models.CASCADE,
        related_name="platos",
    )

    class Meta:
        db_table = "platos"
        db_table_comment = "Platos ofrecidos por los restaurantes"

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        EN_PREPARACION = "en_preparacion", "En preparación"
        LISTO = "listo", "Listo"
        ENTREGADO = "entregado", "Entregado"
        CANCELADO = "cancelado", "Cancelado"

    cliente = models.CharField(max_length=120)
    restaurante = models.ForeignKey(
        Restaurante,
        on_delete=models.PROTECT,
        related_name="pedidos",
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    class Meta:
        db_table = "pedidos"
        ordering = ["-fecha"]
        constraints = [
            models.CheckConstraint(
                condition=Q(estado__in=[
                    "pendiente",
                    "en_preparacion",
                    "listo",
                    "entregado",
                    "cancelado",
                ]),
                name="pedido_estado_valido",
            ),
            models.CheckConstraint(
                condition=Q(total__gte=0),
                name="pedido_total_no_negativo",
            ),
        ]

    def __str__(self):
        return f"Pedido #{self.pk} - {self.cliente}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="items",
    )
    plato = models.ForeignKey(
        Plato,
        on_delete=models.PROTECT,
        related_name="items_pedido",
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        db_table = "items_pedido"
        constraints = [
            models.CheckConstraint(
                condition=Q(cantidad__gt=0),
                name="item_cantidad_mayor_cero",
            ),
            models.CheckConstraint(
                condition=Q(precio_unitario__gte=0),
                name="item_precio_no_negativo",
            ),
        ]

    def __str__(self):
        return f"{self.plato} x {self.cantidad}"

class Empleado(models.Model):
    nombre = models.CharField(max_length=120)
    cargo = models.CharField(max_length=80)

    restaurante = models.ForeignKey(
        Restaurante,
        on_delete=models.CASCADE,
        related_name="empleados",
    )

    class Meta:
        db_table = "empleados"
        db_table_comment = "Empleados de los restaurantes"

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"