"""Important helper functions to the views"""

from datetime import timedelta, datetime
from apps.saloons.models import Appointment
from django.utils import timezone
from django.db.models import Sum


def query_date_range(request, start_date, end_date):
    """Helper function to query the database"""
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
    
    # Calculate total income in date range
    income_dict = appointments.aggregate(Sum('total'))
    income = income_dict['total__sum']
    if not income:
        income = 0
    # Count total of sales
    sales = appointments.count()

    return income, sales

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
    """Returns filtered data for the graph in 7 day daterange"""    
    # Get start_date and end_date of the date range
    start_date = timezone.now() - timezone.timedelta(days=7)
    end_date = timezone.now() + timezone.timedelta(days=1)
    # get all appointments 
    appointments = Appointment.objects.filter(schedule__range=[start_date, end_date], saloon=request.user.saloon).order_by('schedule')

    # Create hash map to store days (key) and total income in each day (value)
    seven_day_summary = {}
    # Iterate through all appointments
    for appointment in appointments:
        # Get numerical date by splitting __str__ method in schedule
        db_date = str(appointment.schedule).split(' ')[0]
        date = display_date(db_date, True)  # convert numerical date to prettier version
        # If date is not in the hashmap, add date as well as and income for each transaction
        if date not in seven_day_summary.keys():
            seven_day_summary[date] = appointment.total
        # If date was already added to the hashmap, add up income to the existing date key
        else:
            seven_day_summary[date] += appointment.total    

    return seven_day_summary