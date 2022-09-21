from django.urls import path
from .views.dashboard import (employee_dashboard, complete_appointment, 
                              pay_appointment, add_appointment)
from .views.schedule import (delete_all_schedule_hours, schedule, default_schedule, add_default_schedule, 
                             delete_default_schedule, edit_schedule, delete_schedule_hour,
                             add_schedule_hour, delete_all_schedule_hours)

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
]