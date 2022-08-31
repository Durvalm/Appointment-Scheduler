from django.shortcuts import render
from apps.saloons.models import Appointment
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.http import HttpResponse


def transactions(request):
    """Render transactions page on the screen with all transactions, paginator, and search"""
    # Get all appointments in determined saloon (default when page is rendered)
    appointments = Appointment.objects.filter(saloon=request.user.saloon).order_by('-schedule')
    keyword = ''  # Empty string will bring up all appointments 

    if 'keyword' in request.GET:  # if keyword is in url params
        keyword = request.GET['keyword']  # Get keyword
        if keyword is not None:  # If keyword is not an empty string
            # Filter appointments according to keyword
            appointments = Appointment.objects.order_by('-schedule').filter(Q(user__username__icontains=keyword) | Q(barber__user__username__icontains=keyword), saloon=request.user.saloon)
        else:  # If keyword is an empty string, bring up all appointments
            appointments = Appointment.objects.filter(saloon=request.user.saloon).order_by('-schedule')

    # Get all total of all sales
    # Calculate total income in date range
    income_dict = appointments.aggregate(Sum('total'))
    income = income_dict['total__sum']
    if not income:
        income = 0
    
    # Count total of sales
    sales = appointments.count()

    # Paginator setup
    paginator = Paginator(appointments, 50) # Item limit per page
    page_number = request.GET.get('page') # get current page from url params
    page_obj = paginator.get_page(page_number) # Paginator object 

    # initial page range
    page_range = range(1, 11)
    # Configure page range preventing non existing page number to appear
    if page_number and int(page_number) > 9:
        if int(page_number) + 5 > page_obj.paginator.page_range[-1]: # If current page + 5 is bigger than maximum page number
            page_range = range(int(page_number) -5, page_obj.paginator.page_range[-1] + 1) # Set max limit to page number | min to (page number - 5)
        else:
            page_range = range(int(page_number) -5, int(page_number) + 5) # If current page not greater than 5, max limit = page num + 5
    elif not page_number:
        pass

    context = {
        'appointments': page_obj,
        'page_range': page_range,
        'sales': sales,
        'income': round(income, 2),
        'keyword': keyword
    }
    return render(request, 'admin/transactions.html', context)
