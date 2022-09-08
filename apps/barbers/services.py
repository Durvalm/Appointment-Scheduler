from apps.saloons.models import Appointment

def change_status(id, status):
    """Changes is_completed and is_paid status of appointments"""
    appointment = Appointment.objects.get(id=id)

    # 'status' will be passed when function is called as (is_completed) or (is_paid)
    if status == 'is_completed':
        if appointment.is_completed:
            appointment.is_completed = False
        else:
            appointment.is_completed = True

    elif status == 'is_paid':
        if appointment.is_paid:
            appointment.is_paid = False
        else:
            appointment.is_paid = True

    appointment.save()