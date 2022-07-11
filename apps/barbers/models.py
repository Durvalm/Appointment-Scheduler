from django.db import models
from apps.users.models import User
from apps.saloons.models import Saloon

class Barber(models.Model):
    """Model for barbers who work in the saloons"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saloon = models.ForeignKey(Saloon, on_delete=models.CASCADE, null=True)
    # Schedule (Add later)

    def __str__(self):
        return self.user.username
