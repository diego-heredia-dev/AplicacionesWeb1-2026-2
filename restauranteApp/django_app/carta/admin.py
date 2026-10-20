from django.contrib import admin

from .models import Restaurante, Plato, Pedido, ItemPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ("precio_unitario",)
    fields = ("plato", "cantidad", "precio_unitario")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cliente",
        "restaurante",
        "estado",
        "fecha",
        "total",
    )

    list_filter = (
        "estado",
        "restaurante",
    )

    search_fields = (
        "cliente",
        "restaurante__nombre",
    )

    readonly_fields = (
        "fecha",
        "total",
    )

    inlines = [ItemPedidoInline]

    date_hierarchy = "fecha"


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "ciudad",
        "telefono",
    )

    search_fields = (
        "nombre",
        "ciudad",
    )


@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "restaurante",
        "precio",
        "disponible",
    )

    list_filter = (
        "disponible",
        "restaurante",
    )

    search_fields = (
        "nombre",
        "restaurante__nombre",
    )