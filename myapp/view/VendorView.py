from datetime import datetime

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, ListCreateAPIView

from rest_framework.response import Response

from myapp.models import Vendor, Shop, Order
from myapp.serializers import VendorGetSerializer, VendorPostSerializer, ShopGetSerializer, OrderGetSerializer, \
    ShopPostSerializer


class VendorView(ListCreateAPIView):
    queryset = Vendor.objects.all()

    def get_serializer_class(self):
        if self.request.POST:
            return VendorPostSerializer
        else:
            return VendorGetSerializer


class VendorShopsView(ListCreateAPIView):
    def get_queryset(self):
        return Shop.objects.filter(vendor=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.POST:
            try:
                self.request.POST._mutable = True
                self.request.data['vendor'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return ShopPostSerializer
        else:
            return ShopGetSerializer


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


class VendorOrdersDetailsView(ListAPIView):
    """
    Returns orders from all the shops of the vendor
    """
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        return Order.objects.filter(product__shop__vendor=self.kwargs['pk'])


class VendorShopDetailsView(RetrieveUpdateAPIView):
    """
    Returns details of a Shop
    Allows User to update shop
    """
    lookup_url_kwarg = 'pk2'
    queryset = Shop.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            try:
                self.request.POST._mutable = True
                self.request.data['vendor'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return ShopPostSerializer
        else:
            return ShopGetSerializer
