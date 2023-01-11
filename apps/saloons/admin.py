from django.contrib import admin
from .models import Saloon, Appointment


class SaloonAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'city']


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'schedule', 'total', 'service', 'saloon', 'barber', 'created_at']


admin.site.register(Saloon, SaloonAdmin)
admin.site.register(Appointment, AppointmentAdmin)