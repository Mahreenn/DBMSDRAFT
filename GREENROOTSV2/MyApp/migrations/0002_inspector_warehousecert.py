# Generated by Django 5.1.3 on 2024-11-30 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("MyApp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Inspector",
            fields=[
                (
                    "IspecialistID",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WarehouseCert",
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
                ("date_received", models.DateField(blank=True, null=True)),
                ("expiry_date", models.DateField(blank=True, null=True)),
                ("name_of_certification", models.CharField(max_length=55)),
                (
                    "inspector",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MyApp.inspector",
                    ),
                ),
                (
                    "warehouse",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="MyApp.warehouse",
                    ),
                ),
            ],
            options={
                "constraints": [
                    models.UniqueConstraint(
                        fields=("name_of_certification", "date_received"),
                        name="unique_certification_date",
                    )
                ],
            },
        ),
    ]
