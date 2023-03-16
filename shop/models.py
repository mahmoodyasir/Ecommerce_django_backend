from django.contrib.auth.models import User
from django.db import models
# from model_utils import Choices


class Profile(models.Model):
    prouser = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/images/customers', null=True, blank=True)

    def __str__(self):
        return self.prouser.username


class Category(models.Model):
    title = models.CharField(max_length=199)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='static/images/products', null=True, blank=True)
    market_price = models.PositiveIntegerField()
    selling_price = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title


class WishList(models.Model):
    wishedProduct = models.ManyToManyField(Product)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"wishlist id=={self.id}==Wished Product=={self.wishedProduct}"


class Cart(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    complete = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Cart id=={self.id}==Complete=={self.complete}==Customer=={self.customer}"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart=={self.cart.id}<==>CartProduct:{self.id}==Quantity=={self.quantity}==Customer=={self.cart.customer}"


class Choice(models.Model):
    choice_name = models.CharField(max_length=199)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.choice_name


class Order(models.Model):
    # ORDER_STATUS = Choices(
    #     ("Order Received", "Order Received"),
    #     ("Order Processing", "Order Processing"),
    #     ("On the way", "On the way"),
    #     ("Order Completed", "Order Completed"),
    #     ("Order Canceled", "Order Canceled"),
    #     ("Order pending", "Order pending"),
    # )
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=16)
    email = models.CharField(max_length=200)
    total = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    # order_status = models.CharField(max_length=100, choices=ORDER_STATUS, default="Order pending")
    order_list = models.ForeignKey(Choice, on_delete=models.CASCADE, default=6)
    date = models.DateField(auto_now_add=True)
    payment_complete = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=200, default="offline")
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    transaction_medium = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Order id=={self.id}==Complete=={self.cart.complete}==Customer=={self.cart.customer}"
