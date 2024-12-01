from django.shortcuts import render
from .modelsdel import Retailer

# Create your views here.
def all_retailer(request):
    ret_list = Retailer.objects.all()
    return render(request, 'retailerlist.html',
                  {'ret_list': ret_list})