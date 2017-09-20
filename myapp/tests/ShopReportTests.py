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


class TestShopReport(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="makarov")
        self.user2 = User.objects.create(username="krukov")
        self.vendor = Vendor.objects.create(user=self.user)
        self.subscription = Subscription.objects.create(name="gold", price=1500000)
        self.category = Category.objects.create(name="category")
        self.subcategory = SubCategory.objects.create(name="subCategory", category=self.category)

        for x in ["makarovShop1", "makarovShop2", "makarovShop3", "makarovShop4"]:
            self.shop = Shop.objects.create(name=x, vendor=self.vendor, subscription=self.subscription)

        self.request_data = {
            "name": "makarovShop",
            "vendor": "ab123",
            "subscription": self.subscription,
            "is_blocked": "False"
        }

    def test_get_vendors(self):
        print("vendors#")
        request = self.client.get(reverse("vendors"))
        print(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    # def test_get_driver(self):
    #     print("one driver#")
    #     request = self.client.get(reverse("driver-details", kwargs={'pk': self.driver.id}))
    #     print(request.data)
    #     self.assertEqual(request.status_code, status.HTTP_200_OK)
    #
    # def test_delete_driver(self):
    #     print("delete driver#")
    #     request = self.client.delete(reverse("driver-details", kwargs={'pk': self.driver.id}))
    #     print(request.data)
    #     self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Driver.objects.count(), 3)
    #
    # def test_create_driver(self):
    #     print("create driver#")
    #     for x in range(4):
    #         self.request_data["name"] = ("Makarov123" + str(x))
    #         user = User.objects.create(username="Yuri" + str(x))
    #         self.request_data["user"] = user.id
    #         request = self.client.post(reverse("drivers"), self.request_data, format="json")
    #         print(request.data)
    #         self.assertEqual(request.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Driver.objects.count(), 8)
