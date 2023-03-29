from django.db import models
from common.models import Product


class Visitor(models.Model):
    telegram_id = models.CharField(max_length=255)
    uername = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.telegram_id} - {self.username}"


class Client(models.Model):
    telegram_id = models.CharField(max_length=500, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=355, blank=True, null=True)
    points = models.IntegerField(default=0)
    phone = models.CharField(max_length=50)
    is_banned = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name}"


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    delivered = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client}"

