"""
Paquete de modelos: un archivo por clase.

Django busca los modelos en "inventario.models". Al importarlos aquí,
Django los encuentra (y las migraciones los detectan) igual que cuando
estaban todos en un solo models.py.

Gracias a este archivo, el resto del proyecto puede seguir escribiendo:
    from inventario.models import Categoria, Producto
"""
from .categoria import Categoria
from .producto import Producto
from .categoria_venta import CategoriaVenta 
from .venta import Venta
from .categoria_detalle import Categoria_Detalle
from .detalle_venta import Detalle_Venta

__all__ = ["Categoria", "Producto","CategoriaVenta", "Venta", "Categoria_Detalle", "Detalle_Venta"]
