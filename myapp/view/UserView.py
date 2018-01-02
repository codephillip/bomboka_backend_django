from datetime import datetime

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, \
    RetrieveDestroyAPIView, \
    CreateAPIView, UpdateAPIView
from rest_framework.permissions import *

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from myapp.filters import UserFilter
from myapp.models import User, Address, Follow, Order, Discount, FeedbackCategory, Feedback, Product, WishList, Task
from myapp.serializers import UserSerializer, AddressSerializer, AddressPostSerializer, FollowGetSerializer, \
    OrderGetSerializer, DiscountGetSerializer, FeedbackCategorySerializer, FeedbackPostSerializer, \
    FeedbackGetSerializer, \
    UserLoginSerializer, UserGetSerializer, UserPostSerializer, ChangePasswordSerializer, WishListGetSerializer, WishListPostSerializer, \
    TaskSerializer


# todo create user using authentication
class UserCreateView(CreateAPIView):
    """
    Allows creation of user.
    The only operation acceptable is buying products until they upgrade to Vendor, Driver, Courier.
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User


# use base APIView when you dont want to use the
# native functionality like GET, PUT, DELETE, POST..
class UserLoginAPIView(APIView):
    """
    Allows the users to login into the system. 
    Returns a token that will be used for accessing other endpoints.
    """
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
    """
    Returns all users in the system(admins, vendors, users, drivers, couriers).
    """ 
    serializer_class = UserGetSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filter_class = UserFilter
    # '&ordering=-last_login' gives most active users
    # '&ordering=last_login' gives domant users
    ordering_fields = ('last_login',)

    def get_queryset(self):
        return User.objects.all()


class UserDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Allows RUD user
    """
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserGetSerializer


class ChangePasswordView(UpdateAPIView):
    """
    Allows user to change password by providing their old and new password.
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


class UserAddressView(ListCreateAPIView):
    def get_queryset(self):
        return Address.objects.filter(user=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.request.POST._mutable = True
            # exception handling only used for swagger
            try:
                self.request.data['user'] = self.kwargs['pk']
            except Exception as e:
                print(e)
            return AddressPostSerializer
        else:
            return AddressSerializer


class AddressView(ListAPIView):
    """
    Returns all addresses created by users
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class FollowedShopsView(ListCreateAPIView):
    """
    Returns all shops followed by the user. 
    Allows a user to follow a shop.
    """
    # Get all shops followed by user
    serializer_class = FollowGetSerializer

    def get_queryset(self):
        follows = Follow.objects.filter(user_id=self.kwargs['pk'])
        if follows:
            return follows
        raise ValidationError("User has no followed shops")


class UserOrdersDetailsView(ListAPIView):
    """
    Returns all the user's orders.
    """
    serializer_class = OrderGetSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.kwargs['pk'])


class DisplayShopDiscounts(ListAPIView):
    """
    Returns discounts to the user from the shops that they have followed.
    """
    serializer_class = DiscountGetSerializer

    def get_queryset(self):
        follows = Follow.objects.filter(user_id=self.kwargs['pk'])
        shop_id_list = []
        [shop_id_list.append(x.shop_id) for x in follows]
        print(shop_id_list)
        return Discount.objects.filter(product__shop_id__in=shop_id_list)


class FeedbackCategoryView(ListCreateAPIView):
    """
    Create and list feedback categorys that will be selected by the user when writing feedback.
    """
    queryset = FeedbackCategory.objects.all()
    serializer_class = FeedbackCategorySerializer
    permission_classes = (IsAdminUser, IsAuthenticated)


class FeedbackCategoryDetailsView(RetrieveUpdateDestroyAPIView):
    """
    Allows RUD of feedback category.
    """
    queryset = FeedbackCategory.objects.all()
    serializer_class = FeedbackCategorySerializer
    permission_classes = (IsAdminUser,)


class FeedbackView(ListCreateAPIView):
    """
    Allows user to insert feedback.
    Returns all feedbacks.
    """
    queryset = Feedback.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FeedbackPostSerializer
        else:
            return FeedbackGetSerializer


class FeedbackDetailsView(RetrieveDestroyAPIView):
    """
    Allows RD of feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackGetSerializer
    permission_classes = (IsAdminUser,)


class UserWishListView(ListCreateAPIView):
    """
    Returns all products that the user has liked.
    User wishlist is a list of products that the user has liked.
    Allows a user to like a product. Which will be appended to the users Wishlist.
    """

    def get_queryset(self):
        return WishList.objects.filter(user=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WishListPostSerializer
        else:
            return WishListGetSerializer


class UserWishDetailsView(RetrieveDestroyAPIView):
    """
    Returns one liked product.
    Allows the user to unlike a product.
    """
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
