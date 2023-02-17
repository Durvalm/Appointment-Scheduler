from datetime import datetime
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from apps.saloons.models import Appointment
from apps.barbers.models import Service
from ..services import change_status
from apps.scheduler.services import create_user
from apps.utils.permissions import barber_member_required

@barber_member_required
def employee_dashboard(request):
    """Render employee dashboard on the screen"""
    # Get first 10 entries of appointments made with request.barber
    appointments = Appointment.objects.filter(barber=request.user.barber, schedule__date=datetime.now().date()).order_by('-schedule')[:10:1]

    context = {
        'appointments': appointments,
    }

    return render(request, 'barber/dashboard.html', context)

def complete_appointment(request, id):
    """When completed button is clicked, change is_completed status"""
    change_status(id, 'is_completed')
    return redirect('employee-dashboard')

def pay_appointment(request, id):
    """When paid button is clicked, change is_paid status"""
    change_status(id, 'is_paid')
    return redirect('employee-dashboard')

def add_appointment(request):
    """Barber can create appointment manually when user hasn't made it online yet"""
    # Get items from post request
    name = request.POST['name']
    email = request.POST['email']
    service_name = request.POST['service']

    service = Service.objects.get(name=service_name, barber=request.user.barber)
    
    # Retrieve price from service selected
    for price in request.user.barber.price.all():
        if price.service == service:
            price = price

    # create user if user doesn't exist
    user = create_user(email, name)
    user.save()

    # Create appointment
    appointment = Appointment.objects.create(user=user, service=service, total=price.value, saloon=request.user.saloon,
                  is_paid=True, is_completed=True, schedule=timezone.now(), barber=request.user.barber)
    appointment.save()

    messages.success(request, 'Appointment successfully created')
    return redirect('employee-dashboard')
