from django.shortcuts import render, get_object_or_404, redirect
from django.http  import HttpResponse
from .models import Product,Category,Profile
from .forms import NewItemForm,UserForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.http import JsonResponse
from cart.forms import CartAddProductForm
import africastalking


# Initialize SDK
# username = "sandbox"    # use 'sandbox' for development in the test environment
# api_key = "4bfc140965fdf936a7de2adada43977c89441a3d4af85286e4fdc2bd7b6e885f" # use your sandbox app API key for development in the test environment
# africastalking.initialize(username, api_key)
#
#
# # Initialize a service e.g. SMS
# sms = africastalking.SMS
#
#
# # Use the service synchronously
# response = sms.send("Hello Message!", ["+2547xxxxxx"])
# print(response)
#
# # Or use it asynchronously
# def on_finish(error, response):
#     if error is not None:
#         raise error
#     print(response)
#
# sms.send("Hello Message!", ["+2547xxxxxx"], callback=on_finish)
# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'index.html',{'category': category,'categories': categories, 'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404 (Product, id=id, slug=slug, available=True)
    categories = Category.objects.all()
    cart_product_form = CartAddProductForm()
    return render(request, 'item_details.html',{'product':product,'cart_product_form': cart_product_form,'categories': categories})

@login_required(login_url='/accounts/login')
def new_item(request):
    categories = Category.objects.all()
    current_user = request.user
    if request.method == 'POST':
        form = NewItemForm(request.POST,request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = current_user
            item.save()
    else:
        form =NewItemForm()
    return render (request, 'new_item.html', {"form":form, "categories":categories})

# def newitem(request):
#         seller_number = request.POST.get('seller_number')
#         seller_location = request.POST.get('seller_location')
#         item_name = request.POST.get('item_name')
#         category = request.POST.get('Category')
#         item_price = request.POST.get('item_price')
#         item_image = request.POST.get('item_image')
#         item_description = request.POST.get('item_description')
#
#         recipient=Item(seller_number=seller_number, seller_location=seller_location, item_name=item_name, category=category, item_price=item_price, item_image=item_image, item_description=item_description)
#         recipient.save()
#         data = {'success': 'Your item has been posted'}
#         return JsonResponse(data)

def search_results(request):
    categories = Category.objects.all()
    if 'name' in request.GET and request.GET["name"]:
        search_term = request.GET.get("name")
        searched_ref = Product.search_by_name(search_term)
        message = f"{search_term}"
        return render(request, "search.html",{"message":message,"name":searched_ref, "categories":categories})
    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message, "item_categories":item_categories})

def posted_by_seller(request, user_id):
    user_posts = Product.objects.filter(seller_id=request.user).order_by('created')[::-1]
    return render(request, 'seller_product.html', {"user_posts":user_posts})

@login_required(login_url='/accounts/login')
def profile(request, user_id):
    profile = Profile.objects.filter(user_id=request.user.id)
    categories = Category.objects.all()
    user_posts = Product.objects.filter(seller_id=request.user).order_by('created')[::-1]


    return render(request, "profile.html", {"profile": profile, "categories":categories, "user_posts":user_posts})

@login_required
@transaction.atomic
def update_profile(request, user_id):
    categories = Category.objects.all()
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
        'profile_form': profile_form, "categories":categories
    })
