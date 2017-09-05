from myapp.models import Order
from myapp.serializers import OrderGetSerializer, OrderPostSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class UserOrders(ListCreateAPIView):
    # get user orders
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        orders = Order.objects.filter(user=self.kwargs['pk'])
        return orders


class OrdersListView(ListCreateAPIView):
    # Get all orders / Create order
    queryset = Order.objects.all()
    filter_fields = ('is_completed', 'is_cancelled', 'is_accepted', 'is_received')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderPostSerializer
        else:
            return OrderGetSerializer


class OrderDetailsView(RetrieveUpdateDestroyAPIView):
    # Get one order / Delete order / Update order
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return OrderPostSerializer
        else:
            return OrderGetSerializer
