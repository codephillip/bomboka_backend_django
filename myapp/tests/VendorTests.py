from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APITestCase

from myapp.models import *
from myapp.tests import generate_photo_file

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
        self.courier = Courier.objects.create(user=self.user2)
        self.subscription = Subscription.objects.create(name="gold", price=1500000)
        self.category = Category.objects.create(name="category")
        self.category2 = Category.objects.create(name="category2")
        self.subcategory = SubCategory.objects.create(name="subCategory", category=self.category)
        self.shop = Shop.objects.create(name="makarovShop", vendor=self.vendor, subscription=self.subscription)
        self.shop2 = Shop.objects.create(name="makarovShop2", vendor=self.vendor, subscription=self.subscription)

        self.request_data = {
            "name": "Uganda",
            "user": "abc"
        }

    def test_get_vendor_shops(self):
        """
        Vendor views all his shops
        """
        url = reverse("vendor-shops", kwargs={'pk': self.vendor.id})
        print(url)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], Shop.objects.filter(vendor=self.vendor).count())

    def test_add_vendor_shop(self):
        """
        Vendor adds shop
        """
        request_data = {
            "name": "Super shop",
            "is_blocked": False,
            "vendor": self.vendor.id,
            "subscription": self.subscription.id,
            "address": "Ntinda",
            "phone": "256756878443",
            "store_link": "link",
            "category": [
                self.category.id,
                self.category2.id,
            ],
            "bank_name": "Stanbic",
            "bank_ac_name": "Shop bank ac name",
            "bank_ac_number": "49384949853",
            "mm_number": "256756878443",
            "image": generate_photo_file(),
            "delivery_partners": [
                self.courier.id
            ]
        }
        url = reverse("vendor-shops", kwargs={'pk': self.vendor.id})
        print(url)
        request = self.client.post(url, request_data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Shop.objects.filter(vendor=self.vendor).count(), 3)

    def test_get_vendors(self):
        print("vendors#")
        request = self.client.get(reverse("vendors"))
        print(request.data)
        self.assertEqual(request.data['count'], Vendor.objects.all().count())
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_vendor(self):
        """
        Display Vendor details
        """
        url = reverse("vendor-details", kwargs={'pk': self.vendor.id})
        print(url)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        print("create vendor#")
        # create four more vendors
        for x in range(4):
            user_id = User.objects.create(username=get_random_string(length=10)).id
            self.request_data["user"] = user_id
            request = self.client.post(reverse("vendors"), self.request_data)
            self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 5)

    def test_edit_vendor(self):
        """
        Edit Vendor details
        """
        request_data = {
            "user": self.vendor.user_id,
            "is_blocked": False,
            "is_verified": True
        }
        url = reverse("vendor-details", kwargs={'pk': self.vendor.id})
        print(url)
        request = self.client.put(url, request_data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_vendor_couriers(self):
        """
        View Vendor Couriers (Courier partners)
        """
        url = reverse("vendor-couriers", kwargs={'pk': self.vendor.id})
        print(url)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], VendorCourier.objects.filter(vendor=self.vendor).count())

    def test_add_vendor_courier(self):
        """
        Vendor creates Courier partner
        """
        request_data = {
            "courier": self.courier.id,
        }
        url = reverse("vendor-couriers", kwargs={'pk': self.vendor.id})
        print(url)
        request = self.client.post(url, request_data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VendorCourier.objects.filter(vendor=self.vendor).count(), 1)