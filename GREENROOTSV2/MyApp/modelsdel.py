from django.db import models
from MyApp.modelsgrad import Inspector,HarvestedProduce,NutritionSpecialist


class Warehouse(models.Model):
    warehouseid = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=155)

    def __str__(self):
        return str (self.warehouseid)
    
class Retailer(models.Model):
    name = models.CharField(max_length=65, primary_key=True)
    acceptedgrade = models.CharField(max_length=1)

    def __str__(self):
        return self.name

class WarehouseDistribution(models.Model):
    warehouseid = models.ForeignKey(Warehouse, on_delete=models.CASCADE,null=True)
    retailername = models.ForeignKey(Retailer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Distribution from {self.warehouseid} to  {self.retailername}"
    
    class Meta:
        unique_together = ['warehouseid', 'retailername'] 

class WarehouseCert(models.Model):
    date_received = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    name_of_certification = models.CharField(max_length=55)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name_of_certification} ({self.date_received})"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name_of_certification', 'date_received'], name='unique_certification_date')
        ]


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    registration_plate_no = models.CharField(max_length=15, unique=True)
    model = models.CharField(max_length=100)
    max_capacity = models.FloatField()
    gps_tracking_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Plate Num: {self.registration_plate_no} - {self.model} (Capacity: {self.max_capacity}kg)"


class LogisticsCompany(models.Model):
    company_name = models.CharField(max_length=255,primary_key=True)
    road = models.CharField(max_length=25)
    area = models.CharField(max_length=55)

    def __str__(self):
        return f"{self.company_name} - {self.road}, {self.area}"
    
class logistics(models.Model):
    company = models.ForeignKey(LogisticsCompany, on_delete=models.CASCADE)
    vehicle_Num = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.company} provided Vehicle No. {self.vehicle_num}"


class PackingFacility(models.Model):
    facID = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    street = models.CharField(max_length=50)
    area = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} located at {self.street}, {self.area} (Capacity: {self.capacity})"

class FacilityCertification(models.Model):
    certification_id = models.AutoField(primary_key=True)
    certification_name = models.CharField(max_length=255)
    expiry_date = models.DateField()
    facility = models.ForeignKey(PackingFacility, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('certification_name', 'facility','expiry_date') 
    
    def __str__(self):
        return f"Certification: {self.certification_name} (Expires: {self.expiry_date})"

class DeliveryHarvested(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    transport_date = models.DateField()
    quantity = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    cost = models.FloatField()
    facility = models.ForeignKey(PackingFacility, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    batch = models.ForeignKey(HarvestedProduce, on_delete=models.CASCADE)

    def __str__(self):
        return f"Delivery {self.delivery_id} - {self.quantity} units at ${self.cost:.2f} (Transport Date: {self.transport_date})"   
    
class PackedProduce(models.Model):
    barcode = models.CharField(max_length=50, unique=True, primary_key=True)
    weight = models.FloatField()
    material = models.CharField(max_length=100)
    cost_per_unit = models.FloatField()
    #source =  models.ForeignKey(PackingFacility, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.barcode}"
    
    

class DeliveryofPacked(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    transport_date = models.DateField()
    quantity = models.FloatField()
    temperature = models.FloatField()
    cost = models.FloatField()
    warehouseid = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    vehicleid = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    barcode = models.ForeignKey('PackedProduce', on_delete=models.CASCADE)

    def __str__(self):
        return f"Delivery {self.delivery_id} - {self.quantity} units at ${self.cost:.2f} from {self.warehouse} by {self.vehicle}"    
    
class NutritionContentReport(models.Model):
    fat_content = models.FloatField()
    sugar_content = models.FloatField()
    vitamin_content = models.FloatField()
    mineral_content = models.FloatField()
    nutritionist_id = models.ForeignKey(NutritionSpecialist, on_delete=models.CASCADE)
    barcode = models.ForeignKey(PackedProduce, on_delete=models.CASCADE)

    def __str__(self):
        return (f"NutritionContentReport(Nutritionist={self.nutritionist_id.name}, "
                f"Barcode={self.barcode.product_name}, fat={self.fat_content}%, "
                f"sugar={self.sugar_content}%, vitamin={self.vitamin_content}%, "
                f"mineral={self.mineral_content}%)")
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nutritionist_id', 'barcode'], name='unique_nutritionist_barcode')
        ]

class InspectionReport(models.Model):
    date_received = models.DateField()
    date_expired = models.DateField()
    ventilation = models.CharField(max_length=55)
    cleanliness = models.CharField(max_length=55)
    inspector_id = models.ForeignKey(Inspector, on_delete=models.CASCADE)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return (f"InspectionReport(Inspector={self.inspector_id.name}, "
                f"Vehicle={self.vehicle_id.make} {self.vehicle_id.model}, "
                f"Date Received={self.date_received}, Date Expired={self.date_expired})")
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['inspector_id', 'vehicle_id', 'date_received'], name='unique_inspector_vehicle_date')
        ]