from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase


class TestDemo(APITestCase):
    def test_user(self):
        assert 1 == 1
        request = self.client.get(reverse("users"))
        print(request.data)

        request = self.client.get(reverse("products"))
        print("testing")
        print(request.data)
        print(request.status_code)

    def test_shop(self):
        request = self.client.get(reverse("users"))
        print(request.data)

