from django.db import models
from django.db.models import Avg, Count
from apps.users.models import User, Admin

class Saloon(models.Model):
    """Model that takes care of each saloon/franchise"""

    name = models.CharField(max_length=50)
    # Fields related to location
    street_number = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=100, blank=True)  
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def sliced_address(self):
        """This method returns address sliced so you can use for geolocation in google maps,
        always remember to divide address by spaces in the database"""
        sliced = self.address.split(' ')
        return sliced


class Appointment(models.Model):
    """Model that holds all of the appointments"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    schedule = models.DateTimeField(auto_now_add=False, blank=True)
    # Without taxes
    price = models.FloatField(null=True, blank=True)
    # With taxes
    total = models.FloatField(null=True, blank=True)

    service = models.ForeignKey('barbers.Service', on_delete=models.CASCADE)
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    barber = models.ForeignKey('barbers.Barber', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)


    def __str__(self):
        return self.saloon.city