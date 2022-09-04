from django.urls import path
from .views.dashboard import dashboard, date_filter_dashboard, date_filter_graph
from .views.transactions import transactions
from .views.employees import employees, add_employee, edit_employee, delete_employee
from .views.settings import settings, edit_host_email

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('date-filter-dashboard/', date_filter_dashboard, name='date-filter-dashboard'),
    path('date-filter-graph/', date_filter_graph, name='date-filter-graph'),
    
    path('transactions/', transactions, name='transactions'),

    path('employees/', employees, name='employees'),
    path('add-employee/', add_employee, name='add-employee'),
    path('edit-employee/', edit_employee, name='edit-employee'),
    path('delete-employee/<int:id>/', delete_employee, name='delete-employee'),

    path('settings/', settings, name='settings'),
    path('edit-host-email/', edit_host_email, name='edit-host-email'),

]