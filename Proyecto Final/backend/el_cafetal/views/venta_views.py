from rest_framework import viewsets

from ..models import venta
from ..serializers import venta_serializers


class venta_views(viewsets.ModelViewSet):
    queryset = venta.objects.prefetch_related("detalles__producto")
    serializer_class = venta_serializers
