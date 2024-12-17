from django import forms
from django.forms import ModelForm
from .modelsdel import DeliveryofPacked
from django.db import connection
from django.core.exceptions import ValidationError


class delPForm(ModelForm):
    class Meta:
        model = DeliveryofPacked
        fields = "__all__"             #('transport_date','temperature','cost','quantity','barcode', 'warehouseid','vehicleid')  

class distribForm(forms.Form):
    #delivery_id = forms.IntegerField(label="Delivery ID", required=True)
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

    
class productVisualForm(forms.Form):
    Barcode = forms.ChoiceField(label="Barcode", required=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   

        query = """SELECT barcode
                  FROM packed_produce;"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        Barcode_choices = [('', 'Choose a product Barcode:')] + [(row[0], row[0]) for row in rows]

        self.fields['Barcode'].choices = Barcode_choices
        

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
    vehicle_id = forms.ChoiceField(label="Vehicle ID:", required=True)
    inspector_id = forms.ChoiceField(label="Inspector ID:", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        query = """SELECT vehicle_id
                  FROM vehicle;"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        vehicles = [('', 'Vehicle ID:')] + [(row[0], row[0]) for row in rows]
        self.fields['vehicle_id'].choices = vehicles

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        query = """SELECT IspecialistID
                  FROM inspector;"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        inspectors = [('', 'Vehicle ID:')] + [(row[0], row[0]) for row in rows]
        self.fields['inspector_id'].choices = inspectors