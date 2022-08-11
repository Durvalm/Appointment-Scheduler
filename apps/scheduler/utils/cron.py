from django.utils import timezone
from apps.barbers.models import Schedule

def clean_schedule():
    """Deletes schedules from past dates from the database"""
    schedules = Schedule.objects.all()

    for schedule in schedules:
        if schedule.date < timezone.now().date():
            schedule.delete()
        elif schedule.date == timezone.now().date():
            if schedule.time < timezone.now().time():
                schedule.delete()
