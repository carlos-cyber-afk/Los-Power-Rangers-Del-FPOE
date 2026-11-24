from django.db.models import ProtectedError
from rest_framework import status, viewsets
from rest_framework.response import Response

from ..models import producto
from ..serializers import producto_serializers


class producto_views(viewsets.ModelViewSet):
    queryset = producto.objects.all()
    serializer_class = producto_serializers

    def destroy(self, request, *args, **kwargs):
        # Si el producto ya está en una venta (on_delete=PROTECT), responder 409 y no un error 500
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "Este producto ya tiene ventas y no se puede eliminar."},
                status=status.HTTP_409_CONFLICT,
            )