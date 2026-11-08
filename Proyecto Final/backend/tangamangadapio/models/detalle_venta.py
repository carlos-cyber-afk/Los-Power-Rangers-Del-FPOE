from django.db import models
from .categoria_detalle import Categoria_Detalle 

class Detalle_Venta(models.Model):

    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    categoria_detalle = models.ForeignKey(
        Categoria_Detalle,
        on_delete=models.PROTECT,
        related_name="detalle_ventas",
    )

    class Meta:
        ordering = ["venta", "producto"]

        def __str__(self):
            return f"Detalle de Venta {self.id} - Venta {self.venta.id} - Producto {self.producto.nombre}"