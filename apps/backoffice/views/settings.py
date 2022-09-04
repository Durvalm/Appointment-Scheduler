from django.shortcuts import render, redirect
from django.contrib import messages
from apps.users.models import Admin
from apps.core.email_host import get_email_host
from django.core.mail import get_connection, send_mail


def settings(request):
    """Render settings in the screen"""
    return render(request, 'admin/settings.html')

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

