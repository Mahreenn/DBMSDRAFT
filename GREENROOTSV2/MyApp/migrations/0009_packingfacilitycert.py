# Generated by Django 5.1.3 on 2024-12-02 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0008_alter_warehouse_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackingFacilityCert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('certificateName', models.CharField(max_length=55)),
                ('date_received', models.DateField()),
                ('facilityID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyApp.packingfacility')),
                ('specialistID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyApp.governmentspecialist')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('certificateName', 'facilityID', 'date_received'), name='unique_certificate')],
            },
        ),
    ]
