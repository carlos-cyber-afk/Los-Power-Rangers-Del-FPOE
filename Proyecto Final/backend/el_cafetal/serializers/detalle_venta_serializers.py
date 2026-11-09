from rest_framework import serializers

from ..models import detalle_venta


class detalle_venta_serializers(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = detalle_venta
        fields = [
            "id", "venta", "producto", "producto_nombre",
            "cantidad", "precio_unitario", "subtotal",
        ]

    def get_subtotal(self, obj):
        return obj.cantidad * obj.precio_unitario

    def validate_cantidad(self, value):
        if value < 1:
            raise serializers.ValidationError("La cantidad debe ser al menos 1.")
        return value
