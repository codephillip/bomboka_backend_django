import jwt
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, CharField
from rest_framework_jwt.utils import jwt_payload_handler

from bomboka_backend.settings import SECRET_KEY
from myapp.models import *


class UserSerializer(serializers.ModelSerializer):
    # todo needs serious refactoring since UserGetSerializer is more active than UserSerializer
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')

    class Meta:
        model = User
        # todo refine user fields for signup
        fields = (
            'id', 'first_name', 'last_name', 'email', 'email2', 'phone', 'password', 'is_blocked', 'createdAt',
            'image',
            'dob')
        read_only = ['id', 'email2']
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        # user can only register one email address.
        # verify that user inserted correct email address
        # todo check if email exists by sending welcome message
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match.")
        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        return value

    def validate_phone(self, value):
        # user can only register one phone number
        user = User.objects.filter(phone=value)
        if user.exists():
            raise ValidationError("This user has already registered with the phone number")
        return value

    def validate(self, data):
        return data

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            # username is a combination of first and last name
            username=validated_data['first_name'] + validated_data['last_name'],
            email=validated_data['email'],
            # email2 is redundant. however it prevents
            # 500 response when user is successfully created
            email2=validated_data['email2'],
            phone=validated_data['phone'],
            is_blocked=validated_data['is_blocked'],
            image=validated_data['image'],
            dob=validated_data['dob']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

        # def update(self, instance, validated_data):
        #     instance.password.set_password(validated_data.get('password', instance.password))


def create_token(user=None):
    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, SECRET_KEY)
    return token.decode('unicode_escape')


class UserLoginSerializer(serializers.ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=True, required=False)
    email = EmailField(label='Email Address', allow_blank=True, required=False)
    phone = CharField(label='Phone Number', allow_blank=True, required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone',
            'password',
            'token',
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_object = None
        username = data.get('username', None)
        email = data.get('email', None)
        phone = data.get('phone', None)
        password = data['password']
        # User logs in with username, email or phone. Plus password
        if username or email or phone:
            # Q allows robust filtering,
            # distinct returns only one object incase there are duplicates
            user = User.objects.filter(
                Q(username=username) |
                Q(email=email) |
                Q(phone=phone)
            ).distinct()

            if user.exists() and user.count() == 1:
                user_object = user.first()
                if user_object:
                    if not user_object.check_password(password):
                        raise ValidationError("Incorrect credentials. Please try again")
            else:
                raise ValidationError("Login failure. Invalid username, email or phone number.")

            data['token'] = create_token(user_object)
            print(user_object.image)
            data['image'] = user_object.image
            data['username'] = user_object.username
            data['first_name'] = user_object.first_name
            data['last_name'] = user_object.last_name
            return data
        else:
            raise ValidationError("A username, email or phone number is required to login")


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'username', 'email', 'phone',
            'image', 'password', 'gender', 'dob')


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email', 'phone',
            'image', 'password', 'gender', 'dob')

    def create(self, validated_data):
        """
        Sets user password.
        NOTE: Without this, User will never sign_in and password will not be encrypted
        """
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class VendorGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Vendor
        fields = (
            'id', 'is_verified', 'is_blocked', 'user', 'createdAt', 'modifiedAt')


class VendorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            'id', 'is_verified', 'is_blocked', 'user', 'createdAt', 'modifiedAt')


class CategoryGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'image')


class CourierGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Courier
        fields = ('id', 'is_verified', 'is_blocked', 'createdAt', 'modifiedAt', 'user')


class ShopGetSerializer(serializers.ModelSerializer):
    vendor = VendorGetSerializer(read_only=True)
    delivery_partners = CourierGetSerializer(read_only=True, many=True)
    category = CategoryGetSerializer(read_only=True, many=True)

    class Meta:
        model = Shop
        fields = (
            'id', 'name', 'is_blocked', 'vendor', 'subscription', 'createdAt', 'modifiedAt', 'address', 'phone',
            'store_link', 'category', 'bank_name', 'bank_ac_name', 'bank_ac_number', 'mm_number', 'image',
            'delivery_partners')


class ShopPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            'id', 'name', 'is_blocked', 'vendor', 'subscription', 'createdAt', 'modifiedAt', 'address', 'phone',
            'store_link', 'category', 'bank_name', 'bank_ac_name', 'bank_ac_number', 'mm_number', 'image',
            'delivery_partners')


class SubCategoryGetSerializer(serializers.ModelSerializer):
    category = CategoryGetSerializer()

    class Meta:
        model = SubCategory
        fields = (
            'id', 'name', 'image', 'category')


class ProductGetSerializer(serializers.ModelSerializer):
    shop = ShopGetSerializer()
    subCategory = SubCategoryGetSerializer()

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'image', 'price', 'description', 'createdAt', 'modifiedAt', 'shop', 'subCategory')


class ProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'image', 'price', 'description', 'createdAt', 'modifiedAt', 'shop', 'subCategory')


class AddressSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Address
        fields = (
            'id', 'name', 'latitude', 'longitude', 'createdAt', 'modifiedAt', 'user')


class AddressPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'id', 'name', 'latitude', 'longitude', 'createdAt', 'modifiedAt', 'user')


class CourierPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = (
            'id', 'is_verified', 'is_blocked', 'createdAt', 'modifiedAt', 'user')


