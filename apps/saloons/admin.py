from django.contrib import admin
from .models import Saloon, Review, Appointment


class SaloonAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'city']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'saloon', 'rating', 'created_at']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'schedule', 'total', 'service', 'saloon', 'barber', 'created_at']


admin.site.register(Saloon, SaloonAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Appointment, AppointmentAdmin)