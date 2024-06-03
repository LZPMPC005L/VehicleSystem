import re

from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Owner, Vehicle, LicensePlateRecognitionRecord
from django.shortcuts import render
from datetime import datetime

#register_owner
def register_owner(request):

    if request.method == 'POST':
        owner_id = request.POST.get('owner_id')
        owner_name = request.POST.get('owner_name')
        owner_email = request.POST.get('owner_email')

        if not all([owner_id, owner_name, owner_email]):
            return HttpResponse('Necessary information is missing', status=400)

        owner = Owner(
            owner_id = owner_id,
            owner_name = owner_name,
            owner_email = owner_email
        )

        try:
            owner.full_clean()
        except ValidationError as e:
            return HttpResponse('ID repeated', status=400)

        owner.save()
        return HttpResponse('Owner registered successfully', status=201)
    else:
        return render(request,'register_owner.html')


#register_vehicle
def register_vehicle(request):

    if request.method == 'POST':
        license_plate = request.POST.get('license_plate')
        vehicle_type = request.POST.get('vehicle_type')
        owner_id = request.POST.get('owner_id')
        registration_date = request.POST.get('registration_date')

        if not all([license_plate, vehicle_type, owner_id, registration_date]):
            return HttpResponse('Necessary information is missing', status=400)

        if Vehicle.objects.filter(license_plate=license_plate).exists():
            return HttpResponse('License plate already existed', status=400)

        try:
            owner = Owner.objects.get(pk=owner_id)
        except Owner.DoesNotExist:
            return HttpResponse('Owner_id does not exist', status=400)

        vehicle = Vehicle(
            license_plate = license_plate,
            vehicle_type = vehicle_type,
            owner_id = owner,
            registration_date = registration_date
        )

        try:
            vehicle.full_clean()
        except ValidationError as e:
            print(e)
            return HttpResponse('Validation error', status=400)

        vehicle.save()
        return HttpResponse('Vehicle registered successfully', status=201)
    else:
        return render(request,'register_vehicle.html')


def check_license_plate_in_system(license_plate):
    #inquery Django ORM to find license_plate
    #result = LicensePlateRecognitionRecord.objects.filter(license_plate=license_plate)
    result = Vehicle.objects.filter(license_plate=license_plate)


    #if existed,True; else return False
    return result.first() if result.exists() else None

#Recognition and record
def license_plate_recognition_record(request):

        if request.method == 'POST':
            license_plate = request.POST.get('license_plate')
            junction = request.POST.get('junction')
            record_date_string = request.POST.get('record_date')
            record_time_string = request.POST.get('record_time')


            #convert date string to a date object
            record_date = datetime.strptime(record_date_string, '%Y-%m-%d').date()

            #convert time string to a date object
            record_time = datetime.strptime(record_time_string, '%H:%M').time()

            if not all([license_plate, junction, record_date, record_time]):
                return HttpResponse('Necessary information is missing', status=400)

            #get the license_plate
            license_plate_exists = check_license_plate_in_system(license_plate)

            #set is_in_system based on whether the license plate exists
            is_in_system = 'Yes' if license_plate_exists else 'No'

            # Create a new record and save it to the database
            new_record = LicensePlateRecognitionRecord(
                    license_plate = license_plate,
                    junction = junction,
                    record_date = record_date,
                    record_time = record_time,
                    is_in_system= is_in_system,
            )
            new_record.save()

            if license_plate_exists:
                message = f'The license plate is in the system. Record: {new_record}'
            else:
                message = 'The license plate is not in the system. A new license record has been created.'

            return HttpResponse(message, status=200)
        else:
            return render(request, 'recognition_record.html')