class VendorCouriersGetSerializer(serializers.ModelSerializer):
    vendor = VendorGetSerializer()
    courier = CourierGetSerializer()

    class Meta:
        model = VendorCourier
        fields = ('id', 'createdAt', 'vendor', 'courier')


class VendorCouriersPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorCourier
        fields = ('id', 'createdAt', 'vendor', 'courier')


class OrderGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()
    product = ProductGetSerializer()
    courier = CourierGetSerializer()

    class Meta:
        model = Order
        fields = (
            'id', 'is_received', 'is_accepted', 'is_cancelled', 'is_completed', 'createdAt', 'modifiedAt', 'address',
            'product', 'user', 'courier')


class OrderPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id', 'is_received', 'is_accepted', 'is_cancelled', 'is_completed', 'createdAt', 'modifiedAt', 'address',
            'product', 'user', 'courier')


class ShopReviewGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    shop = ShopGetSerializer()

    class Meta:
        model = ShopReview
        fields = ('id', 'count', 'comment', 'createdAt', 'user', 'shop')


class ShopReviewPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopReview
        fields = ('id', 'count', 'comment', 'createdAt', 'user', 'shop')


class CoverageGetSerializer(serializers.ModelSerializer):
    courier = CourierGetSerializer()

    class Meta:
        model = Coverage
        fields = ('id', 'area', 'latitude', 'longitude', 'price', 'courier')


class CoveragePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coverage
        fields = ('id', 'area', 'latitude', 'longitude', 'price', 'courier')


class DriverGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = (
            'id', 'is_verified', 'is_blocked', 'createdAt', 'modifiedAt', 'user')


class DriverPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = (
            'id', 'is_verified', 'is_blocked', 'createdAt', 'modifiedAt', 'user')


class CourierDriversGetSerializer(serializers.ModelSerializer):
    courier = CourierGetSerializer()
    driver = DriverGetSerializer()

    class Meta:
        model = CourierDriver
        fields = ('id', 'createdAt', 'courier', 'driver')


class CourierDriversPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierDriver
        fields = ('id', 'createdAt', 'courier', 'driver')

    def validate(self, data):
        print("validate")
        print(self.serializer_url_field)
        user = data['courier']
        product = data['driver']
        courierDriver = CourierDriver.objects.filter(courier=user, driver=product)
        if courierDriver.exists():
            raise ValidationError("This driver is already a courier partner.")
        return data


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class CourierVehicleGetSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()

    class Meta:
        model = CourierVehicle
        fields = ('id', 'courier', 'vehicle')


class CourierVehiclePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierVehicle
        fields = '__all__'


class ProductReviewGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductGetSerializer()

    class Meta:
        model = ProductReview
        fields = ('id', 'count', 'comment', 'createdAt', 'user', 'product')


class ProductReviewPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ('id', 'count', 'comment', 'createdAt', 'user', 'product')

    def validate(self, data):
        print("validate")
        print(self.serializer_url_field)
        user = data['user']
        # user = self._kwargs['user']
        product = data['product']
        review = ProductReview.objects.filter(user=user, product=product)
        if review.exists():
            raise ValidationError("This user has already reviewed the product.")
        return data


class AttributeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ('id', 'name', 'element', 'parameter', 'createdAt', 'product')


class AttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class FollowGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    shop = ShopGetSerializer()

    class Meta:
        model = Follow
        fields = ('id', 'createdAt', 'shop', 'user')


class FollowReportSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    shop = ShopGetSerializer()
    buyers_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Follow
        fields = ('id', 'createdAt', 'shop', 'user', 'buyers_percentage')


class FollowPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('id', 'createdAt', 'shop', 'user')

    def validate(self, data):
        follow = Follow.objects.filter(user=data['user'], shop=data['shop'])
        if follow.exists():
            raise ValidationError("This user has already followed the shop.")
        return data


class DiscountGetSerializer(serializers.ModelSerializer):
    product = ProductGetSerializer()

    class Meta:
        model = Discount
        fields = ('id', 'product', 'percentage', 'activated', 'createdAt', 'startDate', 'endDate')


class DiscountPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductBrandPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = '__all__'

# todo move to product
class ProductBrandGetSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = ProductBrand
        fields = ('id', 'product', 'brand')


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class FeedbackCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackCategory
        fields = '__all__'


class FeedbackPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class FeedbackGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    category = FeedbackCategorySerializer()

    class Meta:
        model = Feedback
        fields = ('id', 'content', 'category', 'user')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CityGetSerializer(serializers.ModelSerializer):
    country = CountrySerializer(required=False, read_only=True)

    class Meta:
        model = City
        fields = ('id', 'name', 'country', 'latitude', 'longitude')


class CityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'country', 'latitude', 'longitude')


class WishListGetSerializer(serializers.ModelSerializer):
    product = ProductGetSerializer()

    class Meta:
        model = WishList
        fields = ('id', 'user', 'product', 'createdAt')


class WishListPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ('id', 'user', 'product', 'createdAt')

    def validate(self, data):
        # user can like the product only once
        wishlist = WishList.objects.filter(user=data['user'], product=data['product'])
        if wishlist.exists():
            raise ValidationError("This user has already liked the product.")
        return data


class ShopReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = '__all__'


STATUSES = (
    'New',
    'Ongoing',
    'Done',
)


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)
    owner = serializers.CharField(max_length=256)
    status = serializers.ChoiceField(choices=STATUSES, default='New')
    product = ProductGetSerializer(read_only=True)