# Django imports
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
# App imports
from .utils import query_date_range, display_date
from .permissions import admin_member_required
from apps.saloons.models import Appointment
 

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