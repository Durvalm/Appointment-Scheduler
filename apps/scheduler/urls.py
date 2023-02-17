from django.urls import path
from .views.modal import (home, scheduler, search_saloon, modal, handle_date_input,
                          handle_hour_input, handle_barber_input, professionals)
from .views.payment import handle_payment, create_appointment
# All URLS related to scheduling
urlpatterns = [
    path('', home, name='home'),
    path('scheduler/', scheduler, name='scheduler'),
    path('professionals/', professionals, name='professionals'),
    path('search-saloon/', search_saloon, name='search-saloon'),
    path('modal/<int:id>/', modal, name='modal'),
    path('handle-date-input/', handle_date_input, name='handle-date-input'),
    path('handle-hour-input/', handle_hour_input, name='handle-hour-input'),
    path('handle-barber-input/', handle_barber_input, name='handle-barber-input'),
    path('handle-payment/', handle_payment, name='handle-payment'),
    path('create-appointment/', create_appointment, name='create-appointment'),
]