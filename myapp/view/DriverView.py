from datetime import datetime

from rest_framework import status

from rest_framework.response import Response

from myapp.models import Driver
from myapp.serializers import DriverGetSerializer, DriverPostSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, ListAPIView


class DriversListView(ListCreateAPIView):
    # Get all drivers / Create driver
    queryset = Driver.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DriverPostSerializer
        else:
            return DriverGetSerializer


class DriverDetailsView(RetrieveDestroyAPIView):
    # Get one driver / Delete driver / Update driver
    queryset = Driver.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return DriverPostSerializer
        else:
            return DriverGetSerializer


class DriverEditView(RetrieveUpdateAPIView):
    serializer_class = DriverPostSerializer

    # edit driver
    def put(self, request, *args, **kwargs):
        # post all the field when editing
        print("put##")
        driver = Driver.objects.filter(id=kwargs['pk'])
        is_verified = request.data['is_verified']
        is_blocked = request.data['is_blocked']

        if driver and is_verified and is_blocked:
            driver.update(is_verified=(is_verified == "true"), is_blocked=(is_blocked == "true"),
                          modifiedAt=datetime.strptime('24052010', "%d%m%Y").now())
            serializer = DriverGetSerializer(driver, many=True)
            return Response({"Drivers": serializer.data})
        return Response("Failed to edit driver", status=status.HTTP_400_BAD_REQUEST)
