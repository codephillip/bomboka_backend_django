from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView, \
    CreateAPIView

from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import User, Address, Follow, Order, Discount, FeedbackCategory, Feedback
from myapp.serializers import UserSerializer, AddressSerializer, AddressPostSerializer, FollowGetSerializer, \
    OrderGetSerializer, DiscountGetSerializer, FeedbackCategorySerializer, FeedbackPostSerializer, FeedbackGetSerializer


# todo create user using authentication
class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User


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
        request.data['user'] = user_id
        serializer = AddressPostSerializer(data=request.data)
        print("db#")
        if serializer.is_valid():
            serializer.save()
            return Response({"Orders": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressView(APIView):
    # get all addresses
    def get(self, request, format=None):
        address = Address.objects.all()
        serializer = AddressSerializer(address, many=True)
        return Response({"Address": serializer.data})


class FollowedShopsView(ListCreateAPIView):
    # Get all shops followed by user
    serializer_class = FollowGetSerializer

    def get_queryset(self):
        follows = Follow.objects.filter(user_id=self.kwargs['pk'])
        if follows:
            return follows
        raise ValidationError("User has no followed shops")


class UserOrdersDetailsView(ListAPIView):
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.kwargs['pk'])


class DisplayShopDiscounts(ListAPIView):
    serializer_class = DiscountGetSerializer

    def get_queryset(self):
        follows = Follow.objects.filter(user_id=self.kwargs['pk'])
        shop_id_list = []
        [shop_id_list.append(x.shop_id) for x in follows]
        print(shop_id_list)
        return Discount.objects.filter(product__shop_id__in=shop_id_list)


class FeedbackCategoryView(ListCreateAPIView):
    queryset = FeedbackCategory.objects.all()
    serializer_class = FeedbackCategorySerializer


class FeedbackCategoryDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = FeedbackCategory.objects.all()
    serializer_class = FeedbackCategorySerializer


class FeedbackView(ListCreateAPIView):
    queryset = Feedback.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FeedbackPostSerializer
        else:
            return FeedbackGetSerializer


class FeedbackDetailsView(RetrieveDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackGetSerializer