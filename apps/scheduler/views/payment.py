# Django imports
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Project imports
from apps.saloons.models import Saloon, Appointment
from apps.barbers.models import Barber, Schedule, Service
from ..services import create_user, add_total_spent, send_appointment_mail, get_payment_session

# Python imports
from datetime import datetime

# Custom imports
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def handle_payment(request):
    """Deal with appointment submission"""
    # Get all the data in appointment modal
    barber = request.POST['barber']
    service = cache.get('service')
    saloon = cache.get('saloon')
    total = float(request.POST['total'])

    # Create Stripe appointment
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(total*100),
                        'product_data': {
                            'name': service.name,
                            'images': ['https://i2.wp.com/therighthairstyles.com/wp-content/uploads/2021/09/1-the-ivy-league-mens-cut.jpg?resize=500%2C592',]
                        },
                    },
                    'quantity': 1,
                    
                },
            ],
            metadata={
                'hours': request.POST['hour'],
                'date': request.POST['date'],
                'barber': barber,
                'service': service.name,
                'saloon': saloon.city,
                'cost': float(request.POST['cost']),
                'total': total,
            },
            # description='EXAMPLE',
            # images=['https://cdn.pixabay.com/photo/2016/03/21/23/25/link-1271843__480.png'],
            mode='payment',
            success_url='http://127.0.0.1:8000' + f'/scheduler/?success=yes',
            cancel_url='http://127.0.0.1:8000' + f'/scheduler/?error=yes',
        )
    except Exception as e:
        return JsonResponse({"error": "error"}) 


    return JsonResponse({"redirect": checkout_session.url})

@csrf_exempt
def create_appointment(request):
    """Creates appointment after payment is successful, sends email, updates database, etc"""
    # call helper function to get stripe event
    event = get_payment_session(request)

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
        saloon = session['metadata']['saloon']
        cost = session['metadata']['cost']
        total = session['metadata']['total']

        # Get queries and use them to create appointment
        barber = Barber.objects.get(user__username=barber, saloon__city=saloon)
        service = Service.objects.get(service__name=service)
        saloon = Saloon.objects.get(city=saloon)

        # transform date and hour field into datetime
        appointment_date = datetime.strptime(f'{date} {hours}', '%Y-%m-%d %H:%M')

        # Create user
        user = create_user(email, name)
            
        # Add up money spent by user
        add_total_spent(user, total)

        # Create appointment
        appointment = Appointment.objects.create(schedule=appointment_date, barber=barber, service=service,
        saloon=saloon, price=cost, total=total, user=user)
        appointment.save()

        # Dissociate determined schedule from barber
        schedule = Schedule.objects.get(date=date, time=hours, barber=barber)
        barber.schedule.remove(schedule)
        barber.save()

        # Transform hour field in AM/PM format
        hours = datetime.strptime(hours, '%H:%M')
        hours = hours.strftime("%I:%M %p")

        # Send email
        send_appointment_mail(user, saloon, barber, date, hours)        
            
    # Passed signature verification
    return HttpResponse(status=200)
