from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'), 
    path('retailer', views.all_retailer, name='retailers'), 
    path('index.html', views.index, name='index'),
    path('warehousemanagerDashboard.html', views.WMDash, name='WM'),
    path('add_delP.html', views.add_delP, name='adddelP'),
    path('update-delivery/<int:pk>/', views.update_delP, name='updtdelP'),
    path('delete-delivery/<int:pk>/', views.dlt_delP, name='dltdelP'),
    path('warehousedistribution.html', views.distrib, name='distrib'),
    path('add_distrib.html', views.add_distrib, name='adddistrib'),
    path('update-distribution/<int:pk>/', views.update_distrib, name='update-distrib'),
    path('dlt-distribution/<int:pk>/', views.delete_distrib, name='delete-distrib'),
    path('charts.html', views.charts, name='charts'),
    path('qualityControl.html', views.QC, name='qualitycontrol'),
    path('fsc.html', views.FSC, name='foodsupplychain'),
    
]