# Django imports
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
# App imports
from ..services import query_date_range, graph_first_entry, income_per_service
from ..permissions import admin_member_required
 

@admin_member_required
def dashboard(request):
    """Render dashboard home page"""
    # Query the database to get data from all appointments from last 30 days
    income, sales, new_customers = query_date_range(request, timezone.now() - timezone.timedelta(days=29), timezone.now())  # This goes to the summary

    # Graph's first entry 
    day_summary = graph_first_entry(request)
    graph_months = list(day_summary.keys())
    graph_sales = list(day_summary.values())    

    # Sservices summary
    service_summary = income_per_service()


    context = {
        'user': request.user,
        'income': round(income, 2),
        'sales': sales,
        'new_customers': new_customers,
        'graph_months': graph_months,
        'graph_sales': graph_sales,
        'service_summary': service_summary
    }
    return render(request, 'admin/dashboard.html', context)
    

def date_filter_dashboard(request):
    """Returns data filtered by determined date range"""
    # Get date range from the frontend
    start_date = request.GET['startDate']
    end_date = request.GET['endDate'] 

    # Query the database to get data from all appointments from date range input by user
    income, sales, new_customers = query_date_range(request, start_date, end_date)

    return JsonResponse({
        'income': round(income, 2),
        'sales': sales,
        'new_customers': new_customers
    })

def date_filter_graph(request):
    """returned filtered data for graph any date range"""   
    day_summary = graph_first_entry(request)
    return JsonResponse(day_summary)

