import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from myapp.utils.constants import *

GENDER_CHOICES = (
    (GENDER_MALE, 'male'),
    (GENDER_FEMALE, 'female'),
    (GENDER_NOT_SPECIFIED, 'not specified'),
)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=12, validators=[
        RegexValidator(
            regex='^(256|254|255)[0-9]{9}$',
            message='Wrong phone number format',
        ),
    ])
    email2 = models.EmailField()
    gender = models.IntegerField(choices=GENDER_CHOICES, default=GENDER_NOT_SPECIFIED)
    createdAt = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile/', max_length=254)
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='category/', max_length=254)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='sub_category/', max_length=254)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User)

    def __str__(self):
        return str(self.user.username)


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='subscription/', max_length=254)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.name


class Shop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    subscription = models.ForeignKey(Subscription)
    vendor = models.ForeignKey(Vendor)

    def __str__(self):
        return self.name


class ShopReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField()
    count = models.FloatField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.shop.name)


class Follow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='product/', max_length=254)
    brand = models.CharField(max_length=250)
    price = models.FloatField()
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop)
    subCategory = models.ForeignKey(SubCategory)

    def __str__(self):
        return self.name


class ProductReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.TextField()
    count = models.FloatField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.comment)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField()
    content = models.CharField(max_length=200)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.email)


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.name)


class Courier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username


class Coverage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    area = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    price = models.IntegerField()
    courier = models.ForeignKey(Courier)

    def __str__(self):
        return self.area


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User)
    address = models.ForeignKey(Address)
    product = models.ForeignKey(Product)
    courier = models.ForeignKey(Courier)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    is_received = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    # once completed, the orders will be removed from the cart
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name


class VendorCourier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(Vendor)
    courier = models.ForeignKey(Courier)

    def __str__(self):
        return str(self.courier.user.username)


class Driver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.username


class CourierDriver(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    courier = models.ForeignKey(Courier)
    driver = models.ForeignKey(Driver)

    def __str__(self):
        return self.courier.user.username


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='vehicle/', max_length=254)

    def __str__(self):
        return self.name


class CourierVehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    courier = models.ForeignKey(Courier)
    vehicle = models.OneToOneField(Vehicle)

    def __str__(self):
        return self.courier.user.username


class Attribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    element = models.CharField(max_length=250, null=True, blank=True)
    parameter = models.CharField(max_length=250, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product)

    def __str__(self):
        return self.product.name


class Discount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product)
    percentage = models.IntegerField(default=0)
    activated = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    startDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField()


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='brand/', max_length=254)

    def __str__(self):
        return self.name


class ProductBrand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product)
    brand = models.ForeignKey(Brand)

    def __str__(self):
        return self.product.name


class FeedbackCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    category = models.ForeignKey(FeedbackCategory)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.user.username


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, unique=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.name
