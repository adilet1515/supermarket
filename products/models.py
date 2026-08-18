from typing import TYPE_CHECKING

from django.contrib.auth.models import User
from django.db.models.manager import Manager
from django.db import models


class Product(models.Model):
    class Meta:
        ordering = ["name", "price", "pk"]

    name = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True)
    price = models.DecimalField(default=0,max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    if TYPE_CHECKING:
        objects : Manager


    def __str__(self):
        return f"{self.__class__.__name__} (pk={self.id}, name={self.name!r})"


class Order(models.Model):
    promocode = models.CharField(max_length=20, null=True, blank=True)
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ManyToManyField(Product, related_name="orders")

    if TYPE_CHECKING:
        objects: Manager