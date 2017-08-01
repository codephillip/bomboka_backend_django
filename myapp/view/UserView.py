from datetime import datetime

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import User, Address
from myapp.serializers import UserSerializer, AddressSerializer


# todo create user using authentication
class UserView(APIView):
    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response({"User": serializer.data})

    def post(self, request, format=None):
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAddressView(APIView):
    # get user addresses
    def get(self, request, user_id):
        address = Address.objects.filter(user=User.objects.get(id=user_id))
        serializer = AddressSerializer(address, many=True)
        return Response({"Address": serializer.data})

    # add user delivery addresses
    def post(self, request, user_id):
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        user = User.objects.get(id=user_id)
        Address.objects.create(user=user, latitude=request.data['latitude'], name=request.data['name'],
                               longitude=request.data['longitude'], createdAt=request.data['createdAt'],
                               modifiedAt=request.data['modifiedAt'])
        address = Address.objects.filter(user_id=user_id)
        serializer = AddressSerializer(address, many=True)
        return Response({"Address": serializer.data})


class AddressView(APIView):
    # get all addresses
    def get(self, request, format=None):
        address = Address.objects.all()
        serializer = AddressSerializer(address, many=True)
        return Response({"Address": serializer.data})
