from django import forms
from .models import Product,User,Profile

class NewItemForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['seller', 'slug', 'created_date', 'published_date']
        widgets = {
        }
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('seller_number','seller_location','profile_image',)
        widges = {
        }
