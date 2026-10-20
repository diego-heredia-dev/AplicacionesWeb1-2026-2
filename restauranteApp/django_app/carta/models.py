from django.db import models
from django.db.models import Q


class Restaurante(models.Model):
    nombre = models.CharField(max_length=120)
    ciudad = models.CharField(max_length=80)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        ordering = ["nombre"]

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
        ordering = ["nombre"]
        constraints = [
            models.CheckConstraint(
                condition=Q(precio__gt=0),
                name="carta_plato_precio_positivo",
            ),
        ]

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("en_preparacion", "En preparación"),
        ("listo", "Listo"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]

    cliente = models.CharField(max_length=255)

    restaurante = models.ForeignKey(
        Restaurante,
        on_delete=models.PROTECT,
        related_name="pedidos",
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente",
    )

    fecha = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = ["-fecha"]
        constraints = [
            models.CheckConstraint(
                condition=Q(
                    estado__in=[
                        "pendiente",
                        "en_preparacion",
                        "listo",
                        "entregado",
                        "cancelado",
                    ]
                ),
                name="carta_pedido_estado_valido",
            ),
            models.CheckConstraint(
                condition=Q(total__gte=0),
                name="carta_pedido_total_no_negativo",
            ),
        ]

    def __str__(self):
        return f"Pedido #{self.pk} - {self.estado}"


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

    cantidad = models.PositiveIntegerField()

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(cantidad__gt=0),
                name="carta_item_cantidad_positiva",
            ),
            models.CheckConstraint(
                condition=Q(precio_unitario__gte=0),
                name="carta_item_precio_no_negativo",
            ),
        ]

    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre}"