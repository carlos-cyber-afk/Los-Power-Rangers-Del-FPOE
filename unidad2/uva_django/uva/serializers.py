from rest_framework import serializers
from .models import Uva

class UvaSerializer(serializers.ModelSerializer):

    peso = serializers.FloatField(error_messages={'invalid': 'solo se permiten números decimales.'})
    tamano = serializers.IntegerField(error_messages={'invalid': 'solo se permiten números enteros.'})
    forma = serializers.CharField(max_length=50, error_messages={'max_length': 'La forma no puede exceder los 50 caracteres.'})
    textura = serializers.CharField(max_length=50, error_messages={'max_length': 'La textura no puede exceder los 50 caracteres.'})
    class Meta:
        model = Uva
        fields = '__all__'

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