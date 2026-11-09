from rest_framework import serializers

from ..models import categoria


class categoria_serializers(serializers.ModelSerializer):
    class Meta:
        model = categoria
        fields = ["id", "nombre", "descripcion"]
