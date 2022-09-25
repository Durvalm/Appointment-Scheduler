from django.shortcuts import render, redirect
from ..models import Service, Price, Barber
from django.contrib.auth.hashers import check_password
from django.contrib import messages

def barber_settings(request):
    """Render settings for the barber"""
    return render(request, 'barber/settings/settings.html')

def manage_services(request):
    """Lets barbers manage their services and how much they charge for each"""
    barber = request.user.barber
    prices = barber.price.all()

    context = {
        'prices': prices,
    }
    return render(request, 'barber/settings/manage-services.html', context)

def edit_service(request, id):
    """Allow Barber to change price of a service"""
    price = request.POST['price']

    # Edit service's price and save
    price_db = Price.objects.get(id=id)
    price_db.value = price
    price_db.save()
    return redirect('manage-services')

def delete_service(request, id):
    """Allow Barber to delete a service"""
    # Get price and service
    price = Price.objects.get(id=id)
    service = price.service

    # Remove price and service
    price.delete()
    request.user.barber.service.remove(service)
    return redirect('manage-services')

def add_service(request):
    """Allow barber to create a service"""
    # Get items from request
    service = request.POST['service'].title() 
    price = request.POST['price']

    # Create service if it doesn't exist
    service_db, created = Service.objects.get_or_create(name=service)
    # Create price
    price_db = Price.objects.create(value=price, service=service_db)

    # Add to the barber's DB
    request.user.barber.service.add(service_db)
    request.user.barber.price.add(price_db)

    return redirect('manage-services')

def change_barber_password(request):
    """Edit admin's password"""
    current_password = request.POST['current-password']
    new_password = request.POST['password1']
    repeat_password = request.POST['password2']

    # Check inputted current password with the actual one from the db
    match_check = check_password(current_password, request.user.password)
    if match_check:
        # check if both password entries match
        if new_password == repeat_password:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password has been changed, login again.')
            return redirect('login')
        else:
            messages.error(request, "Passwords don't match")
            return redirect('barber-settings')
    else:
        messages.error(request, 'Current password is not valid.')
        return redirect('barber-settings')

