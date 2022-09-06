"""Important helper functions to the views"""
from datetime import date as _date
from datetime import timedelta, datetime
from apps.saloons.models import Appointment
from apps.barbers.models import Service, Barber
from apps.users.models import User
from django.utils import timezone
from django.db.models import Sum


def query_date_range(request, start_date, end_date):
    """Helper function to query the database for the dashboard summary"""
    # Add 1 more day to end_date (obs: data comes in str and datetime format, 
    # if it comes in str format convert it, if it comes in datetime format, just add 1 day more
    if type(end_date) == str:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')  # convert str date to datetime obj
        end_date += timedelta(days=1)  # Add 1 day
        end_date = str(end_date)  # Convert back to str
    else:
        end_date += timedelta(days=1)  # Add 1 day

    # Query total of appointments in determined date range
    appointments = Appointment.objects.filter(schedule__range=[start_date, end_date], saloon=request.user.saloon)
    # Query total of users that joined in determined date range
    users = User.objects.filter(date_joined__range=[start_date, end_date], saloon=request.user.saloon, is_admin=False, is_barber=False)

    # Calculate total income in date range
    income_dict = appointments.aggregate(Sum('total'))
    income = income_dict['total__sum']
    if not income:
        income = 0

    # Count total of sales
    sales = appointments.count()

    # Count total of new users
    new_customers = users.count()


    return income, sales, new_customers


# Month names
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

def display_date(num_date, day_format):
    """Convert numerical date to Name date. ex (2022/08/22) = August 22"""

    # Split date
    splitted_date = num_date.split('-')
    # Replace numerical month with month name
    month_name = months[int(splitted_date[1]) -1 ]

    if day_format:
        # Take Year out of numerical date
        del(splitted_date[0])
        # Create new string with month name
        new_date = f'{month_name} {splitted_date[1]}'

    elif not day_format:
        # Take Day out of numerical date
        del(splitted_date[2])
        # Create new string with month name
        new_date = f'{month_name} {splitted_date[0]}'

    return new_date   

def graph_first_entry(request):
    """returned filtered data for graph any date range"""
    # Get days from input
    try:
        days = int(request.GET['days'])  # If there are days in the request, store it in the variable days
    except:
        days = 7  # if there's no input in the request, we are loading the page for the first time.  Return 7 days as initial value

    # Don't display day and month if (days > 90)
    display_day_month = True
    if days > 90:
        display_day_month = False

    # Get start_date and end_date of the date range
    if days == 366: # This means user input is (YTD)
        start_date = _date(_date.today().year, 1, 1)
    else:
        start_date = timezone.now() - timezone.timedelta(days=days)  # if user input is anything other than YTD
    end_date = timezone.now() + timezone.timedelta(days=1)

    # get all appointments 
    appointments = Appointment.objects.filter(schedule__range=[start_date, end_date], saloon=request.user.saloon).order_by('schedule')

    # Create hash map to store days (key) and total income in each day (value)
    day_summary = {}
    # Iterate through all appointments
    for appointment in appointments:
        # Get numerical date by splitting __str__ method in schedule
        db_date = str(appointment.schedule).split(' ')[0]
        date = display_date(db_date, display_day_month)  # convert numerical date to prettier version
        # If date is not in the hashmap, add date as well as and income for each transaction
        if date not in day_summary.keys():
            day_summary[date] = appointment.total
        # If date was already added to the hashmap, add up income to the existing date key
        else:
            day_summary[date] += appointment.total

    return day_summary


def income_per_service(request):
    """Get income and per each service"""
    # Get all services
    services = Service.objects.all()
    # Create dictionaty to store services and their stats
    service_summary = {}

    # Loop through each service
    for service in services:
        appointments = Appointment.objects.filter(service=service, saloon=request.user.saloon)  # Query all appointments for each service
        sales = appointments.count()  # Get total sales count for each service
        sum_dict = Appointment.objects.filter(service=service, saloon=request.user.saloon).aggregate(Sum('total'))  # Get total income brought in by each service
        total = sum_dict['total__sum']

        # Append Service, income, and sales to the dictionary
        service_summary[service.service] = {}
        service_summary[service.service]['income'] = round(total, 2)
        service_summary[service.service]['sales'] = sales

    return service_summary

def income_per_employee(request):
    """Get income and per each employee"""
    # Get all barbers
    barbers = Barber.objects.all()
    # Create dictionaty to store barbers and their stats
    barber_summary = {}

    # Loop through each barber
    for barber in barbers:
        appointments = Appointment.objects.filter(barber=barber, saloon=request.user.saloon)  # Query all appointments for each barber
        sales = appointments.count()  # Get total sales count for each service
        sum_dict = Appointment.objects.filter(barber=barber, saloon=request.user.saloon).aggregate(Sum('total'))  # Get total income brought in by each service
        total = sum_dict['total__sum']

        # Append Service, income, and sales to the dictionary
        barber_summary[barber.user.username] = {}
        if total is None:
            barber_summary[barber.user.username]['income'] = 0
        else:
            barber_summary[barber.user.username]['income'] = round(total, 2)
        barber_summary[barber.user.username]['sales'] = sales
        
    return barber_summary

