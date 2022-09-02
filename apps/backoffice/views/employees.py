from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from apps.barbers.models import Barber
from apps.saloons.models import Saloon
from apps.users.models import User

def employees(request):
    """Display all employees"""
    barbers = Barber.objects.filter(saloon=request.user.saloon)

    context = {
        'barbers': barbers
    }
    return render(request, 'admin/employees.html', context)

def add_employee(request):
    """Add new employee to the DB"""
    # Get data from request
    email = request.POST['email']
    username = request.POST['name']
    password = request.POST['password']
    password1 = request.POST['password1']

    # Check if password is correct
    if password == password1:
        # Return error if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'The email is already in use!')
            return redirect('employees')
        else:
            # if all information is valid, create user
            user = User.objects.create_barber(email=email, username=username)
            barber = Barber.objects.create(user_id=user.id, saloon=request.user.saloon)
            user.save()
            barber.save()
            
            messages.success(request, 'User successfully added')
            return redirect('employees')
    else:
        messages.error(request, "Passwords don't match")
        return redirect('employees')

def edit_employee(request):
    """Update employee information"""
    email = request.POST['email']
    username = request.POST['name']
    password = request.POST['password']
    password1 = request.POST['password1']
    is_admin = request.POST.get('is_admin', False)

    if is_admin == 'on':
        is_admin = True

    # If password matchs, proceed
    if password == password1:
        user = User.objects.get(email=email)
        if not user:
            messages.error(request, "The email doesn't exist!")
            return redirect('employees')
        else:
            # if all information is valid, create user
            user.email = email
            user.username = username
            user.is_admin = is_admin
            if password:
                user.set_password(password)
                user.save()
            
            messages.success(request, 'User successfully edited')
            return redirect('employees')
    else:
        messages.error(request, "Passwords don't match")
        return redirect('employees')

def delete_employee(request, id):
    """Delete employee"""
    user = User.objects.get(id=id)
    user.delete()
    return redirect('employees')
