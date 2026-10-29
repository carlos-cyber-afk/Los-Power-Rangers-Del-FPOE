"""
Modelo Producto.

Cada producto pertenece a una sola categoría (llave foránea en Producto).
"""
from django.db import models

from .categoria import Categoria


class Producto(models.Model):
    nombre = models.CharField(max_length=80)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    # Llave foránea: PROTECT impide borrar una categoría que tenga productos.
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos",
    )

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"
