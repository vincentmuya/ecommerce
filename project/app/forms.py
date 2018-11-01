from django import forms
from .models import Item

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['seller', 'pub_date']
        widgets = {

        }
