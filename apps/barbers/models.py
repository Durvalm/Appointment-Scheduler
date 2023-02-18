from datetime import time, datetime
from django.db.models import Sum
from django.db import models
from apps.users.models import User
from apps.saloons.models import Saloon, Appointment

class Barber(models.Model):
    """Model for barbers who work in the saloons"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE, null=True)
    schedule = models.ManyToManyField('Schedule', blank=True)
    service = models.ManyToManyField('Service', blank=True)
    price = models.ManyToManyField('Price', blank=True)
    photo = models.ImageField(upload_to='barbers', blank=True)

    def __str__(self):
        return self.user.username

    def sales(self):
        """Returns how many sales the barber performed"""
        appointments = Appointment.objects.filter(barber=self)
        count = appointments.count()
        return count
    
    def sold(self):
        """Returns how much dollars barber has made"""
        appointments = Appointment.objects.filter(barber=self)
        income_dict = appointments.aggregate(Sum('total'))
        income = income_dict['total__sum']
        if not income:
            income = 0
        return round(income, 2)


class Schedule(models.Model):
    """Schedule should store all the hours the business operates."""
    date = models.DateField(auto_now=False, blank=True, null=True)
    time = models.TimeField(auto_now=False, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date', '-time')
        unique_together = ('date', 'time')

    def __str__(self):
        return f'{self.date} {self.time}'
   

class Service(models.Model):
    """Stores all the services the business provides"""
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Price(models.Model):
    """Stores prices for every service"""
    value = models.FloatField(null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service')

    def __str__(self):
        return str(self.value)


DAYS = [
    (0, ("Monday")),
    (1, ("Tuesday")),
    (2, ("Wednesday")),
    (3, ("Thursday")),
    (4, ("Friday")),
    (5, ("Saturday")),
    (6, ("Sunday")),
] 

HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]
class WorkingSchedule(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-from_hour')
        unique_together = ('barber', 'day')

    def __str__(self):
        return self.get_day_display()

    def get_all_hours(self, instance):
        """Gets all hours in range (from_hour:to_hour) in determined day"""
        # Transform string hours in datetime (AM, PM)
        from_hour = datetime.strptime(instance.from_hour, '%I:%M %p')
        to_hour = datetime.strptime(instance.to_hour, '%I:%M %p')

        # Converts from_hour to time object
        start = datetime.time(from_hour)
        end = datetime.time(to_hour) 
        TIME_FORMAT = "%H:%M" # Format for hours and minutes
        times = [] # List of times 
        while start <= end:
            times.append(start)
            # If minute is 0, set it to 30
            if start.minute == 0: 
                start = start.replace(minute=30) 
            # if minute is 30, set it to 0 and pass to next hout
            elif start.minute == 30:
                start = start.replace(minute=0) 
                if start.hour != 23:
                    start = start.replace(hour=start.hour + 1)
                else:
                    start = start.replace(hour=0)

            # Break if all hours have been found
            is_equal = start == end
            if is_equal is True:
                times.append(start)
                break
        # Uses list comprehension to format the objects and return list
        times = [x.strftime(TIME_FORMAT) for x in times] 
        return times


