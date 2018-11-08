from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import datetime as dt

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
    pub_date = models.DateTimeField(auto_now_add = True, null = True)
    def __str__(self):
        return self.item_name

    @classmethod
    def all_items(cls):
        product = cls.objects()
        return product

    def item_cat(cls):
        funiture = cls.objects.filter(category__pk=7)
        return funiture

    @classmethod
    def search_by_item_name(cls,search_term):
        search_result = cls.objects.filter(item_name__icontains=search_term)
        return search_result
