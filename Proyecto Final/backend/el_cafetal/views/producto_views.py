from rest_framework import viewsets

from ..models import producto
from ..serializers import producto_serializers


class producto_views(viewsets.ModelViewSet):
    queryset = producto.objects.select_related("categoria")
    serializer_class = producto_serializers
