from django.shortcuts import render
from .modelsdel import Retailer,DeliveryofPacked,WarehouseDistribution,PackedProduce
from .forms import delPForm,distribForm,fscform,gradingform,harvestedgradingForm,productnutrition
from django.http import HttpResponseRedirect,Http404
from django.db.models import Sum
from django.urls import reverse
from django.db import connection, IntegrityError
from django.core.exceptions import ValidationError
from .querries import create_all_tables,insert1,insert2
import json

#insert2()
#insert1()
#create_all_tables()


def all_retailer(request):
    ret_list = Retailer.objects.all()
    return render(request, 'retailerlist.html',
                  {'ret_list': ret_list})

def add_delP(request):    #for c in CRUD
    submitted = False
    if request.method == "POST":
        form = delPForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['transport_date']
            quantity = form.cleaned_data['quantity']
            temperature = form.cleaned_data['temperature']
            cost = form.cleaned_data['cost']
            warehouse_id = form.cleaned_data['warehouse_id']
            vehicle_id = form.cleaned_data['vehicle_id']
            barcode = form.cleaned_data['barcode']

            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO delivery_of_packed (transport_date, quantity,temperature,cost,warehouse_id,vehicle_id,barcode)
                    VALUES ( %s, %s, %s,%s,%s,%s,%s)
                """, [ date, quantity, temperature,cost,warehouse_id,vehicle_id,barcode])

            return HttpResponseRedirect('warehousemanagerDashboard.html?submitted=True')
    else:
        form = delPForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'add_delP.html',{'form':form,'submitted':submitted})

def update_delP(request,pk):
     with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM delivery_of_packed WHERE delivery_id = %s", [pk])
        row = cursor.fetchone()
        if not row:
            raise Http404("Distribution record not found.")
        initial_data = {
            'transport_date': row[1],  
            'quantity'      : row[2], 
            'temperature'   : row[3],
            'cost'          : row[4],
            'warehouse_id'   : row[5],
            'vehicle_id'     : row[6],  
            'barcode'        :  row[7],
        }
        form = delPForm(request.POST or None, initial=initial_data)
        if request.method == 'POST' and form.is_valid():
            transport_date = form.cleaned_data['transport_date']
            quantity = form.cleaned_data['quantity']
            temperature = form.cleaned_data['temperature']
            cost = form.cleaned_data['cost']
            warehouse_id = form.cleaned_data['warehouse_id']
            vehicle_id = form.cleaned_data['vehicle_id']
            barcode = form.cleaned_data['barcode']

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE delivery_of_packed
                    SET transport_date = %s, quantity = %s, temperature= %s, cost = %s, warehouse_id = %s, vehicle_id = %s, barcode = %s
                    WHERE delivery_id = %s
                """, [transport_date, quantity, temperature, cost, warehouse_id, vehicle_id, barcode, pk]) 

            return HttpResponseRedirect(reverse('WM'))

        return render(request, 'add_delP.html', {'form': form})

def dlt_delP(request,pk):
    if request.method == 'POST':
        query = "DELETE FROM delivery_of_packed WHERE delivery_id = %s;"
        with connection.cursor() as cursor:
            cursor.execute(query, [pk])
            if cursor.rowcount == 0:
                raise Http404("Record not found.")
        return HttpResponseRedirect(reverse('WM'))
                                            

def WMDash(request):
    query = """ SELECT *
                from delivery_of_packed """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    return render(request, 'warehousemanagerDashboard.html',{'rows': rows} )


