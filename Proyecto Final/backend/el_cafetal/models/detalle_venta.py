from django.db import models
from .producto import producto
from .venta import venta


class detalle_venta(models.Model):


 venta = models.ForeignKey(
        venta,
        on_delete=models.CASCADE,
        related_name="detalles",
    )

 producto = models.ForeignKey(
        producto,
        on_delete=models.PROTECT,
        related_name= "detalles_venta",
    )
 cantidad = models.PositiveBigIntegerField()
 precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

 class Meta:
  ordering = ["id"]

 def __str__(self):
  return f"Detalle #{self.id}"
 










 """

    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["venta", "producto"]

    def __str__(self):
        return f"Detalle de Venta {self.id} - Venta {self.venta.id} - Producto {self.producto.nombre}

        
"""
