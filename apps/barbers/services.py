from django.shortcuts import redirect
from apps.saloons.models import Appointment

def change_status(id, status):
    """Changes is_completed and is_paid status of appointments"""
    appointment = Appointment.objects.get(id=id)

    # 'status' will be passed when function is called as (is_completed) or (is_paid)
    if status == 'is_completed':
        if appointment.is_completed:
            appointment.is_completed = False
        else:
            appointment.is_completed = True

    elif status == 'is_paid':
        if appointment.is_paid:
            appointment.is_paid = False
        else:
            appointment.is_paid = True

    appointment.save()

def convert_weekday_to_number(weekday):
    """Convert weekday ex: 'tuesday' to number '3' """
    num_day = ''
    if weekday == 'Monday':
        num_day = 1
    elif weekday == 'Tuesday':
        num_day = 2
    elif weekday == 'Wednesday':
        num_day = 3
    elif weekday == 'Thursday':
        num_day = 4
    elif weekday == 'Friday':
        num_day = 5
    elif weekday == 'Saturday':
        num_day = 6
    elif weekday == 'Sunday':
        num_day = 7
    else:
        num_day = None
    return num_day
        
        