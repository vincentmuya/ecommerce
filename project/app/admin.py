from django.contrib import admin
from .models import Item, Category, Profile

# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Profile)
