from django import forms
from django.forms import ModelForm
from .modelsdel import DeliveryofPacked

class delPForm(ModelForm):
    class Meta:
        model = DeliveryofPacked
        fields = "__all__"             #('transport_date','temperature','cost','quantity','barcode', 'warehouseid','vehicleid')  

