from datetime import datetime

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Order, Courier, VendorCourier, Coverage, CourierDriver, Vehicle, CourierVehicle
from myapp.serializers import CourierGetSerializer, CourierPostSerializer, VendorCouriersGetSerializer, \
    VendorCouriersPostSerializer, CoveragePostSerializer, CoverageGetSerializer, CourierDriversGetSerializer, \
    CourierDriversPostSerializer, OrderGetSerializer, VehicleSerializer, CourierVehicleGetSerializer, \
    CourierVehiclePostSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateDestroyAPIView, ListAPIView


class CourierView(APIView):
    # get all couriers
    def get(self, request, format=None):
        print("courierview")
        couriers = Courier.objects.all()
        serializer = CourierGetSerializer(couriers, many=True)
        return Response({"Couriers": serializer.data})

    # create courier
    def post(self, request, format=None):
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        serializer = CourierPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Couriers": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorCouriers(APIView):
    # get vendor couriers
    def get(self, request, vendor_id):
        print("vendor_courier")
        vendor_couriers = VendorCourier.objects.filter(vendor_id=vendor_id)
        serializer = VendorCouriersGetSerializer(vendor_couriers, many=True)
        return Response({"VendorCouriers": serializer.data})

    # add courier to vendor
    def post(self, request, vendor_id):
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        request.data['vendor'] = vendor_id
        serializer = VendorCouriersPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"VendorCouriers": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllCoveragesListView(ListAPIView):
    # Get all coverages from all couriers
    queryset = Coverage.objects.all()
    serializer_class = CoverageGetSerializer


class CourierCoveragesListView(ListCreateAPIView):
    # Get all courier coverages / Create courier coverage
    def get_queryset(self):
        print("courier id " + self.kwargs['pk'])
        return Coverage.objects.filter(courier=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.request.POST._mutable = True
            try:
                self.request.data['courier'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return CoveragePostSerializer
        else:
            return CoverageGetSerializer


class CourierCoveragesUpdateView(RetrieveUpdateDestroyAPIView):
    # Get one courier_coverage, Edit courier_coverage, Delete courier_coverage
    # pk2->coverages.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_serializer_class(self):
        self.request.POST._mutable = True
        try:
            self.request.data['courier'] = self.kwargs['pk']
        except Exception as e:
            print(e)
        return CoveragePostSerializer

    def get_queryset(self):
        return Coverage.objects.filter(courier=self.kwargs['pk'])


class CourierDriversListView(ListCreateAPIView):
    # Get all courier drivers / Create courier driver partnership
    # Courier can also be the driver
    def get_queryset(self):
        print("courier id " + self.kwargs['pk'])
        return CourierDriver.objects.filter(courier=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.request.POST._mutable = True
            try:
                self.request.data['courier'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return CourierDriversPostSerializer
        else:
            return CourierDriversGetSerializer


class CourierDriversDetailsView(RetrieveDestroyAPIView):
    # Get one courier_driver, Delete courier_driver
    # pk2->driver.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_serializer_class(self):
        return CourierDriversPostSerializer

    def get_queryset(self):
        return CourierDriver.objects.filter(courier=self.kwargs['pk'])


class CourierOrdersDetailsView(ListAPIView):
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        return Order.objects.filter(courier=self.kwargs['pk'])


class VehicleView(ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class CourierVehicleListView(ListCreateAPIView):
    # Get all courier vehicle / Create courier vehicle
    def get_queryset(self):
        print("courier id " + self.kwargs['pk'])
        return CourierVehicle.objects.filter(courier=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.request.POST._mutable = True
            try:
                self.request.data['courier'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return CourierVehiclePostSerializer
        else:
            return CourierVehicleGetSerializer


class CourierVehicleDetailsView(RetrieveDestroyAPIView):
    # Get one courier_vehicle, Delete courier_vehicle
    # pk2->vehicle.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_serializer_class(self):
        return CourierVehiclePostSerializer

    def get_queryset(self):
        return CourierVehicle.objects.filter(courier=self.kwargs['pk'])
