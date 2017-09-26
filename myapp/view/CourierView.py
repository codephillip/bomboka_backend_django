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


class CourierView(ListCreateAPIView):
    """
    Returns all Couriers in the System
    Allows User to upgrade to Courier
    """
    queryset = Courier.objects.all()

    def get_serializer_class(self):
        if self.request.POST:
            return CourierPostSerializer
        else:
            return CourierGetSerializer


class VendorCouriers(ListCreateAPIView):
    """
    Returns all Vendor Couriers (Courier partners)
    Vendor registers Vendor Courier (Courier partner)
    Courier partner handles User orders made to the Vendor's Shop
    """
    def get_queryset(self):
        return VendorCourier.objects.filter(courier=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.request.POST._mutable = True
            try:
                self.request.data['vendor'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return VendorCouriersPostSerializer
        else:
            return VendorCouriersGetSerializer


class AllCoveragesListView(ListAPIView):
    """
    Returns all coverages from all couriers.
    Coverage is the area where the courier operates
    """
    queryset = Coverage.objects.all()
    serializer_class = CoverageGetSerializer


class CourierCoveragesListView(ListCreateAPIView):
    """
    Returns all courier coverages
    Allows courier to create coverage
    """
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
    """
    Returns single courier coverage
    Allows UD of courier coverage
    """
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
    """
    Lists all courier driver partnerships
    Allows courier to add drivers as their partner
    """
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
    """
    Returns single courier driver partner
    Allows courier to cancel partnership with driver
    """
    # pk2->driver.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_serializer_class(self):
        return CourierDriversPostSerializer

    def get_queryset(self):
        return CourierDriver.objects.filter(courier=self.kwargs['pk'])


class CourierOrdersDetailsView(ListAPIView):
    """
    Returns all the orders that the courier has to deliver.
    Displays delivered and undelivered orders
    """
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        return Order.objects.filter(courier=self.kwargs['pk'])


class VehicleView(ListCreateAPIView):
    """
    Returns all vehicles(means of transport)
    Allows the admin to add vehicle that will be selected by the courier
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Allows RUD of vehicle
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class CourierVehicleListView(ListCreateAPIView):
    """
    Returns all courier vehicles
    Allows a courier to select their means of transport
    """
    def get_queryset(self):
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
    """
    Returns single courier vehicle.
    Allows deletion of courier vehicle
    """
    # pk2->vehicle.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_serializer_class(self):
        return CourierVehiclePostSerializer

    def get_queryset(self):
        return CourierVehicle.objects.filter(courier=self.kwargs['pk'])
