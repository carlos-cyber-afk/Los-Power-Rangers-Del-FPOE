"""
Paquete de vistas: un archivo por clase.

Permite que urls.py siga importando así, sin cambios:
    from .views import CategoriaViewSet, ProductoViewSet
"""
from .categoria_viewset import CategoriaViewSet
from .producto_viewset import ProductoViewSet

__all__ = ["CategoriaViewSet", "ProductoViewSet"]
