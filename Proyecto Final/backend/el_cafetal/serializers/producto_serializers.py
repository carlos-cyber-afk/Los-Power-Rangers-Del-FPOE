from rest_framework import serializers
import re
from ..models import producto


class producto_serializers(serializers.ModelSerializer):

    class Meta:
        model = producto
        fields = ["id", "nombre", "precio", "stock", "activo"]

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que 0.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("La existencia no puede ser menor que 0.")
        return value

    def validate_nombre(self, value):
        value = value.strip()
        letras = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
        if len(value) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres.")
        if not re.fullmatch(rf"[{letras}0-9 .,()-]+", value) or not re.search(rf"[{letras}]", value):
            raise serializers.ValidationError(
                "El nombre solo puede tener letras, números, espacios y . , - ( ), y al menos una letra."
            )
        return value