"""
Paquete de vistas: un archivo por clase.

Permite que urls.py siga importando así, sin cambios:
    from .views import CategoriaViewSet, ProductoViewSet
"""
from .uva_viewset import UvaViewSet

__all__ = ["UvaViewSet"]
