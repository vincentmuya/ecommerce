from django.shortcuts import render
from django.http  import HttpResponse
from .models import Item
from .forms import NewItemForm

# Create your views here.
def index(request):
    product = Item.objects.all
    return render(request, 'index.html',{"product":product})

def new_item(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewItemForm(request.POST,request.FILES)
        if form.is_valid():
            newitemform = form.save(commit=False)
            newitemform.save()
    else:
        form =NewItemForm()
    return render (request, 'new_item.html', {"form":form})
