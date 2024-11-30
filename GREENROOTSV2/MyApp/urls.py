from django.urls import path
from . import views

urlpatterns = [
   # path('', views.home_view, name='home'), 
    path('retailer', views.all_retailer, name='retailers'), 
]