from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('date-filter-dashboard/', views.date_filter_dashboard, name='date-filter-dashboard'),
    # Graph related endpoints
    path('filter-graph-seven-days/', views.filter_graph_seven_days, name='filter-graph-seven-days'),
    path('filter-graph-one-month/', views.filter_graph_one_month, name='filter-graph-one-month'),
    path('filter-graph-three-months/', views.filter_graph_three_months, name='filter-graph-three-months'),
    path('filter-graph-one-year/', views.filter_graph_one_year, name='filter-graph-one-year'),
    path('filter-graph-ytd/', views.filter_graph_ytd, name='filter-graph-ytd'),
]