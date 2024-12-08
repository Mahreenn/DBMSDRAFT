from django.shortcuts import render
from .modelsdel import Retailer,DeliveryofPacked,WarehouseDistribution,PackedProduce
from .forms import delPForm
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.urls import reverse

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

def update_delP(request,pk):
    delp = DeliveryofPacked.objects.get(delivery_id=pk)
    form =delPForm(instance=delp)

    if request.method == 'POST':
        form= delPForm(request.POST, instance=delp)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(reverse('WM') + '?submitted=True')
    context = {'form':form}
    return render(request,'add_delP.html',context)
    

def WMDash(request):
    packeddel_list = DeliveryofPacked.objects.all()  # Ensure this query returns data as expected
    print(packeddel_list)  # Debugging print statement
    context = {'packeddel_list': packeddel_list}
    return render(request, 'warehousemanagerDashboard.html', context)

def distrib(request):
    distribution_list =  WarehouseDistribution.objects.all()
    return render(request,'warehousedistribution.html',
                  {'distribution_list': distribution_list})

def charts(request):
        # Query for bar chart (total quantity delivered over time)
    deliveries = DeliveryofPacked.objects.values('transport_date').annotate(total_quantity=Sum('quantity')).order_by('transport_date')

    bar_chart_data = {
        'labels': [str(delivery['transport_date']) for delivery in deliveries],
        'values': [delivery['total_quantity'] for delivery in deliveries],
    }

    # Query for pie chart (quantity delivered by material type)
    material_data = DeliveryofPacked.objects.values('barcode__material').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')

    pie_chart_data = {
        'labels': [item['barcode__material'] for item in material_data],
        'values': [item['total_quantity'] for item in material_data],
    }

    # Query for line chart (total cost over time)
    cost_data = DeliveryofPacked.objects.values('transport_date').annotate(total_cost=Sum('cost')).order_by('transport_date')

    line_chart_data = {
        'labels': [str(item['transport_date']) for item in cost_data],
        'values': [item['total_cost'] for item in cost_data],
    }

    return render(request, 'charts.html', {
        'bar_chart_data': bar_chart_data,
        'pie_chart_data': pie_chart_data,
        'line_chart_data': line_chart_data,
    })

def QC(request):
    return render(request,'qualityControl.html')


def homepage(request):
    return render(request,'bg.html')

def index(request):
    return render(request,'index.html')
