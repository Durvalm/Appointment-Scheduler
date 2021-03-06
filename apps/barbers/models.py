from django.db import models
from apps.users.models import User
from apps.saloons.models import Saloon

class Barber(models.Model):
    """Model for barbers who work in the saloons"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE, null=True)
    schedule = models.ManyToManyField('Schedule', blank=True)
    service = models.ManyToManyField('Service', blank=True)
    price = models.ManyToManyField('Price', blank=True)

    def __str__(self):
        return self.user.full_name()


class Schedule(models.Model):
    """Schedule should store all the hours the business operates."""
    date = models.DateField(auto_now=False, blank=True, null=True)
    time = models.TimeField(auto_now=False, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.date} {self.time}'


class Service(models.Model):
    """Stores all the services the business provides"""
    service = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.service

class Price(models.Model):
    """Stores prices for every service"""
    value = models.FloatField(null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.value)