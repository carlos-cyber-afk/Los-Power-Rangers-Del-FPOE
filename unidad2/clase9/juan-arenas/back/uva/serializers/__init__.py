"""
Paquete de serializadores: un archivo por clase.

Permite seguir importando así:
    from inventario.serializers import CategoriaSerializer, ProductoSerializer
"""
from .uva_serializer import UvaSerializer

__all__ = ["UvaSerializer"]
