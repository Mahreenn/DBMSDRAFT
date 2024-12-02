from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'), 
    path('retailer', views.all_retailer, name='retailers'), 
    path('index.html', views.index, name='index'),
    path('Tracking.html', views.deliveryP, name='delP'),
    path('add_delP', views.add_delP, name='add-delP'),
]