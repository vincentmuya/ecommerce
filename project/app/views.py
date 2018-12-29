from django.shortcuts import render, get_object_or_404, redirect
from django.http  import HttpResponse
from .models import Item,Category,Profile
from .forms import NewItemForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction

# Create your views here.
def index(request):
    product = Item.objects.filter(created_date__lte=timezone.now()).order_by('created_date')[::-1]
    item_categories = Category.objects.all()
    return render(request, 'index.html',{"product":product, "item_categories":item_categories })

def item_detail(request, pk):
    item_categories = Category.objects.all()
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'item_details.html',{"item":item, "item_categories":item_categories})

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
    item_categories = Category.objects.all()
    if 'item_name' in request.GET and request.GET["item_name"]:
        search_term = request.GET.get("item_name")
        searched_ref = Item.search_by_item_name(search_term)
        message = f"{search_term}"
        return render(request, "search.html",{"message":message,"item_name":searched_ref, "item_categories":item_categories})
    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message, "item_categories":item_categories})

def category_items(request, pk):
    item_categories = Category.objects.all()
    cat_item = Item.objects.filter(category__pk=pk)
    return render(request, "category.html",{"cat_item":cat_item, "item_categories":item_categories})

@login_required(login_url='/accounts/login')
def profile(request, user_id):
    profile = Profile.objects.filter(user_id=request.user.id)
    print(profile)
    posts  = Item.objects.filter(user_id=user_id)

    return render(request, "profile.html", {"profile": profile, "posts": posts})

@login_required
@transaction.atomic
def update_profile(request, user_id):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
