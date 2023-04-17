from django.contrib.auth.models import AbstractUser
from django.db import models


class UserCustom(AbstractUser):
    fio = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio', 'username']


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)


class Cart(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)


class Order(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE)
    order_price = models.IntegerField(default=0)
