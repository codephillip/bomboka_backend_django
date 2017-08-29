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


class TestCountry(APITestCase):
    def setUp(self):
        self.countrys = ["Uganda", "Kenya", "Rwanda", "Tanzania"]
        self.countrys2 = ["Uganda2", "Kenya2", "Rwanda2", "Tanzania2"]
        # create initial four countrys
        for x in self.countrys:
            Country.objects.create(name=x)

        self.request_data = {
            "name": "Uganda",
            "latitude": 33.5,
            "longitude": 29.7,
        }

        self.objects = Country.objects.all()

    def test_get_countrys(self):
        print("countrys#")
        request = self.client.get(reverse("countrys"))
        print(request.data)
        self.assertEqual(4, Country.objects.count())
        self.assertEqual(status.HTTP_200_OK, request.status_code)

    def test_create_country(self):
        print("create country#")
        # create four more countrys
        for x in self.countrys2:
            self.request_data["name"] = x
            request = self.client.post(reverse("countrys"), self.request_data)
            self.assertEqual(status.HTTP_201_CREATED, request.status_code)
        self.assertEqual(8, Country.objects.count())

    def test_get_country(self):
        # get one country
        print("get country#")
        request = self.client.get(reverse("country-details", kwargs={'pk': self.objects[0].id}))
        print(request.data)
        self.assertEqual(status.HTTP_200_OK, request.status_code)

    def test_update_country(self):
        # update four countries
        print("update country#")
        for x in self.objects:
            self.request_data["name"] = (x.name + "_new")
            url = reverse("country-details", kwargs={'pk': str(x.id)})
            print(url)
            request = self.client.put(url, self.request_data)
            self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertEqual(4, Country.objects.count())

    def test_delete_country(self):
        print("delete country#")
        # delete two country
        for count in range(2):
            url = reverse("country-details", kwargs={'pk': self.objects[count].id})
            print(url)
            request = self.client.delete(url)
            self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(2, Country.objects.count())
