"""
Vista (ViewSet) de Categoria.

Un ModelViewSet de Django REST Framework atiende todos los verbos HTTP:

    Verbo   URL                     Método del ViewSet   Acción
    ------  ----------------------  -------------------  ---------------------------
    GET     /api/categorias/        list()               Listar todas
    POST    /api/categorias/        create()             Crear una nueva
    GET     /api/categorias/{id}/   retrieve()           Consultar una
    PUT     /api/categorias/{id}/   update()             Reemplazar todos los campos
    PATCH   /api/categorias/{id}/   partial_update()     Modificar algunos campos
    DELETE  /api/categorias/{id}/   destroy()            Eliminar
"""
from django.db.models import ProtectedError
from rest_framework import status, viewsets
from rest_framework.response import Response

from ..models import Categoria
from ..serializers import CategoriaSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def destroy(self, request, *args, **kwargs):
        """DELETE: si la categoría tiene productos, responde 409 Conflict."""
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"detail": "No se puede eliminar: la categoría tiene productos asociados."},
                status=status.HTTP_409_CONFLICT,
            )
