from django.db import models


class User(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    image = models.CharField(max_length=250)
    dob = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=250)
    image = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=250)
    image = models.CharField(max_length=250)
    category = models.ForeignKey(Category)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User)

    def __str__(self):
        return str(self.user.name)


class Shop(models.Model):
    name = models.CharField(max_length=250)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    vendor = models.ForeignKey(Vendor)

    def __str__(self):
        return self.name


class ShopReview(models.Model):
    comment = models.TextField()
    count = models.FloatField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.shop.name)


class Follow(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.user.name


class Product(models.Model):
    name = models.CharField(max_length=250)
    image = models.CharField(max_length=250)
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
    comment = models.TextField()
    count = models.FloatField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.comment)


class Comment(models.Model):
    email = models.EmailField()
    content = models.CharField(max_length=200)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.email)


class Address(models.Model):
    name = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.name)


class Courier(models.Model):
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.name


class Coverage(models.Model):
    area = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    price = models.IntegerField()
    courier = models.ForeignKey(Courier)

    def __str__(self):
        return self.area


class Order(models.Model):
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
    createdAt = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(Vendor)
    courier = models.ForeignKey(Courier)

    def __str__(self):
        return str(self.courier.user.name)


class Driver(models.Model):
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user.name


class CourierDriver(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    courier = models.ForeignKey(Courier)
    driver = models.ForeignKey(Driver)

    def __str__(self):
        return self.courier.user.name


class Vehicle(models.Model):
    name = models.CharField(max_length=250)

    # todo upload image

    def __str__(self):
        return self.name


class CourierVehicle(models.Model):
    courier = models.ForeignKey(Courier)
    vehicle = models.OneToOneField(Vehicle)

    def __str__(self):
        return self.courier.user.name


class Attribute(models.Model):
    name = models.CharField(max_length=250)
    element = models.CharField(max_length=250, null=True, blank=True)
    parameter = models.CharField(max_length=250, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product)

    def __str__(self):
        return self.product.name


class Discount(models.Model):
    product = models.OneToOneField(Product)
    percentage = models.IntegerField(default=0)
    activated = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    startDate = models.DateTimeField(auto_now_add=True)
    endDate = models.DateTimeField()


class Brand(models.Model):
    # todo upload image
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class ProductBrand(models.Model):
    product = models.OneToOneField(Product)
    brand = models.ForeignKey(Brand)

    def __str__(self):
        return self.product.name
