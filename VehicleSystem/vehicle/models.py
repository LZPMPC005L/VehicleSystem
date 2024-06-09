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

    license_plate = models.CharField(max_length=100, primary_key=True, unique=True)
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


#Traffic violation
class Violation(models.Model):
    SPEEDING = 'Speeding'
    DRUNK_DRIVING = 'Drunk Driving'
    RED_LIGHT = 'Red Light'
    ILLEGAL_PARKING = 'Illegal Parking'
    VEHICLE_NON_COMPLIANCE = 'Vehicle non-compliance'
    NO_SEAT_BELT = 'No seat belt'
    OTHER = 'Other'

    VIOLATION_TYPE_CHOICES = [
        (SPEEDING, 'Speeding'),
        (DRUNK_DRIVING, 'Drunk Driving'),
        (RED_LIGHT, 'Red Light'),
        (ILLEGAL_PARKING, 'Illegal Parking'),
        (VEHICLE_NON_COMPLIANCE, 'Vehicle non-compliance'),
        (NO_SEAT_BELT, 'No seat belt'),
        (OTHER, 'Other'),
    ]

    record = models.ForeignKey(LicensePlateRecognitionRecord, on_delete=models.CASCADE)
    violation_type = models.CharField(max_length=50, choices=VIOLATION_TYPE_CHOICES)
    fine = models.DecimalField(max_digits=10, decimal_places=2)
    violation_license_plate = models.CharField(max_length=100)
    violation_date = models.DateField(null = True)
    violation_time = models.TimeField(null=True)
    violation_junction = models.CharField(max_length=100, null = True)

    def save(self, *args, **kwargs):
        if not self.violation_license_plate or not self.violation_date or not self.violation_time or not self.violation_junction:
            self.violation_license_plate = self.record.license_plate
            self.violation_date = self.record.record_date
            self.violation_time = self.record.record_time
            self.violation_junction = self.record.junction
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.violation_license_plate} - {self.violation_type}"

