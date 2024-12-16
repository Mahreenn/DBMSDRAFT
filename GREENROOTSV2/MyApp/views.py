from django.shortcuts import render
from .modelsdel import Retailer,DeliveryofPacked,WarehouseDistribution,PackedProduce
from .forms import delPForm,distribForm,productVisualForm,fscform
from django.http import HttpResponseRedirect,Http404
from django.db.models import Sum
from django.urls import reverse
from django.db import connection
from django.core.exceptions import ValidationError

from .querries import create_all_tables,insert1,insert2

#insert2()
#insert1()
#create_all_tables()


def all_retailer(request):
    ret_list = Retailer.objects.all()
    return render(request, 'retailerlist.html',
                  {'ret_list': ret_list})

def deliveryP(request):  # for r in CRUD
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
    packeddel_list = DeliveryofPacked.objects.all()  
    print(packeddel_list) 
    context = {'packeddel_list': packeddel_list}
    return render(request, 'warehousemanagerDashboard.html', context)


def distrib(request):
    query = """
        SELECT wd.id, wd.date, wd.warehouseid, wd.supname, w.address AS warehouse_address
        FROM warehouse_distribution AS wd
        JOIN warehouse AS w ON wd.warehouseid = w.warehouseid
        """
    sort_by_date_str = request.GET.get('sort_by_date', 'false').lower()
    sort_by_date = sort_by_date_str == 'true'
    
    #sort_by_date = request.GET.get('sort_by_date', 'false').lower() == 'true'
    if sort_by_date:
        query += " ORDER BY wd.date DESC"

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    
    print("Fetched rows:", rows)
    return render(request, 'warehousedistribution.html', {'rows': rows, 'sort_by_date': sort_by_date})

def add_distrib(request):
    submitted = False
    if request.method == "POST":
        form = distribForm(request.POST)
        if form.is_valid():
           # field1 = form.cleaned_data['delivery_id']
            field2 = form.cleaned_data['delivery_date']
            field3 = form.cleaned_data['warehouse_id']
            field4 = form.cleaned_data['supplier_name']
            

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO warehouse_distribution (date, warehouseid,supname)
                    VALUES ( %s, %s, %s)
                """, [ field2, field3, field4])
            
            return HttpResponseRedirect('warehousedistribution.html?submitted=True')
    else:
        form = distribForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_distrib.html',{'form':form,'submitted':submitted})


def update_distrib(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM warehouse_distribution WHERE id = %s", [pk])
        row = cursor.fetchone()

    if not row:
        raise Http404("Distribution record not found.")

    initial_data = {
        'warehouse_id': row[2],  
        'supplier_name': row[3], 
        'delivery_date': row[1],  
    }

    form = distribForm(request.POST or None, initial=initial_data)

    if request.method == 'POST' and form.is_valid():
        warehouse_id = form.cleaned_data['warehouse_id']
        supplier_name = form.cleaned_data['supplier_name']
        delivery_date = form.cleaned_data['delivery_date']

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE warehouse_distribution
                SET warehouseid = %s, supname = %s, delivery_date = %s
                WHERE id = %s
            """, [warehouse_id, supplier_name, delivery_date, pk]) 

        # Redirect to the page where the updated distribution is displayed (change the URL as needed)
        return HttpResponseRedirect(f'warehousedistribution/{pk}/')

    # Render the form if the method is GET or if there are errors in the form
    return render(request, 'add_distrib.html', {'form': form})

def delete_distrib(request, pk):
   if request.method == 'POST':
        query = "DELETE FROM warehouse_distribution WHERE id = %s;"
        with connection.cursor() as cursor:
            cursor.execute(query, [pk])
            if cursor.rowcount == 0:
                raise Http404("Record not found.")
            
        return HttpResponseRedirect(reverse('distrib'))  
   
    

def charts(request):
    submitted = False
    form = productVisualForm(request.POST)
    if request.method == "POST":     
        if form.is_valid():
            brc = form.cleaned_data['Barcode']

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
        'form':form,'submitted':submitted,
    }, )



def FSC(request):
    results = None 
    if request.method == 'POST':
        form = fscform(request.POST)
        if form.is_valid():
            selected_batch_id = form.cleaned_data['batchID']
            
            # If a valid batch ID is selected
            if selected_batch_id:
                query = """
                SELECT 
                    p.product_Name AS product_name,
                    f.address AS farm_address,
                    pf.name AS packing_facility_name,
                    w.address AS warehouse_address,
                    wd.supname AS Supplied_To,
                    v.company_name
                FROM 
                    farm_production fp
                JOIN 
                    harvested_produce hp ON fp.batch_id = hp.batch_id
                JOIN 
                    farm f ON fp.registration_id = f.registration_id
                JOIN 
                    product p ON hp.produceID = p.product_ID
                JOIN
                    delivery_harvested dh ON dh.batch_id = hp.batch_id
                JOIN 
                    packing_facility pf ON pf.facID = dh.facility_id
                JOIN 
                    packed_produce pp ON pp.facilityID = pf.facID
                JOIN 
                    delivery_of_packed dp ON dp.barcode = pp.barcode
                JOIN 
                    warehouse w ON w.warehouseid = dp.warehouse_id
                JOIN 
                    warehouse_distribution wd ON wd.warehouseid = w.warehouseid
                JOIN 
                    vehicle v ON v.vehicle_id = dp.vehicle_id
                WHERE fp.batch_id = %s;
                """
                
                with connection.cursor() as cursor:
                    cursor.execute(query, [selected_batch_id])
                    results = cursor.fetchall()

    else:
        form = fscform()  

    return render(request, 'fsc.html', {'form': form, 'results': results})


def QC(request):
    return render(request,'qualityControl.html')

def homepage(request):
    return render(request,'bg.html')

def index(request):
    return render(request,'index.html')
