from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.product_list, name ='product_list'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',views.product_detail,name='product_detail'),
    url(r'^(?P<category_slug>[-\w]+)/$',views.product_list,name='product_list_by_category'),
    url(r'^new/item$', views.new_item, name='new-item'),
    url(r'^search$', views.search_results, name='search_results'),
    url(r'^edit/profile/(\d+)$', views.update_profile, name='update-profile'),
    url(r'^profile/(\d+)$', views.profile, name ='profile'),
    url(r'^seller/products(\d+)$', views.posted_by_seller, name ='posted_by_seller'),
    # url(r'^ajax/newitem/$', views.newitem, name='newitem'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
