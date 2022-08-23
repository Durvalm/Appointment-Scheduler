from urllib import request
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum

from .permissions import admin_member_required
from apps.saloons.models import Appointment

def query_date_range(request, start_date, end_date):
    """Helper function to query the database"""
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

@admin_member_required
def dashboard(request):
    """Render dashboard home page"""
    # if request.user.is_admin:
        # Query the database to get data from all appointments from last 30 days
    income, sales = query_date_range(request, timezone.now() - timezone.timedelta(days=30), timezone.now())

    context = {
        'user': request.user,
        'income': income,
        'sales': sales,
        'new_customers': 1
    }
    return render(request, 'admin/dashboard.html', context)
    # else:
    #     return HttpResponse('You are not an admin')

def date_filter(request):
    """Returns data filtered by determined date range"""
    # Get date range from the frontend
    start_date = request.GET['startDate']
    end_date = request.GET['endDate']

    # Query the database to get data from all appointments from date range input by user
    income, sales = query_date_range(request, start_date, end_date)

    return JsonResponse({
        'income': income,
        'sales': sales,
        'new_customers': 0
    })