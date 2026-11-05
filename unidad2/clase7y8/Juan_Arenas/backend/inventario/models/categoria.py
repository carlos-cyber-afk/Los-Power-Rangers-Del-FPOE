"""
Modelo Categoria.

Categoria (1) ──────< (N) Producto
Una categoría tiene muchos productos.
"""
from django.db import models


class Categoria(models.Model):
    # El campo "id" (llave primaria) lo crea Django automáticamente.
    nombre = models.CharField(max_length=60, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
