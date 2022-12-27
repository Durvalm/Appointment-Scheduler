# Django imports
from django.core.cache import cache
from django.shortcuts import render
from django.contrib import messages

# Project imports
from apps.saloons.models import Saloon
from apps.barbers.models import Barber, Service
from ..services import is_single_saloon, get_available_hours

# Python imports
from datetime import date as today_date
from datetime import datetime


def home(request):
    """Renders out home page"""
    return render(request, 'home.html')


def scheduler(request):
    """Renders out scheduling page with all necessary data"""
    saloon = None
    # If there's only one saloon, retrieve it
    is_single = is_single_saloon()
    if is_single:
        saloon = Saloon.objects.first()
        cache.set('saloon', saloon)

    # If there's multiple saloons get cached saloon
    else:
        try:
            saloon = cache.get('saloon')
        except:
            saloon = None
    
    # If user has made an appointment, send an alert if it was successful or not
    if request.GET.get('success', None):
        messages.success(request, 'Your order was successful')
    elif request.GET.get('error', None):
        messages.warning(request, 'Try to make your appointment again')
      
    context = {
        'saloon': saloon,
        'is_single': is_single,
    }        
    return render(request, 'scheduler.html', context)

def search_saloon(request):
    """Handle Post request from saloon search"""
    try:
        chosen_saloon = request.POST['saloon']
        saloon = Saloon.objects.get(city=chosen_saloon)

    # Handle submission of non-existent saloon
    except Saloon.DoesNotExist:
        messages.error(request, 'Not found, please enter one of the options given!')

    cache.set('saloon', saloon)

    context = {
        'saloon': saloon,
    }
    return render(request, 'scheduler.html', context)

def modal(request, id):
    """Display modal"""
    service = Service.objects.get(id=id)
    cache.set('service', service)
    return render(request, 'modal.html')

def handle_date_input(request):
    """Handle user's date input in the modal"""
    # get data from request and session
    date = request.POST['date']
    saloon = cache.get('saloon')
    service = cache.get('service')

    # Get all barbers available in selected saloon, selected service, and selected date
    #  We will use this to retrieve every schedule available in a day for all barbers
    barbers = Barber.objects.filter(saloon=saloon, service=service, schedule__date__in=[date]).distinct()

    # Use helper function to get available schedule
    available_schedule = get_available_hours(barbers, date)

    # Display message if date has passed
    if datetime.strptime(date, "%Y-%m-%d").date() < today_date.today():
        messages.warning(request, 'Date has already passed')
        available_schedule = {}  # Show no hours
        
    #  Display message if no spots in a day
    elif len(available_schedule) == 0:
        messages.warning(request, 'No spots available in this day.')

    # Store date in sessions
    cache.set('date', date)
    cache.set('available_schedule', available_schedule)

    context = {
        'available_schedule': available_schedule,
    }

    return render(request, 'modal.html', context)

def handle_hour_input(request):
    """Handle user's hour input in the modal"""
    # get data from request and session
    hour =  request.POST['hour']
    date = cache.get('date')
    saloon = cache.get('saloon')
    service = cache.get('service')
    available_schedule = cache.get('available_schedule')
    
    # Filter barbers by available ones in determined date and hour
    # We'll use this to let user choose what barber he'd like
    available_barbers = Barber.objects.filter(saloon=saloon, service__in=[service], schedule__date__in=[date], schedule__time__in=[hour]).distinct()

    #  Display message if no barbers are available at this time
    if len(available_barbers) == 0:
        messages.warning(request, 'No barbers available for this service at this time, \
         please try another time from the options')
    
    # Store in session
    cache.set('hour', hour)
    # Store in queryset in cache
    cache.set('available_barbers', available_barbers) 
        
    context = {
        'barbers': available_barbers,
        'available_schedule': available_schedule,
    }

    return render(request, 'modal.html', context)

def handle_barber_input(request):
    """Handle user's 'barber' input in the modal"""
    # get data from request and session
    barber =  request.POST['barber']
    saloon = cache.get('saloon')
    service = cache.get('service')
    available_schedule = cache.get('available_schedule')
    available_barbers = cache.get('available_barbers')
    tax, cost, total = None, None, None

    # Get the chosen barber by user, and display price charged for determined service 
    try:
        chosen_barber = Barber.objects.get(user__username=barber, saloon=saloon)
        for price in chosen_barber.price.all():
            if price.service == service:
                cost = round(price.value, 2)
        # taxes in Florida
        tax = round(cost * 0.07, 2)
        total = cost + tax
    # Display message if there's no such barber
    except:
        messages.warning(request, 'Barber is not available for this service, please choose from the options.')
    
    context = {
        'tax': tax,
        'total': total,
        'cost': cost,
        'available_schedule': available_schedule,
        'barbers': available_barbers,
    }

    return render(request, 'modal.html', context)