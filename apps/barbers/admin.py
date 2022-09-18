from django.contrib import admin
from .models import Barber, Schedule, Service, Price, WorkingSchedule

class BarberAdmin(admin.ModelAdmin):
    list_display = ['user', 'saloon']

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['date', 'time']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service', 'description']

class PriceAdmin(admin.ModelAdmin):
    list_display = ['value', 'service']

admin.site.register(Barber, BarberAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(WorkingSchedule)

