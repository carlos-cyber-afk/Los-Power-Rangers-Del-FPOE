from rest_framework import viewsets
from .models import Uva
from .serializers import UvaSerializer

class UvaViewSet(viewsets.ModelViewSet):
    queryset = Uva.objects.all()
    serializer_class = UvaSerializer
