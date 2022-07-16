import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from apps.saloons.models import Saloon
from apps.barbers.models import Barber, Schedule, Service

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
    if request.method == "POST":
        saloon_ = Saloon.objects.get(city=saloon)
        barbers = Barber.objects.filter(saloon=saloon_)
        print(service, saloon_, barbers)
        for i in barbers:
            print(i.user.first_name)
        
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "movieListChanged": None,
                    "showMessage": f"{service.service} updated."
                })
            }
        )
    else:
        print(service)
    return render(request, 'modal.html', {
        'service': service,
    })