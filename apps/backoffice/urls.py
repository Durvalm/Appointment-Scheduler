from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('date-filter-dashboard/', views.date_filter_dashboard, name='date-filter-dashboard'),
    path('date-filter-graph/', views.date_filter_graph, name='date-filter-graph'),
]