from datetime import date
from rest_framework import serializers

from ..models import Libro

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ["id", "titulo", "paginas", "fecha_publicacion", "disponible"]
        extra_kwargs = {
            "titulo": {"label": "Título", "help_text": "Obligatorio. Máximo 150 caracteres."},
            "paginas": {"label": "Páginas", "help_text": "Número entero mayor que cero."},
            "fecha_publicacion": {"label": "Fecha de publicación", "help_text": "Formato AAAA-MM-DD. Ejemplo: 2020-05-14"},
            "disponible": {"label": "Disponible"},
        }

    def validate_paginas(self, valor):
        if valor <= 0:
            raise serializers.ValidationError("Las páginas deben ser mayores que cero.")
        return valor

    def validate_fecha_publicacion(self, valor):
        if valor > date.today():
            raise serializers.ValidationError("La fecha no puede ser futura.")
        return valor