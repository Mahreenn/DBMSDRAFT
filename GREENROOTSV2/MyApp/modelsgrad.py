from django.db import models
from django.apps import apps

class Product(models.Model):
    product_ID = models.AutoField(primary_key=True)
    product_Name = models.CharField(max_length=55)
    product_Type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.product_Name} ({self.product_Type})"
    
class Inspector(models.Model):
    IspecialistID = models.IntegerField(primary_key=True)



    
class HarvestedProduce(models.Model):
    batch_id = models.AutoField(primary_key=True)
    sowing_date = models.DateField()
    harvest_date = models.DateField()
    weight = models.FloatField()
    smoothness = models.CharField(max_length=50)
    colour = models.CharField(max_length=50)
    fungal_growth = models.BooleanField()
    weather_conditions = models.CharField(max_length=255)
    pesticides_used = models.BooleanField()

    def __str__(self):
        return f"Batch {self.batch_id} - {self.weight}kg, {self.colour}, {self.smoothness} (Sown: {self.sowing_date}, Harvested: {self.harvest_date})"