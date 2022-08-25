"""Important helper functions to the views"""

from datetime import timedelta, datetime
from apps.saloons.models import Appointment
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

def display_date(num_date):
    """Convert numerical date to Name date. ex (2022/08/22) = August 22"""
    # Month names
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    # Take off year from numerical date
    splitted_date = num_date.split('-')
    del(splitted_date[0])

    # Replace numerical month with month name
    month_name = months[int(splitted_date[0]) -1 ]

    # Create new string with month name
    day_month_date = f'{month_name} {splitted_date[1]}'

    return day_month_date   