# Generated by Django 5.1.3 on 2024-11-30 14:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0003_logisticscompany_packedproduce_vehicle_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackingFacility',
            fields=[
                ('facID', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
                ('street', models.CharField(max_length=50)),
                ('area', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FacilityCertification',
            fields=[
                ('certification_id', models.AutoField(primary_key=True, serialize=False)),
                ('certification_name', models.CharField(max_length=255)),
                ('expiry_date', models.DateField()),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyApp.packingfacility')),
            ],
            options={
                'unique_together': {('certification_name', 'facility', 'expiry_date')},
            },
        ),
    ]
