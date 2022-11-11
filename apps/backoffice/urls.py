from django.urls import path
from .views.dashboard import dashboard, date_filter_dashboard, date_filter_graph
from .views.transactions import transactions
from .views.employees import employees, add_employee, edit_employee, delete_employee
from .views.settings import (settings, edit_host_email, manage_permissions, edit_permissions,
                             edit_profile, change_password, manage_stores, add_saloon, delete_saloon,
                             )

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
    path('manage-permissions/', manage_permissions, name='manage-permissions'),
    path('edit-permissions/<int:id>/', edit_permissions, name='edit-permissions'),
    path('manage-stores/', manage_stores, name='manage-stores'),
    path('add-saloon/', add_saloon, name='add-saloon'),
    path('delete-saloon/<int:id>/', delete_saloon, name='delete-saloon'),
    path('edit-host-email/', edit_host_email, name='edit-host-email'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('change-password/', change_password, name='change-password'),

]