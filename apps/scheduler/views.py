import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from apps.saloons.models import Saloon
from apps.barbers.models import Barber, Schedule, Service
from django.views.decorators.csrf import csrf_exempt
from time import strftime
# Create your views here.

def home(request):
    return render(request, 'home.html')

def scheduler(request):
    # Retrieve data to display on screen
    all_saloons = Saloon.objects.all()
    all_services = Service.objects.all()
    barbers = None
    saloon = None

    # Get desired saloon from user
    if request.method == 'POST':
        chosen_saloon = request.POST['saloon']
    
        barbers = Barber.objects.filter(saloon__city=chosen_saloon)
        saloon = Saloon.objects.get(city=chosen_saloon)

    
    context = {
        'all_saloons': all_saloons,
        'all_services': all_services,
        'barbers': barbers,
        'saloon': saloon,
    }

    return render(request, 'scheduler.html', context)


def modal(request, saloon, id):
    service = get_object_or_404(Service, id=id)
    saloon_ = Saloon.objects.get(city=saloon)
    barbers = None
    available_barbers = None
    available_schedule = {}

    if request.method == "POST":

        #  If user is sending date input
        if request.POST.get('date', False):

            date = request.POST['date']
            barbers = Barber.objects.filter(saloon=saloon_, service=service, schedule__date__in=[date]).distinct()

            # Create a set with hours available
            available_schedule = []
            for barber in barbers:
                for day in barber.schedule.all():
                    if str(day.date) == date and day.time.strftime('%H:%M') not in available_schedule:
                        available_schedule.append(day.time.strftime('%H:%M'))
                    else:
                        pass
            available_schedule.sort() 
        
        # If user is sending hour input
        if request.POST.get('hour', False):
            hour = request.POST['hour']
            date = request.POST['date']
            available_barbers = Barber.objects.filter(saloon=saloon_, service=service, schedule__date__in=[date], schedule__time__in=[hour]).distinct()

    context = {
        'service': service,
        'saloon': saloon_,
        'barbers': available_barbers,
        'available_schedule': available_schedule,
    }

    return render(request, 'modal.html', context)
