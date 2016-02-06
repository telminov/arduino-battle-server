from django.shortcuts import render
import rest_framework.viewsets

from core import models
from core import serializers


def index(request):
    return render(request, 'index.html')


class CarViewSet(rest_framework.viewsets.ReadOnlyModelViewSet):
    queryset = models.Car.objects.all()
    serializer_class = serializers.Car
