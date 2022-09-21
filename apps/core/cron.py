from datetime import timedelta, date
from django.utils import timezone
from apps.barbers.models import Schedule, Barber, WorkingSchedule

def clean_schedule():
    """Deletes schedules from past dates from the database"""
    schedules = Schedule.objects.all()

    for schedule in schedules:
        if schedule.date < timezone.now().date():
            schedule.delete()
        elif schedule.date == timezone.now().date():
            if schedule.time < timezone.now().time():
                schedule.delete()

def add_schedule():
    """Add 1 day of Schedule after 14 days to all barbers (every day at 00:00)"""
    barbers = Barber.objects.all()

    # Figure out what weekday is the day after 14 days
    day = timezone.now().date() + timedelta(days=14)
    weekday = day.weekday()

    # Iterate through all barbers
    for barber in barbers:
        # Get WorkingSchedule for weekday after 14 days
        try:
            working_schedule = WorkingSchedule.objects.get(barber=barber, day=weekday)
        except:
            continue
        
        # If barber works in weekday Get all hours in the created working_schedule
        hour_lst = working_schedule.get_all_hours(working_schedule)

        # Add hours from hour_list to new schedules after 14 days
        for hour in hour_lst:
            schedule, created = Schedule.objects.get_or_create(date=day, time=hour, is_available=True)
            barber.schedule.add(schedule)
