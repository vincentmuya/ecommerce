from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index,name ='index'),
    url(r'^new/item$', views.new_item, name='new-item'),
]
