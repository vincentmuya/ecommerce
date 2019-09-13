from django.shortcuts import render, get_object_or_404, redirect
from django.http  import HttpResponse
from .models import Product,Category,Profile
from .forms import NewItemForm,UserForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.http import JsonResponse
from cart.forms import CartAddProductForm
from django.views import generic
from braces.views import LoginRequiredMixin

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from . import models
# from . import utils
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q

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

class DialogListView(LoginRequiredMixin, generic.ListView):
    template_name = 'dialogs.html'
    model = models.Dialog
    ordering = 'modified'

    def get_queryset(self):
        dialogs = models.Dialog.objects.filter(Q(owner=self.request.user) | Q(opponent=self.request.user))
        return dialogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.kwargs.get('username'):
            # TODO: show alert that user is not found instead of 404
            user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
            dialog = utils.get_dialogs_with_user(self.request.user, user)
            if len(dialog) == 0:
                dialog = models.Dialog.objects.create(owner=self.request.user, opponent=user)
            else:
                dialog = dialog[0]
            context['active_dialog'] = dialog
        else:
            context['active_dialog'] = self.object_list[0]
        if self.request.user == context['active_dialog'].owner:
            context['opponent_username'] = context['active_dialog'].opponent.username
        else:
            context['opponent_username'] = context['active_dialog'].owner.username
        context['ws_server_path'] = '{}://{}:{}/'.format(
            settings.CHAT_WS_SERVER_PROTOCOL,
            settings.CHAT_WS_SERVER_HOST,
            settings.CHAT_WS_SERVER_PORT,
        )
        return context
