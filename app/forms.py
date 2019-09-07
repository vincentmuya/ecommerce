from django import forms
from .models import Product,User,Profile

class NewItemForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['seller', 'created_date', 'published_date', 'slug']
        widgets = {
        }
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('seller_number','seller_location','profile_image',)
        exclude = ['first_name', 'last_name']
        widges = {
        }
