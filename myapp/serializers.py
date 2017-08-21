from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from myapp.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'username', 'email', 'phone', 'password', 'is_blocked', 'createdAt',
            'image',
            'dob')
        read_only = 'id'

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
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


class ShopGetSerializer(serializers.ModelSerializer):
    vendor = VendorGetSerializer()

    class Meta:
        model = Shop
        fields = (
            'id', 'name', 'is_blocked', 'vendor', 'createdAt', 'modifiedAt')


class ShopPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            'id', 'name', 'is_blocked', 'vendor', 'createdAt', 'modifiedAt')


class CategoryGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'image')


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


class CourierGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Courier
        fields = (
            'id', 'is_verified', 'is_blocked', 'createdAt', 'modifiedAt', 'user')


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
