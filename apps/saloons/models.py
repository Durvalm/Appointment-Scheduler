from django.db import models

class Saloon(models.Model):
    """Model that takes care of each saloon/franchise"""

    name = models.CharField(max_length=50)
    # - Transactions (Add later)
    
    # Fields related to location
    location = models.CharField(max_length=255)  # Geolocation (Implement later)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name
