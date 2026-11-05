"""
Serializador de Categoria: convierte objetos Categoria a JSON (y JSON a
objetos) y valida los datos que llegan en POST, PUT y PATCH.

extra_kwargs define cómo se muestra cada campo en el formulario HTML de la
API navegable (etiqueta, texto de ayuda y tipo de caja de texto).
No cambia la base de datos ni el JSON que recibe o devuelve la API.
"""
from typing import __all__

from rest_framework import serializers 

from ..models import Uva


class UvaSerializer(serializers.ModelSerializer):
    peso = serializers.FloatField(error_messages={'invalid': 'solo se permiten números decimales.'})
    tamano = serializers.IntegerField(error_messages={'invalid': 'solo se permiten números enteros.'})
    forma = serializers.CharField(max_length=50, error_messages={'max_length': 'La forma no puede exceder los 50 caracteres.'})
    textura = serializers.CharField(max_length=50, error_messages={'max_length': 'La textura no puede exceder los 50 caracteres.'})
    class Meta:
        model = Uva
        fields = '__all__'
        extra_kwargs = {
            "textura": {
                "label": "Textura",
                "help_text": "Obligatorio. Máximo 50     caracteres.",
            },
            "descripcion": {
                "label": "Descripción",
                "help_text": "Opcional. Máximo 200 caracteres.",
                # Caja de texto de varias líneas en lugar de una sola línea.
                "style": {"base_template": "textarea.html", "rows": 3},
            },
        }
    def validate_tamano(self, value):
        if value <= 0:
            raise serializers.ValidationError("El tamaño debe ser un número positivo.")
        return value

    def validate_peso(self, value):
        if value <= 0:
            raise serializers.ValidationError("El peso debe ser un número positivo.")
        return value

    def validate_forma(self, value):
        if not all(x.isalpha() or x.isspace() for x in value):
           raise serializers.ValidationError("La forma solo puede contener letras y espacios.")
        return value

    def validate_textura(self, value):
        if not all(x.isalpha() or x.isspace() for x in value):
            raise serializers.ValidationError("La textura solo puede contener letras y espacios.")
        return value
