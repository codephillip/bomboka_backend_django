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

        self.countrys = Country.objects.all()

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
        request = self.client.get(reverse("country-details", kwargs={'pk': self.countrys[0].id}))
        print(request.data)
        self.assertEqual(status.HTTP_200_OK, request.status_code)

    def test_update_country(self):
        # update four countries
        print("update country#")
        for x in self.countrys:
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
            url = reverse("country-details", kwargs={'pk': self.countrys[count].id})
            print(url)
            request = self.client.delete(url)
            self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(2, Country.objects.count())
