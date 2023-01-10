from datetime import timedelta, date, datetime
from django.utils import timezone
from apps.barbers.models import Schedule, Barber, WorkingSchedule
from apps.users.models import User
from django_tenants.utils import tenant_context, get_tenant_model


def clean_schedule():
    """Deletes schedules from past dates from the database"""
    schedules = Schedule.objects.all()

    for tenant in get_tenant_model().objects.all():
        with tenant_context(tenant):
            for schedule in schedules:
                if schedule.date < datetime.now().date():
                    schedule.delete()
                elif schedule.date == datetime.now().date():
                    if schedule.time < datetime.now().time():
                        schedule.delete()

def add_schedule():
    """Add 1 day of Schedule after 14 days to all barbers (every day at 00:00)"""
    barbers = Barber.objects.all()

    for tenant in get_tenant_model().objects.all():
        with tenant_context(tenant):
            # Figure out what weekday is the day after 14 days
            day = datetime.now().date() + timedelta(days=14)
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
    