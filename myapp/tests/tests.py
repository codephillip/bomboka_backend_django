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


class TestApi(APITestCase):
    def setUp(self):
        pass

    def test_user(self):
        pass
        # todo create user tests
        # request = self.client.get(reverse("users"))
        # print(request.data)
        # request = self.client.get(reverse("products"))
        # print("testing")
        # print(request.data)
        # print(request.status_code)
