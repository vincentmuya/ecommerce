from django.shortcuts import render, get_object_or_404, redirect
from django.http  import HttpResponse
from .models import Product,Category,Profile
from .forms import NewItemForm,UserForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from cart.forms import CartAddProductForm
import africastalking
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProductSerializer

# Create your views here.
class ProductList(APIView):
    def get(self, request, format=None):
        all_product = Product.objects.all()
        serializers = ProductSerializer(all_product, many=True)
        return Response(serializers.data)

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
            return HttpResponseRedirect('/')
    else:
        form =NewItemForm()
    return render (request, 'new_item.html', {"form":form, "categories":categories})

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
def profile(request, username):
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
