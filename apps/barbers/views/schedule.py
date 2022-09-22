from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
from ..models import WorkingSchedule, Schedule
from ..services import (convert_weekday_to_number, add_delete_barber_schedules, display_pretty_datetime,
                        get_all_schedules, get_all_hours)

def schedule(request):
    """Render schedule page"""
    # Get dictionary of schedule's date and id 
    schedules = get_all_schedules(request)

    context = {
        'schedules': schedules,
    }
    return render(request, 'barber/schedule.html', context)

def edit_schedule(request, id):
    """Edit current schedule for barber"""

    # Get schedule to retrieve its date
    schedule = Schedule.objects.get(id=id)
    # Get date from schedule
    cache.set('date', schedule.date)
    # Get field choices from working_schedule fields
    hours = WorkingSchedule.from_hour.field.choices

    # Use schedule's date above to retrieve all hours in this date
    all_schedules_in_date = Schedule.objects.filter(barber=request.user.barber, date=schedule.date).order_by('time')
    # Create dictionary of schedule hours and Id's using above queryset
    hour_dict = get_all_hours(all_schedules_in_date)

    # Get pretty version of date
    date = display_pretty_datetime(schedule.__str__())
    # Get weekday of date
    weekday = schedule.date.strftime('%A')
    
    context = {
        'schedules': hour_dict,
        'date': date,
        'weekday': weekday,
        'hours': hours,
    }
    return render(request, 'barber/edit-schedule.html', context)

def delete_schedule_hour(request, id):
    """Delete single hour from certain schedule's day"""
    schedule = Schedule.objects.get(id=id)
    
    # store schedule date
    schedule_date = schedule.date

    # Delete schedule
    request.user.barber.schedule.remove(schedule)

    # Get new schedule to get redirect id
    new_schedule = Schedule.objects.filter(date=schedule_date, barber=request.user.barber).first()

    return redirect('edit-schedule', id=new_schedule.id)

def add_schedule_hour(request):
    """Add single hour from certain schedule's day"""
    # Get hour and Date
    hour = request.POST['hour']
    date = cache.get('date')

    hour = datetime.strptime(hour, '%I:%M %p')

    # Create schedule and add it to barber's schedule
    schedule = Schedule.objects.create(time=hour, date=date)
    request.user.barber.schedule.add(schedule)

    return redirect('edit-schedule', id=schedule.id)

def delete_all_schedule_hours(request):
    """Delete all hours in determined schedule's day"""
    date = cache.get('date')

    # Remove all schedules in determined date from barber
    schedules = Schedule.objects.filter(barber=request.user.barber, date=date) 
    for schedule in schedules:
        request.user.barber.schedule.remove(schedule)

    return redirect('schedule')

def default_schedule(request):
    """Render default schedule page"""
    # Filter barber's working schedule
    working_schedule = WorkingSchedule.objects.filter(barber=request.user.barber)

    # Get field choices from working_schedule fields
    days = WorkingSchedule.day.field.choices
    hours = WorkingSchedule.from_hour.field.choices

    context = {
        'days': days,
        'hours': hours,
        'working_schedule': working_schedule,
    }
    return render(request, 'barber/default-schedule.html', context)


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
        return redirect('default-schedule')

    # Check if weekday's schedule exists
    weekday_exists = WorkingSchedule.objects.filter(barber=request.user.barber, day=day).exists()
    if weekday_exists:
        messages.warning(request, 'Weekday already exists! If you want to change schedule, remove existing weekday and add again.')
        return redirect('default-schedule')

    # Create WorkingSchedule if it doesn't exist
    working_schedule = WorkingSchedule.objects.create(from_hour=start_hour, to_hour=end_hour, day=day, barber=request.user.barber)

    # Add Schedules to barber
    add_delete_barber_schedules(request, working_schedule, 'add')

    return redirect('default-schedule')

def delete_default_schedule(request, id):
    """Delete barber's default working schedule to the database"""
    # Get WorkingSchedule's id, and delete it
    working_schedule = WorkingSchedule.objects.get(id=id)

    # Delete related schedules to barber
    add_delete_barber_schedules(request, working_schedule, 'delete')

    # Delete working schedule from the DB
    working_schedule.delete()

    return redirect('default-schedule')

