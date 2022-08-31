from ast import keyword
from django.urls import path
from .views import dashboard, transactions

urlpatterns = [
    path('dashboard/', dashboard.dashboard, name='dashboard'),
    path('date-filter-dashboard/', dashboard.date_filter_dashboard, name='date-filter-dashboard'),
    path('date-filter-graph/', dashboard.date_filter_graph, name='date-filter-graph'),

    path('transactions/', transactions.transactions, name='transactions'),
]