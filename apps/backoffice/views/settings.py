from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from apps.users.models import Admin, User
from apps.barbers.models import Barber

from apps.core.email_host import get_email_host
from django.core.mail import get_connection, send_mail


def settings(request):
    """Render settings in the screen"""
    return render(request, 'admin/settings/settings.html')

def edit_host_email(request):
    """Edit store's email (the one that sends emails to everyone) and secure code"""
    # get email and secure code
    email = request.POST['email']
    secure_code = request.POST['code']

    admin_user = Admin.objects.get(user=request.user)

    # Update email host and secure code in the database
    admin_user.host_email = email
    if secure_code:
        admin_user.host_passcode = secure_code
    admin_user.save()

    messages.success(request, 'Your email host was successfully changed')
    return redirect('settings')

def manage_permissions(request):
    """Render permissions.html for admin to manage who can be an admin"""
    barbers = Barber.objects.filter(saloon=request.user.saloon)

    context = {
        'barbers': barbers,
    }
    return render(request, 'admin/settings/permissions.html', context)

def edit_permissions(request, id):
    """Edits permissions based on admin input"""
    barber = Barber.objects.get(id=id)

    # if user is staff, take off staff status
    if barber.user.is_staff:
        barber.user.is_staff = False
    else:
    # If user is not staff, make him staff
        barber.user.is_staff = True
    barber.user.save()

    return redirect('manage-permissions')

def edit_profile(request):
    """Edit admin's email and username"""
    if request.method == 'POST':
        # POST request from user (get data)
        email = request.POST['email']
        username = request.POST['username']
        
        user = User.objects.filter(email=email)

        # if inputted email already exists in the db, throw an error
        if user.exists():
            messages.error(request, 'Email already exists, try another!')
        # if inputted email doesn't exist in the database, edit profile.
        else:
            request.user.email = email
            request.user.username = username
            request.user.save()
            messages.success(request, 'Successfully changed!')
        return redirect('settings')

def change_password(request):
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
        else:
            messages.error(request, "Passwords don't match")
    else:
        messages.error(request, 'Current password is not valid.')
    return redirect('login')
