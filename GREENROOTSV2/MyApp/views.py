from django.shortcuts import render
from .modelsdel import Retailer,DeliveryofPacked,WarehouseDistribution
from .forms import delPForm
from django.http import HttpResponseRedirect

# Create your views here.
def all_retailer(request):
    ret_list = Retailer.objects.all()
    return render(request, 'retailerlist.html',
                  {'ret_list': ret_list})

def deliveryP(request):  # for reading in CRUD
    packeddel_list = DeliveryofPacked.objects.all()
    return render(request, 'deliveriesP.html',
                  {'packeddel_list': packeddel_list})

def add_delP(request):    #for c in CRUD
    submitted = False
    if request.method == "POST":
        form = delPForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('warehousemanagerDashboard.html?submitted=True')
    else:
        form = delPForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_delP.html',{'form':form,'submitted':submitted})

def WMDash(request):
    packeddel_list_ = DeliveryofPacked.objects.all()
    return render(request,'warehousemanagerDashboard.html',
                  {'packeddel_list': packeddel_list_})

def distrib(request):
    distribution_list =  WarehouseDistribution.objects.all()
    return render(request,'warehousedistribution.html',
                  {'distribution_list': distribution_list})

def homepage(request):
    return render(request,'bg.html')

def index(request):
    return render(request,'index.html')
