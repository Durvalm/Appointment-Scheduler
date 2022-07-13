from django.contrib import admin
from .models import Barber, Schedule, Service

admin.site.register(Barber)
admin.site.register(Schedule)
admin.site.register(Service)
