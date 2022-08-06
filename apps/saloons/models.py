from django.db import models
from django.db.models import Avg, Count
from apps.users.models import User


class Saloon(models.Model):
    """Model that takes care of each saloon/franchise"""

    name = models.CharField(max_length=50)
    # Fields related to location
    street_number = models.CharField(max_length=10, blank=True)
    adress = models.CharField(max_length=100, blank=True)  
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def sliced_address(self):
        """This method returns address sliced so you can use for geolocation in google maps,
        always remember to divide address by spaces in the database"""
        sliced = self.adress.split(' ')
        return sliced
    
    def average_review(self):
        """Computer the average review of each saloon"""
        reviews = Review.objects.filter(saloon=self).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return round(avg, 1)

    def review_count(self):
        """Compute how many reviews the saloon has"""
        reviews = Review.objects.filter(saloon=self).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class Review(models.Model):
    """Model that creates a review"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review[0:15]


class Appointment(models.Model):
    """Model that holds all of the appointments"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    schedule = models.ForeignKey('barbers.Schedule', on_delete=models.CASCADE)
    # Without taxes
    price = models.FloatField(null=True, blank=True)
    # With taxes
    total = models.FloatField(null=True, blank=True)
    service = models.ForeignKey('barbers.Service', on_delete=models.CASCADE)
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE)
    barber = models.ForeignKey('barbers.Barber', on_delete=models.CASCADE)

    def __str__(self):
        if self.user:
            return self.user.full_name()
        else:
            return self.saloon.city