from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('date-filter/', views.date_filter, name='date-filter'),
]