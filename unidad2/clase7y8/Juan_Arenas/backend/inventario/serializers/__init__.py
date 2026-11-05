"""
Paquete de serializadores: un archivo por clase.

Permite seguir importando así:
    from inventario.serializers import CategoriaSerializer, ProductoSerializer
"""
from .categoria_serializer import CategoriaSerializer
from .producto_serializer import ProductoSerializer

__all__ = ["CategoriaSerializer", "ProductoSerializer"]
