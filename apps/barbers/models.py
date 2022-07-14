from django.db import models
from apps.users.models import User
from apps.saloons.models import Saloon

class Barber(models.Model):
    """Model for barbers who work in the saloons"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE, null=True)
    schedule = models.ManyToManyField('Schedule', blank=True)
    service = models.ManyToManyField('Service', blank=True)

    def __str__(self):
        return self.user.username


class Schedule(models.Model):
    """Schedule should store all the hours the business operates."""
    time = models.DateTimeField(auto_now=False, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.time


class Service(models.Model):
    """Stores all the services the business provides"""
    service = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    price = models.FloatField(null=True)

    def __str__(self):
        return self.service