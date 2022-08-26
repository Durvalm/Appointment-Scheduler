# Django imports
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
# App imports
from .utils import query_date_range, graph_first_entry
from .permissions import admin_member_required
 

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

def date_filter_graph(request):
    """returned filtered data for graph any date range"""    
    day_summary = graph_first_entry(request)
    return JsonResponse(day_summary)

