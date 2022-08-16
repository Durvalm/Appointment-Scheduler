from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from apps.saloons.models import Saloon, Appointment
from apps.barbers.models import Barber, Schedule, Service
from apps.users.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from datetime import date as today_date
from datetime import datetime
from django.utils import timezone
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
    # If order has failed, display messaging
    if request.GET.get('transaction'):
        messages.warning(request, 'Try to make your appointment again')

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

            # Display message if date has passed
            if datetime.strptime(date, "%Y-%m-%d").date() < today_date.today():
                messages.warning(request, 'Date has already passed')
                available_schedule = {}  # "Gambiarra" to stop execution of function
                
            #  Display message if no spots in a day
            elif len(available_schedule) == 0:
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
            barber = request.POST['barber']

            # Get the chosen barber by user, and display price charged for determined service 
            try:
                chosen_barber = Barber.objects.get(user__username=barber, saloon=saloon_)
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


def handle_payment(request):
    """Deal with appointment submission"""
    # Get all the data in appointment modal
    barber = request.POST['barber']
    service_id = request.POST['service']
    saloon_city = request.POST['saloon']
    total = float(request.POST['total'])

    service = Service.objects.get(id=service_id)

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
            metadata={
                'hours': request.POST['hour'],
                'date': request.POST['date'],
                'barber': barber,
                'service': service.service,
                'saloon_city': request.POST['saloon'],
                'cost': float(request.POST['cost']),
                'total': total,
            },
            mode='payment',
            success_url='http://127.0.0.1:8000' + f'/scheduler?location={saloon_city}',
            cancel_url='http://127.0.0.1:8000' + f'/scheduler?transaction=none',
        )
    except Exception as e:
        return JsonResponse({"error": "error"})


    return JsonResponse({"redirect": checkout_session.url})


@csrf_exempt
def create_appointment(request):
    """Creates appointment after payment is successful, sends email, updates database, etc"""
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

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Get data from json response in stripe session
        name = session['customer_details']['name']
        email = session['customer_details']['email']
        hours = session['metadata']['hours']
        date = session['metadata']['date']
        barber = session['metadata']['barber']
        service = session['metadata']['service']
        saloon_city = session['metadata']['saloon_city']
        cost = session['metadata']['cost']
        total = session['metadata']['total']

        # Get queries and use them to create appointment
        barber = Barber.objects.get(user__username=barber, saloon__city=saloon_city)
        service = Service.objects.get(service=service)
        saloon = Saloon.objects.get(city=saloon_city)
        # transform date and hour field into datetime
        appointment_date = datetime.strptime(f'{date} {hours}', '%Y-%m-%d %H:%M')

        # If returning user, create appointment with existing user
        try:
            user = User.objects.get(email=email)
        # if new user, create User in the database
        except:
            user = User.objects.create(username=name, email=email)
            user.save()

        # Create appointment
        appointment = Appointment.objects.create(schedule=appointment_date, barber=barber, service=service,
        saloon=saloon, price=cost, total=total, user=user)
        appointment.save()

        # Dissociate determined schedule from barber
        schedule = Schedule.objects.get(date=date, time=hours, barber=barber)
        barber.schedule.remove(schedule)
        barber.save()

        # Send Email of appointment
        subject = f'Your Appointment to Super Barbershop in {saloon_city}'
        messages = [f'Hi {user.username}, thank you for relying on us, your appointment will be on day {date}, at {hours}.',
                    f'New appointment with {user.username} on day {date}, at {hours}.']
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, barber.user.email]
        # Email sent to barber and to user
        send_mail(subject, messages[0], email_from, [recipient_list[0],])
        send_mail(subject, messages[1], email_from, [recipient_list[1],])
            
        # Passed signature verification
    return HttpResponse(status=200)
