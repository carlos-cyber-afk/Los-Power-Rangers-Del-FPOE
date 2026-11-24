import re
from rest_framework import serializers

from ..models import venta
from .detalle_venta_serializers import detalle_venta_serializers


class venta_serializers(serializers.ModelSerializer):
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

    def validate_cliente(self, value):
        value = value.strip()
        letras = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
        if not value:
            raise serializers.ValidationError("Escribe el nombre del cliente.")
        if len(value) < 2:
            raise serializers.ValidationError("El nombre del cliente debe tener al menos 2 caracteres.")
        if not re.fullmatch(rf"[{letras}0-9 .,()-]+", value) or not re.search(rf"[{letras}]", value):
            raise serializers.ValidationError(
                "El nombre del cliente solo puede tener letras, números, espacios y . , - ( ), y al menos una letra."
            )
        return value