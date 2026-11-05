"""
Serializador de Categoria: convierte objetos Categoria a JSON (y JSON a
objetos) y valida los datos que llegan en POST, PUT y PATCH.

extra_kwargs define cómo se muestra cada campo en el formulario HTML de la
API navegable (etiqueta, texto de ayuda y tipo de caja de texto).
No cambia la base de datos ni el JSON que recibe o devuelve la API.
"""
from rest_framework import serializers

from ..models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre", "descripcion"]
        extra_kwargs = {
            "nombre": {
                "label": "Nombre",
                "help_text": "Obligatorio y único. Máximo 60 caracteres.",
            },
            "descripcion": {
                "label": "Descripción",
                "help_text": "Opcional. Máximo 200 caracteres.",
                # Caja de texto de varias líneas en lugar de una sola línea.
                "style": {"base_template": "textarea.html", "rows": 3},
            },
        }
