from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('scheduler', views.scheduler, name='scheduler'),
    path('modal/<str:saloon>/<int:id>', views.modal, name='modal'),
]