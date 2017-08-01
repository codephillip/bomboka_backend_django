from datetime import date, datetime, timezone

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Vendor, User, Shop, Product, SubCategory, Order, Courier, VendorCourier
from myapp.serializers import ShopPostSerializer, ShopGetSerializer, ProductGetSerializer, ProductPostSerializer, \
    OrderGetSerializer, OrderPostSerializer, CourierGetSerializer, CourierPostSerializer, VendorCouriersSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView


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

        print("db#")
        if serializer.is_valid():
            serializer.save()
            return Response({"Couriers": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorCouriers(APIView):
    # get vendor couriers
    def get(self, request, vendor_id):
        print("vendor_courier")
        vendor_couriers = VendorCourier.objects.filter(vendor_id=vendor_id)
        serializer = VendorCouriersSerializer(vendor_couriers, many=True)
        return Response({"VendorCouriers": serializer.data})
