from django.urls import reverse
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
        # create admin user, then authenticate
        # only admin users get list
        self.user = User.objects.create(is_staff=True, is_superuser=True)
        self.user2 = User.objects.create(username="krukov")
        self.vendor = Vendor.objects.create(user=self.user)
        self.subscription = Subscription.objects.create(name="gold", price=1500000)
        self.category = Category.objects.create(name="category")
        self.subcategory = SubCategory.objects.create(name="subCategory", category=self.category)
        self.shop = Shop.objects.create(name="makarovShop", vendor=self.vendor, subscription=self.subscription)
        self.shop2 = Shop.objects.create(name="makarovShop2", vendor=self.vendor, subscription=self.subscription)
        self.client.force_authenticate(user=self.user)

        # add products to two shops, self.shop and self.shop2
        for x in ["iphone1", "iphone2", "iphone3", "iphone4"]:
            Product.objects.create(name=x, price=40000, shop=self.shop, subCategory=self.subcategory)
            Product.objects.create(name=(x+"Product"), price=66000, shop=self.shop2, subCategory=self.subcategory)

    def test_get_shops(self):
        """
        Admin views all shops
        """
        request = self.client.get(reverse("shops"))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_products(self):
        """
        Admin views all products in the platform
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
        User adds a product to shop
        """
        request_data = {
            "name": "Iphone 10",
            "price": 5690000,
            "description": "Nice phone",
            "image": generate_photo_file(),
            "subCategory": self.subcategory.id
        }
        url = reverse("shop-products", kwargs={'pk': self.shop.id})
        print(url)
        request = self.client.post(url, request_data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.filter(shop=self.shop).count(), 5)