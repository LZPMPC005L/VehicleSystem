from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Owner, Vehicle, LicensePlateRecognitionRecord, Violation
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
import re
from decimal import Decimal
from django.core.mail import send_mail

#register_owner
def register_owner(request):
    if request.method == 'POST':
        owner_id = request.POST.get('owner_id')
        owner_name = request.POST.get('owner_name')
        owner_email = request.POST.get('owner_email')

        context = {
            'owner_id': owner_id,
            'owner_name': owner_name,
            'owner_email': owner_email,
        }

        if not all([owner_id, owner_name, owner_email]):
            messages.error(request, 'Necessary information is missing')
            return render(request, 'register_owner.html', context)

        owner = Owner(
            owner_id = owner_id,
            owner_name = owner_name,
            owner_email = owner_email
        )

        try:
            owner.full_clean()
        except ValidationError as e:
            messages.error(request,'ID repeated')
            return render(request, 'register_owner.html', context)

        owner.save()
        messages.success(request, 'Owner Registered successfully')
        return redirect('register_owner')
    else:
        return render(request,'register_owner.html')




#register_vehicle
def register_vehicle(request):

    if request.method == 'POST':
        license_plate = request.POST.get('license_plate')
        vehicle_type = request.POST.get('vehicle_type')
        owner_id = request.POST.get('owner_id')
        registration_date = request.POST.get('registration_date')

        context = {
            'license_plate': license_plate,
            'vehicle_type': vehicle_type,
            'owner_id': owner_id,
            'registration_date': registration_date,
        }

        if not all([license_plate, vehicle_type, owner_id, registration_date]):
            messages.error(request, 'Necessary information is missing')
            return render(request, 'register_vehicle.html', context)

        if Vehicle.objects.filter(license_plate=license_plate).exists():
            messages.error(request, 'License plate already existed')
            return render(request, 'register_vehicle.html', context)

        try:
            owner = Owner.objects.get(pk=owner_id)
        except Owner.DoesNotExist:
            messages.error(request, 'Owner_id does not exist')
            return render(request, 'register_vehicle.html', context)

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
            messages.error(request, 'Validation error' + str(e))
            return render(request, 'register_vehicle.html', context)

        vehicle.save()
        messages.success(request, 'Vehicle Registered successfully')
        return redirect('register_vehicle')
    else:
        return render(request,'register_vehicle.html')


def check_license_plate_in_system(license_plate):
    #inquery Django ORM to find license_plate
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
                messages.success(request, message)
            else:
                message = 'The license plate is not in the system. A new license record has been created.'
                messages.success(request, message)

            return render(request,'recognition_record.html')
        else:
            return render(request, 'recognition_record.html')


#create Violation record
def create_violation(request):
    records = LicensePlateRecognitionRecord.objects.all()

    violation_types = ['Speeding', 'Drunk Driving', 'Red Light', 'Illegal Pakring','Vehicle non-compliance', 'No seat belt', 'Other']

    if request.method == 'POST':
        print(request.POST)

        record_id = request.POST.get('record')
        violation_type = request.POST.get('violation_type')
        fine = request.POST.get('fine')

        #set context for continue
        context = {
            'records' : records,
            'record_selected': record_id,
            'violation_type_selected': violation_type,
            'fine': fine,
            'violation_types': violation_types
        }

        #check if the fields are not empty
        if not all([record_id, violation_type, fine]):
            messages.error(request,'Necessary information is missing')
            return render(request, 'create_violation.html',context)

        #check if fine is a valid number
        if not re.match(r"^\d+(\.\d{1,2})?$", fine):
            messages.error(request, 'Invalid fine format')
            return render(request, 'create_violation.html', context)

        #change string into decimal number
        try:
            fine = Decimal(fine)
        except (ValueError, TypeError):
            messages.error(request, 'Invalid fine amount')
            return render(request, 'create_violation.html', context)

        #get the record in database by record_id
        try:
            record = LicensePlateRecognitionRecord.objects.get(pk=record_id)
        except LicensePlateRecognitionRecord.DoesNotExist:
            messages.error(request,'Record does not exist')
            return render(request, 'create_violation.html', context)

        #create new violation record
        new_violation = Violation(
            record = record,
            violation_type = violation_type,
            fine = fine,
            violation_license_plate = record.license_plate,
            violation_date = record.record_date,
            violation_time = record.record_time,
            violation_junction = record.junction,
        )

        new_violation.save()

        messages.success(request, f'Violation for license plate {record.license_plate} has been recorded.')

        #after creating violation record, check whether license_plate is in the system, if so, send email immediately
        if send_violation_email(new_violation):
            messages.success(request, 'Violation email sent successfully.')
        else:
            messages.warning(request, 'This vehicle is not in the system, violation email could not be sent.')

        return render(request, 'create_violation.html',)
    else:
        context = {'records': records, 'violation_types': violation_types}
        return render(request, 'create_violation.html',{'records': records})


#send_violation_email
def send_violation_email(violation):
    try:
        vehicle = Vehicle.objects.get(license_plate=violation.violation_license_plate)
        owner_email = vehicle.owner_id.owner_email
    except Vehicle.DoesNotExist:
        return False

    subject = 'Traffic Violation Notice'
    message = (
        f'Your vehicle with {violation.violation_license_plate} has been recorded for '
        f'{violation.violation_type} on {violation.violation_date} at {violation.violation_time} '
        f' near {violation.violation_junction}. The fine is ${violation.fine}.'
    )
    from_email = 'checke006@gmail.com'
    recipient_list = [owner_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return True

