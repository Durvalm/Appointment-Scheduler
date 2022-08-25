from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('date-filter-dashboard/', views.date_filter_dashboard, name='date-filter-dashboard'),
    path('filter-graph-seven-days/', views.filter_graph_seven_days, name='filter-graph-seven-days'),

]