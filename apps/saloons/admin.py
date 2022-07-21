from django.contrib import admin
from .models import Saloon, Review, Appointment
# Register your models here.

admin.site.register(Saloon)
admin.site.register(Review)
admin.site.register(Appointment)