def distrib(request):
    query = """
        SELECT wd.id, wd.date, wd.warehouseid, wd.supname, w.address AS warehouse_address
        FROM warehouse_distribution AS wd
        JOIN warehouse AS w ON wd.warehouseid = w.warehouseid
        """
    sort_by_date_str = request.GET.get('sort_by_date', 'false').lower()
    sort_by_date = sort_by_date_str == 'true'
    
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
                SET warehouseid = %s, supname = %s, date = %s
                WHERE id = %s
            """, [warehouse_id, supplier_name, delivery_date, pk]) 

        return HttpResponseRedirect(reverse('distrib'))

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
    if request.method == 'POST':
        form1 = harvestedgradingForm(request.POST)
        if form1.is_valid():
            sowing_date = form1.cleaned_data['sowing_date']
            harvest_date = form1.cleaned_data['harvest_date']
            weight = form1.cleaned_data['weight']
            texture = form1.cleaned_data['texture']
            colour = form1.cleaned_data['colour']
            fungal_growth = form1.cleaned_data['fungal_growth']
            weather_conditions = form1.cleaned_data['weather_conditions']
            pesticides_used = form1.cleaned_data['pesticides_used']
            nutrionistID = int(form1.cleaned_data['nutrionistID'])
            productID = int(form1.cleaned_data['productID'])
            grade = form1.cleaned_data['grade']
            
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO harvested_produce (
                        sowing_date, 
                        harvest_date, 
                        weight, 
                        texture, 
                        colour,
                        fungal_growth,
                        weather_conditions,
                        pesticides_used,
                        nutrionistID,
                        produceID,
                        grade        
                    ) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)
                    """, 
                    [sowing_date, harvest_date, weight, texture, colour, fungal_growth, weather_conditions, pesticides_used,nutrionistID ,productID, grade])
        
            except IntegrityError as e:
                    print(f"Database error: {e}")
                    return render(request, 'charts.html', {'form1': form1, 'error': 'Database error occurred. Please try again later.'})
                    
            return HttpResponseRedirect(request.path) 
    else:
        form1 = harvestedgradingForm()

   #BARCHART
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT grade, COUNT(*) AS grade_count
                FROM harvested_produce
                GROUP BY grade;
            ''')
            result = cursor.fetchall()
    except Exception as e:
        result = []  
    labels = [row[0] for row in result]  
    counts = [row[1] for row in result]  
   
    selected_product = None   
    if request.method == 'POST':
        form2 = productnutrition(request.POST )
        if form2.is_valid():
            selected_batch_id = form2.cleaned_data['batchID']
            
            if selected_batch_id:
                query = """ """
                with connection.cursor() as cursor:
                    cursor.execute(query, [selected_batch_id])
                    results = cursor.fetchall()


    return render(request, 'charts.html', {
        'selected_product': selected_product,
        'labels': labels,
        'counts': counts,
        'form1' :form1,
        'form2' :form2,
    })

def FSC(request):
    results = None 
    if request.method == 'POST':
        form = fscform(request.POST)
        if form.is_valid():
            selected_batch_id = form.cleaned_data['batchID']
            
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
    if request.method == 'POST':
        form = gradingform(request.POST)
        
        if form.is_valid():
            date_received = form.cleaned_data['date_recieved']
            date_expired = form.cleaned_data['inspection_expiry_date']
            ventilation = form.cleaned_data['ventilation']
            cleanliness = form.cleaned_data['cleanliness']
            warehouse_id = int(form.cleaned_data['warehouseid'])
            inspector_id = int(form.cleaned_data['inspector_id'])
            
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO inspection_report (
                        date_received, 
                        date_expired, 
                        ventilation, 
                        cleanliness, 
                        warehouseid, 
                        inspector_id
                    ) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """, 
                    [date_received, date_expired, ventilation, cleanliness, warehouse_id, inspector_id]
                )
            except IntegrityError as e:
                    print(f"Database error: {e}")
                    return render(request, 'qualityControl.html', {'form': form, 'error': 'Database error occurred. Please try again later.'})
                    
            return HttpResponseRedirect(request.path)  
    else:
        form = gradingform()  

    #LINECHART
    query = """
        SELECT warehouseid, AVG(ventilation) AS avg_ventilation, AVG(cleanliness) AS avg_cleanliness
        FROM inspection_report
        GROUP BY warehouseid
        ORDER BY warehouseid;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    warehouses = [row[0] for row in rows]
    ventilation_scores = [float(row[1]) for row in rows]  
    cleanliness_scores = [float(row[2]) for row in rows]  

    context = {
        'form': form,
        'warehouses': json.dumps(warehouses),
        'ventilation_scores': json.dumps(ventilation_scores),
        'cleanliness_scores': json.dumps(cleanliness_scores),
    }

    return render(request, 'qualityControl.html', context)

def homepage(request):
    return render(request,'bg.html')

def index(request):
    return render(request,'index.html')
