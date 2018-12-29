from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Category(models.Model):
    categories = models.CharField(max_length= 100,null= True)
    def __str__(self):
        return self.categories

class Item(models.Model):
    seller = models.ForeignKey(User, null = True)
    seller_number = models.IntegerField(null= True)
    seller_location = models.CharField(null = True,max_length= 100)
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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile_pic/",blank = True, null = True)
    seller_number = models.IntegerField(null= True)
    seller_location = models.CharField(null = True,max_length= 100)

    def save_profile(self):
        self.save()

    @classmethod
    def this_profile(cls):
        profile = cls.objects.all()
        return profile

def Create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(Create_profile,sender=User)
