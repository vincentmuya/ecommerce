from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length= 100)
    item_image = models.ImageField(upload_to="posts/",blank = True, null = True)
    item_description = HTMLField()
