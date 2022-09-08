from django.urls import path
from .views.dashboard import employee_dashboard, complete_appointment, pay_appointment, add_appointment

urlpatterns = [
    path('dashboard/', employee_dashboard, name='employee-dashboard'),
    path('add-appointment/', add_appointment, name='add-appointment'),
    path('complete-appointment/<int:id>/', complete_appointment, name='complete-appointment'),
    path('pay-appointment/<int:id>/', pay_appointment, name='pay-appointment'),
]