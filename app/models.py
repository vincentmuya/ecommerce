from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200,db_index=True, null = True)
    slug = models.SlugField(max_length=200,db_index=True, unique=True, null = True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category',args=[self.slug])

class Product(models.Model):
    seller = models.ForeignKey(User, null = True,on_delete=models.DO_NOTHING,)
    category = models.ForeignKey(Category, related_name='products', null = True ,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, null = True)
    image = models.ImageField(upload_to="posts/",blank = True, null = True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])

    @classmethod
    def search_by_name(cls,search_term):
        search_result = cls.objects.filter(name__icontains=search_term)
        return search_result

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="profile_pic/",blank = True, null = True)
    seller_number = models.IntegerField(blank = True, null = True )
    seller_location = models.CharField(blank = True,max_length= 100, null = True)

    def save_profile(self):
        self.save()

    # def __str__(self):
    #     return self.user

    @classmethod
    def this_profile(cls):
        profile = cls.objects.all()
        return profile

def Create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(Create_profile,sender=User)
