from django.urls import path
from .views.dashboard import (employee_dashboard, complete_appointment, 
                              pay_appointment, add_appointment)
from .views.schedule import (delete_all_schedule_hours, schedule, default_schedule, add_default_schedule, 
                             delete_default_schedule, edit_schedule, delete_schedule_hour,
                             add_schedule_hour, delete_all_schedule_hours)
from .views.settings import barber_settings, delete_service, manage_services, edit_service, delete_service, add_service

urlpatterns = [
    path('dashboard/', employee_dashboard, name='employee-dashboard'),
    path('add-appointment/', add_appointment, name='add-appointment'),
    path('complete-appointment/<int:id>/', complete_appointment, name='complete-appointment'),
    path('pay-appointment/<int:id>/', pay_appointment, name='pay-appointment'),

    path('schedule/', schedule, name='schedule'),
    path('edit-schedule/<int:id>/', edit_schedule, name='edit-schedule'),
    path('delete-schedule-hour/<int:id>/', delete_schedule_hour, name='delete-schedule-hour'),
    path('add-schedule-hour/', add_schedule_hour, name='add-schedule-hour'),
    path('delete-all-schedule-hours/', delete_all_schedule_hours, name='delete-all-schedule-hours'),

    path('default-schedule/', default_schedule, name='default-schedule'),
    path('add-default-schedule/', add_default_schedule, name='add-default-schedule'),
    path('delete-default-schedule/<int:id>/', delete_default_schedule, name='delete-default-schedule'),

    path('settings/', barber_settings, name='barber-settings'),
    path('manage-services/', manage_services, name='manage-services'),
    path('edit-service/<int:id>/', edit_service, name='edit-service'),
    path('delete-service/<int:id>/', delete_service, name='delete-service'),
    path('add-service/', add_service, name='add-service'),
]