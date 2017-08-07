from datetime import date, datetime, timezone

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Vendor, User, Shop, Product, SubCategory, Order, Courier, VendorCourier, Coverage
from myapp.serializers import ShopPostSerializer, ShopGetSerializer, ProductGetSerializer, ProductPostSerializer, \
    OrderGetSerializer, OrderPostSerializer, CourierGetSerializer, CourierPostSerializer, VendorCouriersGetSerializer, \
    VendorCouriersPostSerializer, CoveragePostSerializer, CoverageGetSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, \
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
    # Get all courier coverages / Create courier coverage
    queryset = Coverage.objects.all()
    serializer_class = CoverageGetSerializer
