from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import WorkingSchedule, Barber
from ..services import convert_weekday_to_number

def schedule(request):
    """Render schedule page"""
    # Filter barber's working schedule
    working_schedule = WorkingSchedule.objects.filter(barber=request.user.barber)
    # Get field choices from working_schedule fields
    days = WorkingSchedule.day.field.choices
    hours = WorkingSchedule.from_hour.field.choices

    # Add Schedules for next 14 days
    # try:
    #     schedule = Barber.objects.get(schedule=)

    context = {
        'days': days,
        'hours': hours,
        'working_schedule': working_schedule,
    }
    return render(request, 'barber/schedule.html', context)

def add_default_schedule(request):
    """Add barber's default working schedule to the database"""
    # Get barber input
    start_hour = request.POST['start_hour']
    end_hour = request.POST['end_hour']
    weekday = request.POST['day']

    # Convert alphabetical weekday to numerical weekday (Monday to 1) 
    day = convert_weekday_to_number(weekday)

    # If Barber input is wrong, raise error
    if day is None:
        messages.success(request, 'Day entered is not valid, enter one of the provided values')
        return redirect('schedule')

    # Add Schedule to database
    WorkingSchedule.objects.create(from_hour=start_hour, to_hour=end_hour, day=day, barber=request.user.barber)

    return redirect('schedule')

def delete_default_schedule(request, id):
    """Delete barber's default working schedule to the database"""
    # Get schedule's id, and delete it
    working_schedule = WorkingSchedule.objects.get(id=id)
    working_schedule.delete()
    return redirect('schedule')

