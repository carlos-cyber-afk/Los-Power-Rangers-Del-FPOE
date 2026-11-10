"""
Serializador de Categoria: convierte objetos Categoria a JSON (y JSON a
objetos) y valida los datos que llegan en POST, PUT y PATCH.

extra_kwargs define cómo se muestra cada campo en el formulario HTML de la
API navegable (etiqueta, texto de ayuda y tipo de caja de texto).
No cambia la base de datos ni el JSON que recibe o devuelve la API.
"""
import re
from typing import __all__

from rest_framework import serializers 

from ..models import Uva


import re
from rest_framework import serializers
from ..models.uva import Uva

# 1. Clases personalizadas para capturar campos numéricos vacíos o nulos limpiamente
class CustomIntegerField(serializers.IntegerField):
    def to_internal_value(self, data):
        if data is None or data == "" or (isinstance(data, str) and not data.strip()):
            raise serializers.ValidationError("El tamaño no puede estar vacío.")
        return super().to_internal_value(data)

class CustomFloatField(serializers.FloatField):
    def to_internal_value(self, data):
        if data is None or data == "" or (isinstance(data, str) and not data.strip()):
            raise serializers.ValidationError("El peso no puede estar vacío.")
        return super().to_internal_value(data)


class UvaSerializer(serializers.ModelSerializer):
    # 2. Declaración de atributos con sus mensajes de error personalizados
    peso = CustomFloatField(
        allow_null=False,
        error_messages={
            'required': 'El peso no puede estar vacío.',
            'null': 'El peso no puede ser nulo.',
            'invalid': 'El peso debe ser un número decimal válido.'
        }
    )
    tamano = CustomIntegerField(
        allow_null=False,
        error_messages={
            'required': 'El tamaño no puede estar vacío.',
            'null': 'El tamaño no puede ser nulo.',
            'invalid': 'El tamaño debe ser un número entero válido.'
        }
    )
    forma = serializers.CharField(
        max_length=50, 
        error_messages={
            'required': 'La forma no puede estar vacía.',
            'blank': 'La forma no puede estar vacía.',
            'max_length': 'La forma no puede exceder los 50 caracteres.'
        }
    )
    textura = serializers.CharField(
        max_length=50, 
        error_messages={
            'required': 'La textura no puede estar vacía.',
            'blank': 'La textura no puede estar vacía.',
            'max_length': 'La textura no puede exceder los 50 caracteres.'
        }
    )

    class Meta:
        model = Uva
        fields = '__all__'
        extra_kwargs = {
            "textura": {
                "label": "Textura",
                "help_text": "Obligatorio. Máximo 50 caracteres.",
            },
            "descripcion": {
                "label": "Descripción",
                "help_text": "Opcional. Máximo 200 caracteres.",
                "style": {"base_template": "textarea.html", "rows": 3},
            },
        }

    # 3. Validaciones de texto (forma y textura)
    def validate_textura(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("La textura no puede estar vacía.")
        patron = re.compile(r"^[A-Za-zñÑáéíóúÁÉÍÓÚüÜ\s]+$")
        if not patron.match(value):
            raise serializers.ValidationError("La textura solo se permite con letras y espacios.")
        return value
    
    def validate_forma(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("La forma no puede estar vacía.")
        patron = re.compile(r"^[A-Za-zñÑáéíóúÁÉÍÓÚüÜ\s]+$")
        if not patron.match(value):
            raise serializers.ValidationError("La forma solo puede contener letras y espacios.")
        return value  

    # 4. Validaciones de números (peso y tamaño)
    def validate_peso(self, value):
        if value <= 0:
            raise serializers.ValidationError("El peso debe ser un número positivo.")
        if value >= 15:
            raise serializers.ValidationError("Máximo 15 de peso.")
        return value

    def validate_tamano(self, value):
        if value <= 0:
            raise serializers.ValidationError("El tamaño debe ser un número positivo.")
        if value >= 10:
            raise serializers.ValidationError("Máximo 10 de tamaño.")
        return value