from rest_framework import serializers
from django.db import transaction

from ..models import detalle_venta, producto


class detalle_venta_serializers(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    subtotal = serializers.SerializerMethodField()
    precio_unitoria = serializers.DecimalField( 
       max_digits=10, decimal_places=2, required=False
    )

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
    def validate(self,attrs):
        prod = attrs.get("producto") or (self.instance.producto if self.instance else None)
        cant = attrs.get("cantidad") if "cantidad" in attrs else (self.instace.cantidad if self.self.instance else None)

        if prod is not None and cant is not None and self.instance is None:
            if prod.stock < cant:
                raise serializers.ValidacionError(
                    {"cantidad": f"Stock insuficiente para {prod.nombre}. Disponible: {prod.stock}. "}
                )  
        return attrs
    def create(self, validated_data):
        with transaction.atomic():
            prod = producto.objects.select_for_update().get(pk = self.validated_data["producto"].pk)
            cant = validated_data["cantidad"]

            if prod.stock < cant:
                raise serializers.ValidationError(
                    {"cantidad"f"Stock insuficiente para {prod.nombre}. Disponible: {prod.stock}."}
                )
            if "precio_unitario" not in validated_data or validated_data["precio_unitario"] is None:
                validated_data["precio_unitario"] = prod.precio

            prod.stock -= cant
            prod.save(update_fields=["stock"])

            return super().create(validated_data)