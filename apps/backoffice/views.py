from datetime import timedelta, datetime
from datetime import date as _date

from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum

from .permissions import admin_member_required
from apps.saloons.models import Appointment

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

@admin_member_required
def dashboard(request):
    """Render dashboard home page"""
    # Query the database to get data from all appointments from last 30 days
    income, sales = query_date_range(request, timezone.now() - timezone.timedelta(days=29), timezone.now())

    context = {
        'user': request.user,
        'income': round(income, 2),
        'sales': sales,
        'new_customers': 1
    }
    return render(request, 'admin/dashboard.html', context)
    

def date_filter_dashboard(request):
    """Returns data filtered by determined date range"""
    # Get date range from the frontend
    start_date = request.GET['startDate']
    end_date = request.GET['endDate'] 

    # Query the database to get data from all appointments from date range input by user
    income, sales = query_date_range(request, start_date, end_date)

    return JsonResponse({
        'income': round(income, 2),
        'sales': sales,
        'new_customers': 0
    })

def filter_graph_seven_days(request):
    """Returns filtered data for the graph"""    
    # Get start_date and end_date from the date range
    start_date = timezone.now() - timezone.timedelta(days=6)
    end_date = timezone.now() + timezone.timedelta(days=1)
    # get all appointments 
    appointments = Appointment.objects.filter(schedule__range=[start_date, end_date], saloon=request.user.saloon).order_by('schedule')

    # Create hash map to store days (key) and total income in each day (value)
    seven_day_summary = {}
    # Iterate through all appointments
    for appointment in appointments:
        # Get numerical date by splitting __str__ method in schedule
        db_date = str(appointment.schedule).split(' ')[0]
        date = display_date(db_date)  # convert numerical date to prettier version
        # If date is not in the hashmap, add date as well as and income for each transaction
        if date not in seven_day_summary.keys():
            seven_day_summary[date] = appointment.total
        # If date was already added to the hashmap, add up income to the existing date key
        else:
            seven_day_summary[date] += appointment.total    


    return JsonResponse(seven_day_summary)