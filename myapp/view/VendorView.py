from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from myapp.models import Vendor, Shop, Order, Book
from myapp.serializers import VendorGetSerializer, VendorPostSerializer, ShopGetSerializer, OrderGetSerializer, \
    ShopPostSerializer


class VendorView(ListCreateAPIView):
    """
    Returns all Vendors in the System
    Allows User to upgrade to Vendor
    """
    queryset = Vendor.objects.all()

    def get_serializer_class(self):
        if self.request.POST:
            return VendorPostSerializer
        else:
            return VendorGetSerializer


class VendorShopsView(ListCreateAPIView):
    """
    Returns all Vendor Shops
    Allows Vendor to create a Shop
    """
    def get_queryset(self):
        return Shop.objects.filter(vendor=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            try:
                self.request.POST._mutable = True
                self.request.data['vendor'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return ShopPostSerializer
        else:
            return ShopGetSerializer


class VendorDetailsView(RetrieveUpdateAPIView):
    """
    Returns details of a Vendor
    Allows Admin to update Vendor
    """
    queryset = Vendor.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return VendorPostSerializer
        else:
            return VendorGetSerializer


class VendorOrdersDetailsView(ListAPIView):
    """
    Returns Orders from all the Shops of the Vendor
    """
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        return Order.objects.filter(product__shop__vendor=self.kwargs['pk'])


class VendorShopDetailsView(RetrieveUpdateAPIView):
    """
    Returns details of a Shop
    Allows Vendor to update Shop
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
