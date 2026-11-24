from rest_framework import viewsets
from ..models.detalle_venta import detalle_venta
from ..serializers.detalle_venta_serializers import detalle_venta_serializers

class detalle_venta_views(viewsets.ModelViewSet):
    queryset = detalle_venta.objects.all()
    serializer_class = detalle_venta_serializers

    def get_queryset(self):
        queryset = detalle_venta.objects.all()
        # Captura el id de la venta enviado desde la URL (ej: /api/detalles/?venta=2)
        venta_id = self.request.query_params.get('venta')
        if venta_id is not None:
            queryset = queryset.filter(venta_id=venta_id)
        return queryset