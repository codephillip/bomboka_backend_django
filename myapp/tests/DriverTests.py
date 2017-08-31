from django.test import TestCase
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


class TestDriver(APITestCase):
    def setUp(self):
        for x in ["makarov", "krukov", "vladimir", "yuri"]:
            user = User.objects.create(username=x)
            # keep reference of last driver to use in the delete, update test
            self.driver = Driver.objects.create(user=user)
        self.request_data = {
            "name": "Makarov",
            "user": "ab123",
            "is_verified": "True",
            "is_blocked": "False"
        }

    def test_get_drivers(self):
        print("all drivers#")
        request = self.client.get(reverse("drivers"))
        print(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Driver.objects.count(), 4)

    def test_get_driver(self):
        print("one driver#")
        request = self.client.get(reverse("driver-details", kwargs={'pk': self.driver.id}))
        print(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_delete_driver(self):
        print("delete driver#")
        request = self.client.delete(reverse("driver-details", kwargs={'pk': self.driver.id}))
        print(request.data)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Driver.objects.count(), 3)

    def test_create_driver(self):
        print("create driver#")
        for x in range(4):
            self.request_data["name"] = ("Makarov123" + str(x))
            user = User.objects.create(username="Yuri" + str(x))
            self.request_data["user"] = user.id
            request = self.client.post(reverse("drivers"), self.request_data, format="json")
            print(request.data)
            self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 8)
