# Python imports
from datetime import date as _date
# Django imports
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
# App imports
from .utils import query_date_range, display_date, graph_first_entry
from .permissions import admin_member_required
from apps.saloons.models import Appointment
 

@admin_member_required
def dashboard(request):
    """Render dashboard home page"""
    # Query the database to get data from all appointments from last 30 days
    income, sales = query_date_range(request, timezone.now() - timezone.timedelta(days=29), timezone.now())  # This goes to the summary

    # get data for the graph's first entry
    graph_dict = graph_first_entry(request)
    graph_months = list(graph_dict.keys())
    graph_sales = list(graph_dict.values())
    months = list(graph_months)

    context = {
        'user': request.user,
        'income': round(income, 2),
        'sales': sales,
        'new_customers': 1,
        'graph_months': months,
        'graph_sales': graph_sales
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

    return JsonResponse(seven_day_summary)

def filter_graph_one_month(request):
    """Returns filtered data for the graph in 1 month daterange"""
    # Get start_date and end_date of the date range
    start_date = timezone.now() - timezone.timedelta(days=30)
    end_date = timezone.now() + timezone.timedelta(days=1)
    # get all appointments 
    appointments = Appointment.objects.filter(schedule__range=[start_date, end_date], saloon=request.user.saloon).order_by('schedule')

    # Create hash map to store days (key) and total income in each day (value)
    one_month_summary = {}
    
    # Iterate through all appointments
    for appointment in appointments:
        # Get numerical date by splitting __str__ method in schedule
        db_date = str(appointment.schedule).split(' ')[0]
        date = display_date(db_date, True)  # convert numerical date to prettier version
        # If date is not in the hashmap, add date as well as and income for each transaction
        if date not in one_month_summary.keys():
            one_month_summary[date] = appointment.total
        # If date was already added to the hashmap, add up income to the existing date key
        else:
            one_month_summary[date] += appointment.total    

    return JsonResponse(one_month_summary)

def filter_graph_three_months(request):
    """Returns filtered data for the graph in 3 month daterange"""
    # Get start_date and end_date of the date range
    start_date = timezone.now() - timezone.timedelta(days=90)
    end_date = timezone.now() + timezone.timedelta(days=1)
    # get all appointments 
    appointments = Appointment.objects.filter(schedule__range=[start_date, end_date], saloon=request.user.saloon).order_by('schedule')

    # Create hash map to store days (key) and total income in each day (value)
    three_months_summary = {}
    
    # Iterate through all appointments
    for appointment in appointments:
        # Get numerical date by splitting __str__ method in schedule
        db_date = str(appointment.schedule).split(' ')[0]
        date = display_date(db_date, True)  # convert numerical date to prettier version
        # If date is not in the hashmap, add date as well as and income for each transaction
        if date not in three_months_summary.keys():
            three_months_summary[date] = appointment.total
        # If date was already added to the hashmap, add up income to the existing date key
        else:
            three_months_summary[date] += appointment.total    

    return JsonResponse(three_months_summary)

def filter_graph_one_year(request):
    """Returns filtered data for the graph in 1 year daterange"""
    # Get start_date and end_date of the date range
    start_date = timezone.now() - timezone.timedelta(days=365)
    end_date = timezone.now() + timezone.timedelta(days=1)
    # get all appointments 
    appointments = Appointment.objects.filter(schedule__range=[start_date, end_date], saloon=request.user.saloon).order_by('schedule')

    # Create hash map to store days (key) and total income in each day (value)
    one_year_summary = {}
    
    # Iterate through all appointments
    for appointment in appointments:
        # Get numerical date by splitting __str__ method in schedule
        db_date = str(appointment.schedule).split(' ')[0]
        date = display_date(db_date, False)  # convert numerical date to prettier version
        # If date is not in the hashmap, add date as well as and income for each transaction
        if date not in one_year_summary.keys():
            one_year_summary[date] = appointment.total
        # If date was already added to the hashmap, add up income to the existing date key
        else:
            one_year_summary[date] += appointment.total    

    return JsonResponse(one_year_summary)

def filter_graph_ytd(request):
    """Returns filtered data for the graph in 1 year daterange"""
    # Get start_date and end_date of the date range
    start_date = _date(_date.today().year, 1, 1)
    end_date = timezone.now() + timezone.timedelta(days=1)
    # get all appointments 
    appointments = Appointment.objects.filter(schedule__range=[start_date, end_date], saloon=request.user.saloon).order_by('schedule')

    # Create hash map to store days (key) and total income in each day (value)
    ytd_summary = {}
    
    # Iterate through all appointments
    for appointment in appointments:
        # Get numerical date by splitting __str__ method in schedule
        db_date = str(appointment.schedule).split(' ')[0]
        date = display_date(db_date, False)  # convert numerical date to prettier version
        # If date is not in the hashmap, add date as well as and income for each transaction
        if date not in ytd_summary.keys():
            ytd_summary[date] = appointment.total
        # If date was already added to the hashmap, add up income to the existing date key
        else:
            ytd_summary[date] += appointment.total    

    return JsonResponse(ytd_summary)


