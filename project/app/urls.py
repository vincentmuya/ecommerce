from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index,name ='index'),
    url(r'^new/item$', views.new_item, name='new-item'),
    url(r'^search/', views.search_results, name='search_results'),
    url('item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    url(r'^category/(?P<pk>\d+)/$', views.category_items, name='category_items'),
    url(r'^edit/profile/(\d+)$', views.update_profile, name='update-profile'),
    url(r'^profile/(\d+)$', views.profile, name ='profile'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
