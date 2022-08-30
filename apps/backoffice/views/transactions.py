from django.shortcuts import render

def transactions(request):
    return render(request, 'admin/transactions.html')

