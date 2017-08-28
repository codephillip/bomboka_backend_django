from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from myapp.models import *


class TestApi(APITestCase):
    def setUp(self):
        pass

    def test_user(self):
        assert 1 == 1
        # request = self.client.get(reverse("users"))
        # print(request.data)

        request = self.client.get(reverse("products"))
        print("testing")
        print(request.data)
        print(request.status_code)

    def test_shop(self):
        request = self.client.get(reverse("shops"))
        self.assertEqual(status.HTTP_200_OK, request.status_code)

        request = self.client.get(reverse("shops"))
        self.assertEqual(status.HTTP_200_OK, request.status_code)

    def test_product(self):
        print("products#")
        request = self.client.get(reverse("products"))
        print(request.data)
        self.assertEqual(status.HTTP_200_OK, request.status_code)

        # request = self.client.get(reverse("product-reviews", args=['1']))
        # self.assertEqual(status.HTTP_200_OK, request.status_code)

    def test_driver(self):
        print("all drivers#")
        request = self.client.get(reverse("drivers"))
        print(request.data)
        self.assertEqual(status.HTTP_200_OK, request.status_code)

        print("one drivers#")
        object = Driver.objects.create(user=User.objects.create())
        print(object.id)
        request = self.client.get(reverse("driver-details", kwargs={'pk': object.id}))
        print(request.data)
        self.assertEqual(status.HTTP_200_OK, request.status_code)

        # object.delete()
        # request = self.client.get(reverse("driver-details", kwargs={'pk': object.id}))
        # print(request.data)
        # self.assertEqual(status.HTTP_404_NOT_FOUND, request.status_code)

        print("drivers#")
        object = Driver.objects.create(user=User.objects.create(username="phillip"))
        print(object.id)
        request = self.client.get(reverse("driver-details", kwargs={'pk': object.id}))
        print(request.data)
        self.assertEqual(status.HTTP_200_OK, request.status_code)

        print("all drivers#")
        for x in range(4):
            object = Driver.objects.create(user=User.objects.create(username=("phillip" + str(x))))
        request = self.client.get(reverse("drivers"), format="json")
        print(request.data)
        self.assertEqual(status.HTTP_200_OK, request.status_code)