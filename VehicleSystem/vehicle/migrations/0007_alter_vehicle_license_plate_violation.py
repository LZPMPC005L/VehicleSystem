# Generated by Django 5.0.1 on 2024-06-07 13:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vehicle", "0006_alter_licenseplaterecognitionrecord_junction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="license_plate",
            field=models.CharField(
                max_length=100, primary_key=True, serialize=False, unique=True
            ),
        ),
        migrations.CreateModel(
            name="Violation",
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
                    "violation_type",
                    models.CharField(
                        choices=[
                            ("Speeding", "Speeding"),
                            ("Drunk Driving", "Drunk Driving"),
                            ("Red Light", "Red Light"),
                            ("Illegal Parking", "Illegal Parking"),
                            ("Vehicle non-compliance", "Vehicle non-compliance"),
                            ("No seat belt", "No seat belt"),
                            ("Other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                ("fine", models.DecimalField(decimal_places=2, max_digits=10)),
                ("violation_license_plate", models.CharField(max_length=100)),
                ("violation_date", models.DateField(null=True)),
                ("violation_time", models.TimeField(null=True)),
                ("violation_junction", models.CharField(max_length=100, null=True)),
                (
                    "record",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vehicle.licenseplaterecognitionrecord",
                    ),
                ),
            ],
        ),
    ]
