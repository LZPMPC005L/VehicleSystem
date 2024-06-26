# Generated by Django 5.0.1 on 2024-06-02 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LicensePlateRecognitionRecord",
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
                ("license_plate", models.CharField(max_length=10)),
                ("junction", models.CharField(max_length=10)),
                ("record_time", models.DateTimeField()),
                (
                    "is_in_system",
                    models.CharField(
                        choices=[("Yes", "Yes"), ("No", "No")],
                        default="No",
                        max_length=3,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Owner",
            fields=[
                (
                    "owner_id",
                    models.CharField(
                        max_length=10, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("owner_name", models.CharField(max_length=50)),
                ("owner_email", models.EmailField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                (
                    "license_plate",
                    models.CharField(
                        max_length=10, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "vehicle_type",
                    models.CharField(
                        choices=[
                            ("Car", "Car"),
                            ("Electromobile", "Electromobile"),
                            ("Motorcycle", "Motorcycle"),
                            ("Bus", "Bus"),
                            ("Other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                ("registration_date", models.DateTimeField()),
                (
                    "owner_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vehicle.owner"
                    ),
                ),
            ],
        ),
    ]
