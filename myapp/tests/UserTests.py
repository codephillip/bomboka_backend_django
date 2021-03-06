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


class TestUser(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="makarov")
        self.user2 = User.objects.create(username="krukov")
        self.vendor = Vendor.objects.create(user=self.user)
        self.subscription = Subscription.objects.create(name="gold", price=1500000)
        self.category = Category.objects.create(name="category")
        self.subcategory = SubCategory.objects.create(name="subCategory", category=self.category)
        self.shop = Shop.objects.create(name="makarovShop", vendor=self.vendor, subscription=self.subscription)

        for x in range(4):
            product = Product.objects.create(name=get_random_string(length=10), price=40000, shop=self.shop, subCategory=self.subcategory)
            WishList.objects.create(product=product, user=self.user2)

        for x in range(3):
            Address.objects.create(user=self.user, name=get_random_string(length=10), latitude=23.5, longitude=99.4)
            Address.objects.create(user=self.user2, name=get_random_string(length=10), latitude=23.5, longitude=99.4)

        self.products = Product.objects.all()
        # create one extract product for testing
        self.product = Product.objects.create(name="Samsung S7", price=80000, shop=self.shop,
                                              subCategory=self.subcategory)

        # post data template
        self.request_data = {
            "user": "abc123",
            "product": "abc123",
        }

    def test_get_user_wishlist(self):
        print("user's wishlist#")
        url = reverse("user-wishlist", kwargs={'pk': self.user2.id})
        print(url)
        request = self.client.get(url)
        print(request.data)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(WishList.objects.count(), 4)

    def test_post_user_wishlist(self):
        # testing user liking a product for the first time
        print("user's wishlist#")
        url = reverse("user-wishlist", kwargs={'pk': self.user2.id})
        print(url)
        self.request_data["user"] = self.user2.id
        self.request_data["product"] = self.product.id
        request = self.client.post(url, self.request_data)
        print(request.data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WishList.objects.count(), 5)

    def test_post_invalid_user_wishlist(self):
        # testing user liking a product twice
        print("user's wishlist#")
        url = reverse("user-wishlist", kwargs={'pk': self.user2.id})
        print(url)
        self.request_data["user"] = self.user2.id
        self.request_data["product"] = self.products[0].id
        request = self.client.post(url, self.request_data)
        print(request.data)
        # user can like the product only once
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(WishList.objects.count(), 4)

    def test_user_single_wishlist_item(self):
        print("user's wishlist#")
        wishlist = WishList.objects.all().first()
        url = reverse("user-wishlist-details", kwargs={'pk': self.user2.id, 'pk2': wishlist.id})
        print(url)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_user_unlike_product(self):
        print("user's wishlist#")
        wishlist = WishList.objects.all().first()
        url = reverse("user-wishlist-details", kwargs={'pk': self.user2.id, 'pk2': wishlist.id})
        print(url)
        request = self.client.delete(url)
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WishList.objects.count(), 3)

    def test_list_user_addresses(self):
        """
        lists users addresses that are displayed to the user when making an order
        """
        url = reverse("user-addresses", kwargs={'pk': self.user.id})
        print(url)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], Address.objects.filter(user=self.user).count())

    def test_create_user_address(self):
        """
        user creates an address that will be used when making a purchase
        """
        request_data = {
            "name": "Kiwatule",
            "latitude": 76.8,
            "longitude": 92.4,
        }
        url = reverse("user-addresses", kwargs={'pk': self.user2.id})
        print(url)
        request = self.client.post(url, request_data)
        print(request.data)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 7)

    def test_list_all_addresses(self):
        """
        Returns list all addresses created by all users
        """
        url = reverse("address")
        print(url)
        request = self.client.get(url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['count'], 6)
