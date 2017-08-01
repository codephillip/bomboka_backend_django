from datetime import date, datetime, timezone

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import Vendor, User, Shop, Product, SubCategory, Order
from myapp.serializers import ShopPostSerializer, ShopGetSerializer, ProductGetSerializer, ProductPostSerializer, \
    OrderGetSerializer, OrderPostSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView


class OrderView(APIView):
    # get all orders
    def get(self, request, format=None):
        print("orderview")
        orders = Order.objects.all()
        serializer = OrderGetSerializer(orders, many=True)
        return Response({"Orders": serializer.data})

    # create order
    def post(self, request, format=None):
        request.data['createdAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        request.data['modifiedAt'] = datetime.strptime('24052010', "%d%m%Y").now()
        serializer = OrderPostSerializer(data=request.data)

        print("db#")
        if serializer.is_valid():
            serializer.save()
            return Response({"Orders": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)