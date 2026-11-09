from rest_framework import serializers

from ..models import producto


class producto_serializers(serializers.ModelSerializer):
    # Campo extra solo de lectura: muestra el nombre de la categoría.
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)

    class Meta:
        model = producto
        fields = ["id", "nombre", "precio", "stock", "categoria", "categoria_nombre"]

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que 0.")
        return value
