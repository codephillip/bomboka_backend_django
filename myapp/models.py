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
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.id)


class Shop(models.Model):
    name = models.CharField(max_length=250)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    is_blocked = models.BooleanField(default=False)
    vendor = models.ForeignKey(Vendor)

    def __str__(self):
        return self.name


class Rating(models.Model):
    count = models.FloatField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.count)


class Product(models.Model):
    name = models.CharField(max_length=250)
    image = models.CharField(max_length=250)
    price = models.FloatField()
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop)
    subCategory = models.ForeignKey(SubCategory)

    def __str__(self):
        return self.name


class Review(models.Model):
    comment = models.TextField()
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
    user = models.ForeignKey(User)

    def __str__(self):
        return self.user.name


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
        return str(self.createdAt)


class Driver(models.Model):
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    courier = models.ForeignKey(Courier)

    def __str__(self):
        return self.name
