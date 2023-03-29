from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    req_points = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.title}"


class Category(models.Model):
    title = models.CharField(max_length=255)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}"


class Promo(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    promocode = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.promocode} {self.category.points}"


