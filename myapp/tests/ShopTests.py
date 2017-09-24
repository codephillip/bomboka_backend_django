from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APITestCase

from myapp.models import *
from myapp.tests.TestUtils import generate_photo_file

"""
TESTS GUIDE
assert actual == expected
assertEqual(actual, expected)
assert getOne() == 1
"""


class TestShop(APITestCase):
    def setUp(self):
        # create Admin, then authenticate
        # only Admins can view all Products and Shops in the System
        self.user = User.objects.create(is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

        self.user2 = User.objects.create(username="krukov")
        self.vendor = Vendor.objects.create(user=self.user)
        self.subscription = Subscription.objects.create(name="gold", price=1500000)
        self.category = Category.objects.create(name="category")
        self.subcategory = SubCategory.objects.create(name="subCategory", category=self.category)
        self.shop = Shop.objects.create(name="makarovShop", vendor=self.vendor, subscription=self.subscription)
        self.shop2 = Shop.objects.create(name="makarovShop2", vendor=self.vendor, subscription=self.subscription)

        for x in range(4):
            self.product = Product.objects.create(name=get_random_string(length=10), price=40000, shop=self.shop, subCategory=self.subcategory)
            self.product2 = Product.objects.create(name=get_random_string(length=10), price=66000, shop=self.shop2, subCategory=self.subcategory)

    def test_get_shops(self):
        """
        Admin views all Shops
        """
        request = self.client.get(reverse("shops"))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_shop(self):
        """
        View details of a single Shop
        """
        url = reverse("vendor-shop-details", kwargs={'pk': self.vendor.id, 'pk2': self.shop.id})
        print(url)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_edit_shop(self):
        """
        Vendor edits Shop
        """
        request_data = {
            "name": "NewName",
            "description": "Lorem Ipsum Lorem Default",
            "subscription": self.subscription.id
        }
        url = reverse("vendor-shop-details", kwargs={'pk': self.vendor.id, 'pk2': self.shop.id})
        print(url)
        request = self.client.put(url, request_data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_products(self):
        """
        Admin views all Products in the System
        """
        request = self.client.get(reverse("products"))
        print(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_shop_products(self):
        """
        View all Shop Products
        """
        url = reverse("shop-products", kwargs={'pk': self.shop.id})
        print(url)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], Product.objects.filter(shop=self.shop).count())

    def test_add_product_to_shop(self):
        """
        Vendor adds a Product to Shop
        """
        request_data = {
            "name": "Iphone 10",
            "price": 5690000,
            "description": get_random_string(length=100),
            "image": generate_photo_file(),
            "subCategory": self.subcategory.id
        }
        url = reverse("shop-products", kwargs={'pk': self.shop.id})
        print(url)
        request = self.client.post(url, request_data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.filter(shop=self.shop).count(), 5)

    def test_edit_shop_product(self):
        """
        Vendor edits a Product in his Shop
        """
        request_data = {
            "name": "NewName",
            "price": 899999,
            "description": get_random_string(length=30),
            "image": generate_photo_file(),
            "subCategory": self.subcategory.id,
        }
        url = reverse("shop-product", kwargs={'pk': self.shop.id, 'pk2': self.product.id})
        print(url)
        request = self.client.put(url, request_data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_shop_product(self):
        """
        View details of single Product in the Shop
        """
        url = reverse("shop-product", kwargs={'pk': self.shop.id, 'pk2': self.product.id})
        print(url)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)