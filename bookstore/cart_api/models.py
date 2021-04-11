from django.db import models

from users.models import User
from books.models import Book

# Create your models here.
class Cart(models.Model):
  status = models.CharField(max_length=255, blank=True, null=True)
  user = models.ForeignKey(User, related_name="carts", on_delete=models.SET_NULL, null=True)
  items = models.ManyToManyField(Book)    
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Order(models.Model):
  cart = models.ForeignKey(Cart, blank=True, null=True, on_delete=models.PROTECT)
  items = models.ManyToManyField(Book) 
  user = models.ForeignKey(User, related_name="orders", on_delete=models.SET_NULL, null=True)
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)