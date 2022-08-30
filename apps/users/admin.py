from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'saloon', 'total_spent', 'is_admin', 'is_barber', 'date_joined', 'last_login')


admin.site.register(User, UserAdmin)