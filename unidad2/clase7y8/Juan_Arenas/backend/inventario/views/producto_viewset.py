"""
Vista (ViewSet) de Producto.

Atiende GET, POST, PUT, PATCH y DELETE sobre /api/productos/ y
/api/productos/{id}/ (ver la tabla en categoria_viewset.py).
"""
from rest_framework import viewsets

from ..models import Producto
from ..serializers import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    # select_related evita una consulta extra por cada producto al leer la categoría.
    queryset = Producto.objects.select_related("categoria").all()
    serializer_class = ProductoSerializer

    def get_queryset(self):
        """GET /api/productos/?categoria=3 filtra los productos de una categoría."""
        consulta = super().get_queryset()
        categoria_id = self.request.query_params.get("categoria")
        if categoria_id:
            consulta = consulta.filter(categoria_id=categoria_id)
        return consulta
