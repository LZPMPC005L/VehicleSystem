from django.db import models
from datetime import date

#Owner registration information
class Owner(models.Model):
    owner_id = models.CharField(max_length=10, primary_key=True, unique=True)
    owner_name = models.CharField(max_length=50)
    owner_email = models.EmailField(max_length=50)

    def __str__(self):
        return self.owner_name


#Vehicle registration information
class Vehicle(models.Model):
    CAR = 'Car'
    ELECTROMOBILE = 'Electromobile'
    MOTORCYCLE = 'Motorcycle'
    BUS = 'Bus'
    OTHER = 'Other'

    VEHICLE_TYPE_CHOICES = [
        (CAR, 'Car'),
        (ELECTROMOBILE, 'Electromobile'),
        (MOTORCYCLE, 'Motorcycle'),
        (BUS, 'Bus'),
        (OTHER, 'Other'),
    ]

    license_plate = models.CharField(max_length=10, primary_key=True, unique=True)
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPE_CHOICES)
    owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE)
    registration_date = models.DateField()

    def __str__(self):
        return self.license_plate


#Recognizing and logging information
class LicensePlateRecognitionRecord(models.Model):
    license_plate = models.CharField(max_length=10)
    junction = models.CharField(max_length=100)
    record_date = models.DateField(default=date.today)
    record_time = models.TimeField()

    YES = 'Yes'
    No = 'No'

    IS_IN_SYSTEM_CHOICES = [
        (YES, 'Yes'),
        (No, 'No'),
    ]
    is_in_system = models.CharField(max_length=3, choices=IS_IN_SYSTEM_CHOICES, default=No)


    def __str__(self):
        return self.license_plate