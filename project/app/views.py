from django.shortcuts import render
from django.http  import HttpResponse
from .models import Item
from .forms import NewItemForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    product = Item.objects.all
    return render(request, 'index.html',{"product":product})

@login_required(login_url='/accounts/login')
def new_item(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewItemForm(request.POST,request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = current_user
            item.save()
    else:
        form =NewItemForm()
    return render (request, 'new_item.html', {"form":form})
