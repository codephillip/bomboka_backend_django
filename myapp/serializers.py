from rest_framework import serializers

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
