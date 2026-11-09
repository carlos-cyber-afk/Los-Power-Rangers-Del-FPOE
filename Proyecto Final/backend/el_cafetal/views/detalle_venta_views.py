from rest_framework import viewsets

from ..models import detalle_venta
from ..serializers import detalle_venta_serializers


class detalle_venta_views(viewsets.ModelViewSet):
    queryset = detalle_venta.objects.select_related("venta", "producto")
    serializer_class = detalle_venta_serializers
