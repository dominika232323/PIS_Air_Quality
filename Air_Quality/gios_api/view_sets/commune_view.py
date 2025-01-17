from rest_framework import viewsets

from gios_api.models import Commune
from gios_api.serializer import CommuneSerializer


class CommuneViewSet(viewsets.ModelViewSet):
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
