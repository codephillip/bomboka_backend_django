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


class UserOrders(APIView):
    # get user orders
    def get(self, request, user_id):
        print("orderview")
        orders = Order.objects.filter(user_id=user_id)
        serializer = OrderGetSerializer(orders, many=True)
        return Response({"Orders": serializer.data})


class OrdersListView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer


# using pk
class OrderDetailsView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer


# using custom value other than <pk> in url
# class OrderDetailsView(RetrieveAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderGetSerializer
#     # field to query in table
#     lookup_field = 'pk'
#     # the value pass in url
#     lookup_url_kwarg = 'order_id'


class OrderUpdateView(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderPostSerializer


class OrderDestroyView(RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderPostSerializer
