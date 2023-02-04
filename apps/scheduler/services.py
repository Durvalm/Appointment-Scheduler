from django.core.mail import send_mail
from django.http import HttpResponse

from apps.saloons.models import Saloon
from apps.users.models import User
from apps.core.email_host import get_email_host
from django.conf import settings

import stripe


def is_single_saloon():
    # Saloon quantity
    single_saloon = True
    saloons = Saloon.objects.all()
    count = saloons.count()
    if count > 1:
        single_saloon = False
    return single_saloon


def get_available_hours(barbers, date):
    """Get all hours available from all barbers"""
    # Create a set with all hours available for these barbers 
    available_schedule = []
    for barber in barbers:
        for day in barber.schedule.all():
            # Append available time to the set
            if str(day.date) == date and day.time.strftime('%H:%M') not in available_schedule and day.is_available:
                available_schedule.append(day.time.strftime('%I:%M %p'))  # Display AM PM format to users
            else:
                pass

    # Return Sorted hour values to display in the frontend 
    available_schedule.sort()

    return available_schedule

def create_user(email, name):
    """Create user for appointment"""
    # If returning user, create appointment with existing user
    try:
        user = User.objects.get(email=email)
    # if new user, create User in the database
    except:
        user = User.objects.create(username=name, email=email)

    return user

def add_total_spent(user, total):
    """adds up all time money spent from user"""
    # Add Total spent to user db
    if user.total_spent is not None:
        user.total_spent += float(total)
    else:
        user.total_spent = float(total)
    user.save()

def send_appointment_mail(user, saloon, barber, date, hours):
    # Send Email of appointment
    connection = get_email_host(saloon)
    subject = f'Your Appointment to Super Barbershop in {saloon.city}'
    messages = [f'Hi {user.username}, thank you for relying on us, your appointment will be on day {date}, at {hours}.',
                f'New appointment with {user.username} on day {date}, at {hours}.']
    email_from = saloon.admin.host_email
    recipient_list = [user.email, barber.user.email]
    # Email sent to barber and to user
    send_mail(subject, messages[0], email_from, [recipient_list[0],], connection=connection)
    send_mail(subject, messages[1], email_from, [recipient_list[1],], connection=connection)

def get_payment_session(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    # Construct webhook event
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    return event
