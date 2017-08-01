from datetime import date, datetime

from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Vendor, User, Shop
from myapp.serializers import VendorGetSerializer, VendorPostSerializer, ShopGetSerializer


class VendorView(APIView):
    def get(self, request, format=None):
        vendor = Vendor.objects.all()
        serializer = VendorGetSerializer(vendor, many=True)
        return Response(serializer.data)
        # return Response({"Vendor": serializer.data})

    def post(self, request, format=None):
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").now()

        serializer = VendorPostSerializer(data=request.data)
        print("db#")
        print(User.objects.get(id=request.data['user']))
        serializer.user = User.objects.get(id=request.data['user'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetVendorShopsView(APIView):
    def get(self, request, vendor_id):
        print("shopDetails")
        print(vendor_id)
        shops = Shop.objects.filter(vendor_id=vendor_id)
        # shop = Shop.objects.all()
        serializer = ShopGetSerializer(shops, many=True)
        return Response({"Shops": serializer.data})


class VendorEditView(RetrieveUpdateAPIView):
    # edit vendor
    def put(self, request, *args, **kwargs):
        # post all the field when editing
        print("put##")
        vendor = Vendor.objects.filter(id=kwargs['vendor_id'])
        is_blocked = request.data['is_blocked']
        is_verified = request.data['is_verified']
        if vendor and is_blocked and is_verified:
            vendor.update(is_blocked=(is_blocked == "true"), is_verified=(is_verified == "true"),
                          modifiedAt=datetime.strptime('24052010', "%d%m%Y").now())
            serializer = VendorGetSerializer(vendor, many=True)
            return Response({"Vendors": serializer.data})
        return Response("Failed to edit vendor", status=status.HTTP_400_BAD_REQUEST)
