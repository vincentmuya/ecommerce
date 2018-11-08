from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    categories = models.CharField(max_length= 100,null= True)
    def __str__(self):
        return self.categories

class Item(models.Model):
    seller = models.ForeignKey(User, null = True)
    item_name = models.CharField(max_length= 100)
    category = models.ForeignKey(Category, null =True)
    item_price = models.IntegerField(null=True)
    item_image = models.ImageField(upload_to="posts/",blank = True, null = True)
    item_description = models.TextField(max_length = 1000)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.item_name

    @classmethod
    def search_by_item_name(cls,search_term):
        search_result = cls.objects.filter(item_name__icontains=search_term)
        return search_result

class ShoppingCart(object):

    def __init__(self):
        self.total = 0
        self.items = {}

    def add_item(self,item_name,quantity,item_price):
      self.items[item_name] = quantity
      self.total += item_price*quantity

    def remove_item(self,item_name,quantity,item_price):
      if quantity < self.items[item_name] and quantity >= 0:
          self.total -= item_price*quantity
          self.items[item_name] -= quantity
      elif quantity >= self.items[item_name] :
          del self.items[item_name]

    def checkout(self,cash_paid):
      if cash_paid >= self.total:
          return cash_paid - self.total
      else:
          return "Cash paid not enough"

class Shop(ShoppingCart):
  def __init__(self):
      self.quantity = 100

  def remove_item(self):
      self.quantity -= 1
