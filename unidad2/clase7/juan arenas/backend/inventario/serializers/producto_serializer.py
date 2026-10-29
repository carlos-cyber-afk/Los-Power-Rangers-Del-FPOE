"""
Serializador de Producto: convierte objetos Producto a JSON (y JSON a
objetos) y valida los datos que llegan en POST, PUT y PATCH.

extra_kwargs define cómo se muestra cada campo en el formulario HTML de la
API navegable (etiqueta y texto de ayuda).
No cambia la base de datos ni el JSON que recibe o devuelve la API.
"""
from rest_framework import serializers

from ..models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    # Campo de solo lectura para mostrar el nombre de la categoría en la
    # interfaz sin hacer otra petición. Para escribir se usa "categoria" (id).
    # Por ser de solo lectura, no aparece en el formulario.
    categoria_nombre = serializers.CharField(
        source="categoria.nombre",
        read_only=True,
        label="Nombre de la categoría",
    )

    class Meta:
        model = Producto
        fields = ["id", "nombre", "precio", "stock", "categoria", "categoria_nombre"]
        extra_kwargs = {
            "nombre": {
                "label": "Nombre",
                "help_text": "Obligatorio. Máximo 80 caracteres.",
            },
            "precio": {
                "label": "Precio",
                "help_text": "En pesos, mayor que cero. Ejemplo: 3500.00",
            },
            "stock": {
                "label": "Stock",
                "help_text": "Unidades disponibles. Por defecto 0.",
            },
            "categoria": {
                "label": "Categoría",
                "help_text": "Elija la categoría de la lista.",
            },
        }

    def validate_precio(self, valor):
        if valor <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que cero.")
        return valor
