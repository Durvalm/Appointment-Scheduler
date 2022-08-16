from django.urls import path
from . import views

# All URLS related to scheduling
urlpatterns = [
    path('', views.home, name='home'),
    path('scheduler', views.scheduler, name='scheduler'),
    path('modal/<str:saloon>/<int:id>', views.modal, name='modal'),
    path('handle-payment', views.handle_payment, name="handle-payment"),
    path('create-appointment', views.create_appointment, name='create-appointment'),

]