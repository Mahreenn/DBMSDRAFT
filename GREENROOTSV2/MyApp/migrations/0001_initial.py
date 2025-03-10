# Generated by Django 5.1.3 on 2024-11-30 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("product_ID", models.AutoField(primary_key=True, serialize=False)),
                ("product_Name", models.CharField(max_length=55)),
                ("product_Type", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Retailer",
            fields=[
                (
                    "name",
                    models.CharField(max_length=65, primary_key=True, serialize=False),
                ),
                ("acceptedgrade", models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name="Warehouse",
            fields=[
                ("warehouseid", models.IntegerField(primary_key=True, serialize=False)),
                ("address", models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name="WarehouseDistribution",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "retailername",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MyApp.retailer",
                    ),
                ),
                (
                    "warehouseid",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MyApp.warehouse",
                    ),
                ),
            ],
            options={
                "unique_together": {("warehouseid", "retailername")},
            },
        ),
    ]
