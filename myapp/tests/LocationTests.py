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
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_country(self):
        print("create country#")
        # create four more countrys
        for x in self.countrys2:
            self.request_data["name"] = x
            request = self.client.post(reverse("countrys"), self.request_data)
            self.assertEqual(request.status_code, status.HTTP_201_CREATED)
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
            self.assertEqual(request.status_code, status.HTTP_200_OK)
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


class TestCity(APITestCase):
    def setUp(self):
        self.citysList = ["Kampala", "Gulu", "Jinja", "Wakiso"]
        self.citysList2 = ["Kampala2", "Gulu2", "Jinja2", "Wakiso2"]
        self.countrysList = ["Uganda", "Kenya", "Rwanda", "Tanzania"]

        # create initial four countrys
        for x in self.countrysList:
            Country.objects.create(name=x)

        # create initial four citys
        for x, y in zip(Country.objects.all(), self.citysList):
            City.objects.create(name=y, country=x)

        self.request_data = {
            "name": "Kampala",
            "country": "abc123",
            "latitude": 33.5,
            "longitude": 29.7,
        }

        self.citys = City.objects.all()
        self.countrys = Country.objects.all()

    def test_get_citys(self):
        print("citys#")
        request = self.client.get(reverse("citys"))
        print(request.data)
        self.assertEqual(4, City.objects.count())
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_create_city(self):
        print("create city#")
        # create four more citys
        for x in self.citysList2:
            self.request_data["name"] = x
            self.request_data["country"] = self.countrys[2].id
            request = self.client.post(reverse("citys"), self.request_data)
            self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(8, City.objects.count())

    def test_get_city(self):
        # get one city
        print("get city#")
        request = self.client.get(reverse("city-details", kwargs={'pk': self.citys[0].id}))
        print(request.data)
        self.assertEqual(status.HTTP_200_OK, request.status_code)

    def test_update_city(self):
        # update four countries
        print("update city#")
        for x in self.citys:
            self.request_data["name"] = (x.name + "_new")
            self.request_data["country"] = self.countrys[1].id
            url = reverse("city-details", kwargs={'pk': x.id})
            print(url)
            request = self.client.put(url, self.request_data)
            self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(4, City.objects.count())

    def test_delete_city(self):
        print("delete city#")
        # delete two city
        for count in range(2):
            url = reverse("city-details", kwargs={'pk': self.citys[count].id})
            print(url)
            request = self.client.delete(url)
            self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(2, City.objects.count())