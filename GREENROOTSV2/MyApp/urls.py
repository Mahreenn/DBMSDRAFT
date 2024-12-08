from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'), 
    path('retailer', views.all_retailer, name='retailers'), 
    path('index.html', views.index, name='index'),
    path('deliveriesP', views.deliveryP, name='delP'),  #want this to show on warehousemanager dashboard
    path('add_delP.html', views.add_delP, name='add-delP'),
    path('warehousemanagerDashboard.html', views.WMDash, name='WM'),
    path('warehousedistribution.html', views.distrib, name='distrib'),
    path('charts.html', views.charts, name='charts'),
    path('qualityControl.html', views.QC, name='qualitycontrol'),
    path('update-delivery/<int:pk>/', views.update_delP, name='update-delP'),
]