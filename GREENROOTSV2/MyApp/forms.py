from django import forms
from django.forms import ModelForm
#from .modelsdel import DeliveryofPacked
from django.db import connection

class delPForm(forms.Form):
    transport_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),label="Transport Date" )
    quantity = forms.FloatField(label="Quantity (in units)",min_value=0.0)
    temperature = forms.FloatField(label="Temperature (°C)")
    cost = forms.FloatField(label="Cost (BDT)",min_value=0.0,)           
    warehouse_id = forms.ChoiceField(label="Warehouse ID", required=True)
    vehicle_id = forms.ChoiceField(label="vehicle id", required=True)
    barcode =  forms.ChoiceField(label="barcode", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        q1 = """SELECT warehouseid
                  FROM warehouse;"""
        with connection.cursor() as cursor:
            cursor.execute(q1)
            rows = cursor.fetchall()
        warehouse_choices = [('', '  ')] + [(row[0], row[0]) for row in rows]
        self.fields['warehouse_id'].choices = warehouse_choices

        q2 = """SELECT vehicle_id
                  FROM vehicle;"""
        with connection.cursor() as cursor:
            cursor.execute(q2)
            rows2 = cursor.fetchall()
        vehicles = [('', '   ')] + [(row[0], row[0]) for row in rows2]
        self.fields['vehicle_id'].choices = vehicles

        q3 = """SELECT barcode
                  FROM packed_produce;"""
        with connection.cursor() as cursor:
            cursor.execute(q3)
            rows3 = cursor.fetchall()
        barcodes = [('', '  ')] + [(row[0], row[0]) for row in rows3]
        self.fields['barcode'].choices = barcodes


class distribForm(forms.Form):
    warehouse_id = forms.ChoiceField(label="Warehouse ID", required=True)
    supplier_name = forms.ChoiceField(label="Supplier Name", required=True)
    delivery_date = forms.DateField(label="Delivery Date", widget=forms.SelectDateWidget(years=range(2016, 2025)))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   

        query = """SELECT name
                  FROM supplier;"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        supplier_choices = [('', 'Choose a supplier')] + [(row[0], row[0]) for row in rows]

        self.fields['supplier_name'].choices = supplier_choices

        q1 = """SELECT warehouseid
                  FROM warehouse;"""
        with connection.cursor() as cursor:
            cursor.execute(q1)
            rows = cursor.fetchall()

        warehouse_choices = [('', 'Choose warehouse ID')] + [(row[0], row[0]) for row in rows]

        self.fields['warehouse_id'].choices = warehouse_choices

    
class productnutrition(forms.Form):
    barcode = forms.ChoiceField(label="barcode of the packaged produce:", required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        query = """SELECT barcode
                  FROM nutrition_content_report"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        choices = [('', 'Choose a product barcdoe:')] + [(row[0], row[0]) for row in rows]
        self.fields['barcode'].choices = choices

class harvestedgradingForm(forms.Form):
    sowing_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    harvest_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    weight = forms.FloatField(min_value=0, required=True)
    texture = forms.CharField(max_length=50, required=True)
    colour = forms.CharField(max_length=50, required=True)
    fungal_growth = forms.BooleanField(required=False)
    weather_conditions = forms.CharField(max_length=50, required=True)
    pesticides_used = forms.BooleanField(required=False)
    nutrionistID = forms.ChoiceField(required=True)
    productID = forms.ChoiceField(required=True)
    grade = forms.ChoiceField(choices=[('Ungraded', 'Ungraded'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], initial='Ungraded', required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        q1 = """SELECT NspecialistID
                  FROM nutrition_specialist;"""
        with connection.cursor() as cursor:
            cursor.execute(q1)
            rows = cursor.fetchall()
        nutritionists = [('', 'nutrionistID:')] + [(row[0], row[0]) for row in rows]
        self.fields['nutrionistID'].choices = nutritionists

        q2 = """SELECT product_ID
                  FROM product;"""
        with connection.cursor() as cursor2:
            cursor2.execute(q2)
            rows2 = cursor2.fetchall()
        prods = [('', 'products:')] + [(row[0], row[0]) for row in rows2]
        self.fields['productID'].choices = prods

class fscform(forms.Form):
    batchID = forms.ChoiceField(label="Choose a harvest Batch ID to track its journey through the supply chain:", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        query = """SELECT batch_id
                  FROM harvested_produce;"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        batches = [('', 'batch ID:')] + [(row[0], row[0]) for row in rows]
        self.fields['batchID'].choices = batches

class gradingform(forms.Form):
    date_recieved = forms.DateField(label=" Inspection completed on", widget=forms.SelectDateWidget(years=range(2016, 2024)))
    inspection_expiry_date = forms.DateField(label="Inspection invalid after", widget=forms.SelectDateWidget(years=range(2016, 2030)))
    ventilation = forms.IntegerField(label="Ventillation score:", required=True, min_value=0.0)
    cleanliness = forms.IntegerField(label="Cleanliness score", required=True, min_value=0.0)
    warehouseid = forms.ChoiceField(label="warehouse ID:", required=True)
    inspector_id = forms.ChoiceField(label="Inspector ID:", required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        q1 = """SELECT warehouseid
                  FROM warehouse;"""
        with connection.cursor() as cursor:
            cursor.execute(q1)
            rows = cursor.fetchall()
        warehouses = [('', ' ')] + [(row[0], row[0]) for row in rows]
        self.fields['warehouseid'].choices = warehouses

        q2= """SELECT IspecialistID
                  FROM inspector;"""
        with connection.cursor() as cursor:
            cursor.execute(q2)
            rows = cursor.fetchall()
        inspectors = [('', ' ')] + [(row[0], row[0]) for row in rows]
        self.fields['inspector_id'].choices = inspectors