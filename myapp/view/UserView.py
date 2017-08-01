from datetime import date, datetime

from django.shortcuts import render
from django.views import View
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import User, Address
from myapp.serializers import UserSerializer, AddressSerializer


class UserView(APIView):
    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response({"User": serializer.data})

    def post(self, request, format=None):
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").date()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").date()
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAddressView(APIView):
    # get all addresses
    def get(self, request, user_id):
        address = Address.objects.filter(user=User.objects.get(id=user_id))
        serializer = AddressSerializer(address, many=True)
        return Response({"Address": serializer.data})


class AddressView(APIView):
    # get all addresses
    def get(self, request, format=None):
        address = Address.objects.all()
        serializer = AddressSerializer(address, many=True)
        return Response({"Address": serializer.data})

    def post(self, request, format=None):
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").date()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").date()
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
