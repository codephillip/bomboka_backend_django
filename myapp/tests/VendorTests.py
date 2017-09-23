from django.template.defaulttags import lorem
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from myapp.models import *


"""
TESTS GUIDE
assert actual == expected
assertEqual(actual, expected)
assert getOne() == 1
"""


class TestVendor(APITestCase):
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

    def test_get_vendor_shops(self):
        """
        Vendor views all his shops
        """
        url = reverse("vendors-shops", kwargs={'pk': self.vendor.id})
        print(url)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], Shop.objects.filter(vendor=self.vendor).count())

    def test_add_vendor_shop(self):
        """
        Vendor adds shop
        """
        request_data = {
            "name": "makarovShop3",
            "description": "Lorem Ipsum",
            "subscription": self.subscription.id
        }
        url = reverse("vendors-shops", kwargs={'pk': self.vendor.id})
        print(url)
        request = self.client.post(url, request_data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Shop.objects.filter(vendor=self.vendor).count(), 3)