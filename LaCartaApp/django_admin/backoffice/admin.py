from django.contrib import admin
from .models import Pedido, ItemPedido


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

    list_filter = ("estado", "restaurante")

    search_fields = ("cliente",)

    readonly_fields = ("fecha", "total")

    inlines = [ItemPedidoInline]