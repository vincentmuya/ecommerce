from django.contrib import admin
from .models import Product, Category, Profile

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug']
#     prepopulated_fields = {'slug':('name')}
# admin.site.register(Category, CategoryAdmin)
#
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
#     list_filter = ['available', 'created', 'updated',]
#     list_editable = ['price', 'stock', 'available']
#     prepopulated_fields = {'slug':('name,')}
# admin.site.register(Product, ProductAdmin)

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Profile)
