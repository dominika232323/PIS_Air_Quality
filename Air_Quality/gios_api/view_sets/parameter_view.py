from rest_framework import viewsets

from gios_api.models import Parameter
from gios_api.serializer import ParameterSerializer


class ParameterViewSet(viewsets.ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
