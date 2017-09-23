from datetime import datetime

from rest_framework import status

from rest_framework.response import Response

from myapp.models import Driver
from myapp.serializers import DriverGetSerializer, DriverPostSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView


class DriversListView(ListCreateAPIView):
    """
    Returns all drivers.
    Allows user to upgrade to driver
    """
    queryset = Driver.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DriverPostSerializer
        else:
            return DriverGetSerializer


class DriverDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Allows RUD driver
    """
    queryset = Driver.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DriverGetSerializer
        else:
            return DriverPostSerializer
