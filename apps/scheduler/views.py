from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from apps.saloons.models import Saloon, Appointment
from apps.barbers.models import Barber, Schedule, Service
from django.contrib import messages

import stripe

# Email
from django.conf import settings
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    """Renders out home page"""
    return render(request, 'home.html')


def scheduler(request):
    """Renders out scheduling page with all necessary data"""
    # Retrieve data to display on screen (We'll display all saloons and services available)
    all_saloons = Saloon.objects.all()
    all_services = Service.objects.all()
    saloon = None

    # If user has ordered, display messaging confirming the order
    # Automatically update map with location retrieved from query params
    location = request.GET.get('location', '')
    if len(location) > 1:
        messages.success(request, 'Your order was successful')
        saloon = Saloon.objects.get(city=location)


    # Handle user's location request
    if request.method == 'POST':
        try:
            chosen_saloon = request.POST['saloon']
            saloon = Saloon.objects.get(city=chosen_saloon)

        # Handle submission of non-existent saloon
        except Saloon.DoesNotExist:
            messages.error(request, 'Not found, please enter one of the options given!')

    context = {
        'all_saloons': all_saloons,
        'all_services': all_services,
        'saloon': saloon,
    }

    return render(request, 'scheduler.html', context)


def modal(request, saloon, id):
    """Deal with every post request inside the modal"""

    # Get saloon and service sent in the url
    service = get_object_or_404(Service, id=id)
    saloon_ = Saloon.objects.get(city=saloon)
    # Initialize variables that will be sent to the frontend
    barbers = None
    cost = None
    tax = None
    total = None
    available_barbers = None
    available_schedule = {}

    if request.method == "POST":

        #  If user is sending date input
        if request.POST.get('date', False):

            date = request.POST['date']
            # Get allbarbers available in selected saloon, selected service, and selected date
            #  We will use this to retrieve every schedule available in a day for all barbers
            barbers = Barber.objects.filter(saloon=saloon_, service=service, schedule__date__in=[date]).distinct()

            # Create a set with all hours available for these barbers 
            available_schedule = []
            for barber in barbers:
                for day in barber.schedule.all():
                    # Append available time to the set
                    if str(day.date) == date and day.time.strftime('%H:%M') not in available_schedule and day.is_available:
                        available_schedule.append(day.time.strftime('%H:%M'))
                    else:
                        pass
            # Sort hour values to display in the frontend 
            available_schedule.sort()

            #  Display message if no spots in a day
            if len(available_schedule) == 0:
                messages.warning(request, 'No spots available in this day.')
        
        # If user is sending hour input
        if request.POST.get('hour', False):
            # Initialize variables
            hour = request.POST['hour']
            date = request.POST['date']

            # Filter barbers by available ones in determined date and hour
            # We'll use this to let user choose what barber he'd like
            available_barbers = Barber.objects.filter(saloon=saloon_, service__in=[service], schedule__date__in=[date], schedule__time__in=[hour]).distinct()

            #  Display message if no barbers are available at this time
            if len(available_barbers) == 0:
                messages.warning(request, 'No barbers available for this service at this time, please try another time from the options')

        #  If user is sending barber input
        if request.POST.get('barber', False):
            # initialize variables
            hour =  request.POST['hour']
            date = request.POST['date']
            barber = request.POST['barber'].split()
            # Get barber's first name to match in the database (change  it later)
            barber_first_name = barber[0]
            barber_last_name = barber[1]

            # Get the chosen barber by user, and display price charged for determined service 
            try:
                chosen_barber = Barber.objects.get(user__first_name=barber_first_name, user__last_name=barber_last_name, saloon=saloon_)
                for price in chosen_barber.price.all():
                    if price.service == service:
                        cost = round(price.value, 2)
                # taxes in Florida
                tax = round(cost * 0.07, 2)
                total = cost + tax
            # Display message if there's no such barber
            except Barber.DoesNotExist:
                messages.warning(request, 'Barber is not available for this service, please choose from the options.')

    context = {
        'service': service,
        'saloon': saloon_,
        'barbers': available_barbers,
        'available_schedule': available_schedule,
        'cost': cost,
        'tax': tax,
        'total': total,
    }

    return render(request, 'modal.html', context)


def appointment_submit(request):
    """Deal with appointment submission"""

    # Get all the data in appointment modal
    hours = request.POST['hour']
    date = request.POST['date']
    barber = request.POST['barber'].split()
    barber_first_name = barber[0]
    barber_last_name = barber[1]
    service = request.POST['service']
    saloon_city = request.POST['saloon']
    cost = request.POST['cost']
    total = request.POST['total']
    cost = float(cost)
    total = float(total)

    # Get queries and use them to create appointment
    barber = Barber.objects.get(user__first_name=barber_first_name, user__last_name=barber_last_name, saloon__city=saloon_city)
    schedule = Schedule.objects.get(date=date, time=hours, barber=barber)
    service = Service.objects.get(id=service)
    saloon = Saloon.objects.get(city=saloon_city)


    # Create Stripe appointment
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(total*100),
                        'product_data': {
                            'name': service.service
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000' + f'/scheduler?location={saloon_city}',
            cancel_url='http://127.0.0.1:8000' + '/cancel',
        )
    except Exception as e:
        return {'error': 'error'}
   
    # Create appointment
    appointment = Appointment.objects.create(schedule=schedule, barber=barber, service=service,
     saloon=saloon, price=cost, total=total, user=request.user)
    appointment.save()

    # Dissociate determined schedule from barber
    barber.schedule.remove(schedule)
    barber.save()

    # Send Email of appointment
    subject = f'Your Appointment to Super Barbershop in {saloon_city}'
    messages = [f'Hi {request.user.first_name}, thank you for relying on us, your appointment will be on day {date}, at {hours}.',
                f'New appointment with {request.user.first_name} on day {date}, at {hours}.']
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [request.user.email, barber.user.email]
    # Email sent to barber and to user
    send_mail(subject, messages[0], email_from, [recipient_list[0],])
    send_mail(subject, messages[1], email_from, [recipient_list[1],])

    return JsonResponse({"redirect": checkout_session.url})


def cancel(request):
    return render(request, 'payment/cancel.html')
    
