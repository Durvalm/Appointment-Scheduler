import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from apps.saloons.models import Saloon
from apps.barbers.models import Barber, Schedule, Service
from django.views.decorators.csrf import csrf_exempt

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
    available_schedule = {}

    # Post date from user inside modal
    if request.method == "POST":

        date = request.POST['date']

        barbers = Barber.objects.filter(saloon=saloon_, service=service, schedule__date__in=[date]).distinct()

        available_schedule = {}
        for barber in barbers:
            for day in barber.schedule.all():
                if barber.user.first_name in available_schedule and str(day.date) == str(date):
                    available_schedule[barber.user.first_name].append(str(day.time))
                elif barber.user.first_name not in available_schedule and str(day.date) == str(date):
                    available_schedule[barber.user.first_name] = [str(day.time)]
                else:
                    pass
        print(available_schedule)

    # Get Service id
    else:
        print("GET")
        pass

    context = {
        'service': service,
        'saloon': saloon_,
        'barbers': barbers,
        'available_schedule': available_schedule,
    }

    return render(request, 'modal.html', context)
