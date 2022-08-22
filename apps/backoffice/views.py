from django.shortcuts import render

def dashboard(request):
    """Render dashboard home page"""
    return render(request, 'admin/dashboard.html')