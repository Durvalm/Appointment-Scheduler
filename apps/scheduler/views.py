from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def scheduler(request):
    return render(request, 'scheduler.html')