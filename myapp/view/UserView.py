from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveDestroyAPIView, \
    CreateAPIView, UpdateAPIView
from rest_framework.permissions import *

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from myapp.models import User, Address, Follow, Order, Discount, FeedbackCategory, Feedback, Product, WishList, Task
from myapp.serializers import UserSerializer, AddressSerializer, AddressPostSerializer, FollowGetSerializer, \
    OrderGetSerializer, DiscountGetSerializer, FeedbackCategorySerializer, FeedbackPostSerializer, \
    FeedbackGetSerializer, \
    UserLoginSerializer, UserGetSerializer, ChangePasswordSerializer, WishListGetSerializer, WishListPostSerializer, \
    TaskSerializer


# todo create user using authentication
class UserCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User


# use base APIView when you dont want to use the
# native functionality like GET, PUT, DELETE, POST..
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserView(ListAPIView):
    # list all users in the system
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    permission_classes = (IsAdminUser,)


class UserDetailsView(RetrieveUpdateDestroyAPIView):
    # view single user, update or delete user
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    permission_classes = (IsAdminUser,)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = User.objects.get(id=kwargs['pk'])
        serializer = self.get_serializer(data=request.data)
        print("data###")
        print(request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

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
    permission_classes = (IsAdminUser, IsAuthenticated)


class FeedbackCategoryDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = FeedbackCategory.objects.all()
    serializer_class = FeedbackCategorySerializer
    permission_classes = (IsAdminUser,)


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
    permission_classes = (IsAdminUser,)


class UserWishListView(ListCreateAPIView):
    """
    User wishlist is a list of products that the user has liked
    """
    def get_queryset(self):
        return WishList.objects.filter(user=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WishListPostSerializer
        else:
            return WishListGetSerializer


class UserWishDetailsView(RetrieveDestroyAPIView):
    serializer_class = WishListGetSerializer
    lookup_url_kwarg = 'pk2'

    def get_queryset(self):
        wishlist = WishList.objects.filter(user=self.kwargs['pk'])
        return wishlist


class TaskViewSet(ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = TaskSerializer

    def list(self, request):
        tasks = {
            1: Task(id=1, name='Demo', owner='xordoquy', status='Done', product=Product.objects.all()[0]),
            2: Task(id=2, name='Model less demo', owner='xordoquy', status='Ongoing', product=Product.objects.all()[0]),
            3: Task(id=3, name='Sleep more', owner='xordoquy', status='New', product=Product.objects.all()[0]),
        }
        serializer = TaskSerializer(
            instance=tasks.values(), many=True)
        return Response({"results": serializer.data})
