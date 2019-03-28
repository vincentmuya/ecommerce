from django import forms
from .models import Item,User,Profile

class NewItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = ['seller', 'created_date', 'published_date']
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
