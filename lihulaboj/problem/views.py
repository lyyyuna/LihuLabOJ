from rest_framework import mixins, viewsets
from .models import Answser
from .serializers import AnswserSerializer


class AnswserViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    queryset = Answser.objects.all()
    serializer_class = AnswserSerializer