from datetime import date, datetime, timezone

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Vendor, User, Shop, Product, SubCategory, Order, Courier, VendorCourier, Coverage, Driver
from myapp.serializers import ShopPostSerializer, ShopGetSerializer, ProductGetSerializer, ProductPostSerializer, \
    OrderGetSerializer, OrderPostSerializer, CourierGetSerializer, CourierPostSerializer, VendorCouriersGetSerializer, \
    VendorCouriersPostSerializer, CoveragePostSerializer, CoverageGetSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView


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
            self.request.data['courier'] = self.kwargs['pk']
            return CoveragePostSerializer
        else:
            return CoverageGetSerializer


class CourierCoveragesUpdateView(RetrieveUpdateDestroyAPIView):
    # Get one courier_coverage, Edit courier_coverage, Delete courier_coverage
    # pk2->coverages.id passed to the queryset
    lookup_url_kwarg = 'pk2'

    def get_serializer_class(self):
        self.request.POST._mutable = True
        self.request.data['courier'] = self.kwargs['pk']
        return CoveragePostSerializer

    def get_queryset(self):
        return Coverage.objects.filter(courier=self.kwargs['pk'])


# class AllDriversListView(ListAPIView):
#     # Get all coverages from all couriers
#     queryset = Driver.objects.all()
#     serializer_class = DriverGetSerializer
#
#
# class CourierDriversListView(ListCreateAPIView):
#     # Get all courier coverages / Create courier coverage
#     def get_queryset(self):
#         print("courier id " + self.kwargs['pk'])
#         return Driver.objects.filter(courier=self.kwargs['pk'])
#
#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             self.request.POST._mutable = True
#             self.request.data['courier'] = self.kwargs['pk']
#             return DriverPostSerializer
#         else:
#             return DriverGetSerializer
#
#
# class CourierDriversUpdateView(RetrieveUpdateDestroyAPIView):
#     # Get one courier_coverage, Edit courier_coverage, Delete courier_coverage
#     # pk2->coverages.id passed to the queryset
#     lookup_url_kwarg = 'pk2'
#
#     def get_serializer_class(self):
#         self.request.POST._mutable = True
#         self.request.data['courier'] = self.kwargs['pk']
#         return DriverPostSerializer
#
#     def get_queryset(self):
#         return Driver.objects.filter(courier=self.kwargs['pk'])