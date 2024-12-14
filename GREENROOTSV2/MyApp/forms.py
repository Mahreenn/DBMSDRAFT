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
    delivery_id = forms.IntegerField(label="Delivery ID", required=True)
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


    def clean_delivery_id(self):
        # Get the delivery_id entered by the user
        delivery_id = self.cleaned_data.get('delivery_id')

        # Query the database to check if the delivery_id already exists
        query = """SELECT id FROM warehouse_distribution WHERE id = %s"""
        with connection.cursor() as cursor:
            cursor.execute(query, [delivery_id])  # Use parameterized query to avoid SQL injection
            rows = cursor.fetchall()

  
        if rows:
            raise ValidationError(f"Delivery ID {delivery_id} already exists in the warehouse distribution.")

        return delivery_id
    
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