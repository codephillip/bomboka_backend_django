from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APITestCase

from myapp.models import *

"""
TESTS GUIDE
assert actual == expected
assertEqual(actual, expected)
assert getOne() == 1
"""


class TestCourier(APITestCase):
    def setUp(self):
        for x in range(4):
            self.user = User.objects.create(username=get_random_string(length=10))
            self.courier = Courier.objects.create(user=self.user)

        self.request_data = {
            "user": "ab123",
            "is_verified": "True",
            "is_blocked": "False"
        }

    def test_get_couriers(self):
        request = self.client.get(reverse("couriers"))
        print(request.data)
        self.assertEqual(request.data['count'], Courier.objects.all().count())
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_courier(self):
        user_id = User.objects.create(username=get_random_string(length=10)).id
        self.request_data["user"] = user_id
        request = self.client.post(reverse("couriers"), self.request_data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Courier.objects.count(), 5)
