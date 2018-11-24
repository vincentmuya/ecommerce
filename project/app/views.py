from django.shortcuts import render, get_object_or_404
from django.http  import HttpResponse
from .models import Item,Category
from .forms import NewItemForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.
def index(request):
    product = Item.objects.filter(created_date__lte=timezone.now()).order_by('created_date')[::-1]
    item_categories = Category.objects.all()
    clothes = Item.objects.filter(category__pk=5)
    return render(request, 'index.html',{"product":product, "item_categories":item_categories ,"clothes":clothes})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'item_details.html',{"item":item})

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

def category_items(request, pk):
    cat_item = Item.objects.filter(category__pk=pk)
    return render(request, "category.html",{"cat_item":cat_item})
