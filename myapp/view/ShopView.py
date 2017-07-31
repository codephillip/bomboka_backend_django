from datetime import date, datetime

from django.shortcuts import render
from django.views import View
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Vendor, User, Shop
from myapp.serializers import ShopPostSerializer, ShopGetSerializer


class ShopView(APIView):
    def get(self, request, format=None):
        shop = Shop.objects.all()
        serializer = ShopGetSerializer(shop, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").date()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").date()
        serializer = ShopPostSerializer(data=request.data)

        print("db#")
        print(Vendor.objects.get(id=request.data['vendor']))
        serializer.vendor = Vendor.objects.get(id=request.data['vendor'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
