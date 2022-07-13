from django.shortcuts import render
from apps.saloons.models import Saloon
from apps.barbers.models import Barber, Schedule, Service

# Create your views here.

def home(request):
    return render(request, 'home.html')

def scheduler(request):
    # Retrieve all saloons available
    saloons = Saloon.objects.all()
    barbers = None

    # Get desired saloon from user
    if request.method == 'POST':
        chosen_saloon = request.POST['saloon']
    
        barbers = Barber.objects.filter(saloon__city=chosen_saloon)

    context = {
        'saloons': saloons,
        'barbers': barbers,
    }

    return render(request, 'scheduler.html', context)


