from django.shortcuts import render
from django.http  import HttpResponse
from .models import Item,Category
from .forms import NewItemForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    product = Item.objects.all
    clothes = Item.objects.filter(category__pk=6)
    return render(request, 'index.html',{"product":product, "clothes":clothes})

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

def search_results(request):
    if 'item_name' in request.GET and request.GET["item_name"]:
        search_term = request.GET.get("item_name")
        searched_ref = Item.search_by_item_name(search_term)
        message = f"{search_term}"
        return render(request, "search.html",{"message":message,"item_name":searched_ref})
    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})
