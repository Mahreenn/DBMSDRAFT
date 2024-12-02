from django.db import models
from django.apps import apps

class Product(models.Model):
    product_ID = models.AutoField(primary_key=True)
    product_Name = models.CharField(max_length=55)
    product_Type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.product_Name} ({self.product_Type})"
    
class GovernmentSpecialist(models.Model):
    specialist_id = models.AutoField(primary_key=True)
    designation = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.designation} (ID: {self.specialist_id})"
    
class Specialist_License(models.Model):
    specialist = models.ForeignKey(GovernmentSpecialist, on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=255)
    date_received = models.DateField()

    def __str__(self):
        return f"{self.degree_name} (Received: {self.date_received})"
    
class Inspector(models.Model):
    IspecialistID = models.IntegerField(primary_key=True)

class NutritionSpecialist(models.Model):
     NspecialistID = models.IntegerField(primary_key=True)
    
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
    #nutrionistID = models.ForeignKey(NutritionSpecialist, on_delete=models.CASCADE)
    #produceID = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Batch {self.batch_id} - {self.weight}kg, {self.colour}, {self.smoothness} (Sown: {self.sowing_date}, Harvested: {self.harvest_date})"

class Farm(models.Model):
    registration_id = models.CharField(max_length=100, primary_key=True)
    size = models.FloatField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"Farm({self.registration_id}, {self.size} acres, located at {self.address})"
    
class FarmProduction(models.Model):
    batchID = models.ForeignKey(HarvestedProduce, on_delete=models.CASCADE)
    registration_id = models.ForeignKey(Farm, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('batchID', 'registration_id')

    def __str__(self):
        return f"FarmProduction(batchID={self.batchID}, Farm={self.registration_id})"
    

