from datetime import date, datetime

from django.shortcuts import render
from django.views import View
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Vendor, User
from myapp.serializers import VendorGetSerializer, VendorPostSerializer


class VendorView(APIView):

    def get(self, request, format=None):
        vendor = Vendor.objects.all()
        serializer = VendorGetSerializer(vendor, many=True)
        return Response(serializer.data)
        # return Response({"Vendor": serializer.data})

    def post(self, request, format=None):
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").date()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").date()

        serializer = VendorPostSerializer(data=request.data)
        print("db#")
        print(User.objects.get(id=request.data['user']))
        serializer.user = User.objects.get(id=request.data['user'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
