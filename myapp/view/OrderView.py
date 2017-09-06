from myapp.models import Order
from myapp.serializers import OrderGetSerializer, OrderPostSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class UserOrders(ListCreateAPIView):
    # todo add post serializer. VALIDATE CODE
    """
    Returns all orders made by current user
    Allows user to create an order
    """
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        orders = Order.objects.filter(user=self.kwargs['pk'])
        return orders


class OrdersListView(ListCreateAPIView):
    # todo make ListAPIView
    """
    Returns all orders made by all the users
    """
    queryset = Order.objects.all()
    filter_fields = ('is_completed', 'is_cancelled', 'is_accepted', 'is_received')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderPostSerializer
        else:
            return OrderGetSerializer


class OrderDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Allows RUD order
    """
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return OrderPostSerializer
        else:
            return OrderGetSerializer
