from django.db import models

class Saloon(models.Model):
    """Model that takes care of each saloon/franchise"""

    name = models.CharField(max_length=50)
    # - Transactions (Add later)
    
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

