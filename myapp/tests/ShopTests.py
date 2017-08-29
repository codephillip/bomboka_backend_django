from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from myapp.models import *

"""
TESTS GUIDE
assert expected == actual
assertEqual(expected, actual)
assert 1 == 1
"""


class TestShop(APITestCase):
    def setUp(self):
        pass

    def test_get_shops(self):
        request = self.client.get(reverse("shops"))
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_products(self):
        print("products#")
        request = self.client.get(reverse("products"))
        print(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
