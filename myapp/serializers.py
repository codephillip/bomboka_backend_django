from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from myapp.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'name', 'email', 'phone', 'password', 'is_blocked', 'createdAt', 'modifiedAt', 'image',
            'dob')


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
            'id', 'name', 'image', 'price', 'createdAt', 'modifiedAt', 'shop', 'subCategory')


class ProductPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'image', 'price', 'createdAt', 'modifiedAt', 'shop', 'subCategory')


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


class RatingGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    shop = ShopGetSerializer()

    class Meta:
        model = Rating
        fields = ('id', 'count', 'createdAt', 'user', 'shop')


class RatingPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'count', 'createdAt', 'user', 'shop')


class CoverageGetSerializer(serializers.ModelSerializer):
    courier = CourierGetSerializer()

    class Meta:
        model = Coverage
        fields = ('id', 'area', 'latitude', 'longitude', 'price', 'courier')


class CoveragePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coverage
        fields = ('id', 'area', 'latitude', 'longitude', 'price', 'courier')


class ReviewGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductGetSerializer()

    class Meta:
        model = Review
        fields = ('id', 'comment', 'createdAt', 'user', 'product')


class ReviewPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'comment', 'createdAt', 'user', 'product')

    def validate(self, data):
        print("validate")
        print(self.serializer_url_field)
        user = data['user']
        # user = self._kwargs['user']
        product = data['product']
        review = Review.objects.filter(user=user, product=product)
        if review.exists():
            raise ValidationError("This user has already reviewed the product.")
        return data


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
