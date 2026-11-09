from rest_framework import viewsets

from ..models import categoria
from ..serializers import categoria_serializers


class categoria_views(viewsets.ModelViewSet):
    queryset = categoria.objects.all()
    serializer_class = categoria_serializers
