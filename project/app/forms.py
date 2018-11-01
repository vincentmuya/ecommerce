from django import forms
from .models import Item

class NewItemForm(forms.ModelForm):
    # categories = (
    # ("1","Funiture"),
    # ("2","Clothes"),
    # ("3","Electrical")
    # )
    # category = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
    # choices=categories)
    class Meta:
        model = Item
        exclude = ['seller', 'pub_date']
        widgets = {
            # 'level': forms.CheckboxSelectMultiple(),
        }
