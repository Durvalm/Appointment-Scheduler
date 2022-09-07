from apps.saloons.models import Saloon
from apps.barbers.models import Service


def all_saloons(request):
    all_saloons = Saloon.objects.all()
    return dict(all_saloons=all_saloons)


def all_services(request):
    all_services = Service.objects.all()
    return dict(all_services=all_services)

