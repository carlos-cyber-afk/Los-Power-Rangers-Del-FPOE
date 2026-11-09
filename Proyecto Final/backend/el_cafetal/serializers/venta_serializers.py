from rest_framework import serializers

from ..models import venta
from .detalle_venta_serializers import detalle_venta_serializers


class venta_serializers(serializers.ModelSerializer):
    # Lista de detalles de esta venta (solo lectura).
    detalles = detalle_venta_serializers(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = venta
        fields = [
            "id", "fecha", "cliente", "metodo_pago",
            "observaciones", "detalles", "total",
        ]

    def get_total(self, obj):
        return sum(d.cantidad * d.precio_unitario for d in obj.detalles.all())
