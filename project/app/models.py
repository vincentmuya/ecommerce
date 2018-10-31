from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length= 100)
    item_image = models.ImageField(upload_to="posts/",blank = True, null = True)
    item_description = models.TextField(max_length = 1000)

    def __str__(self):
        return self.item_name

    @classmethod
    def all_items(cls):
        product = cls.objects()
        return product
