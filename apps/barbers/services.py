from datetime import timedelta, date
from django.shortcuts import redirect
from django.utils import timezone
from apps.saloons.models import Appointment
from apps.barbers.models import Schedule


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

def convert_weekday_to_number(weekday):
    """Convert weekday ex: 'tuesday' to number '3' """
    num_day = ''
    if weekday == 'Monday':
        num_day = 0
    elif weekday == 'Tuesday':
        num_day = 1
    elif weekday == 'Wednesday':
        num_day = 2
    elif weekday == 'Thursday':
        num_day = 3
    elif weekday == 'Friday':
        num_day = 4
    elif weekday == 'Saturday':
        num_day = 5
    elif weekday == 'Sunday':
        num_day = 6
    else:
        num_day = None
    return num_day

# Month names
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
def display_pretty_datetime(num_date):
    # Take out hour
    month = num_date.split(' ')[0]
    # Split date
    splitted_date = month.split('-')

    # Replace numerical month with month name
    month_name = months[int(splitted_date[1]) -1 ]

    # Take Year out of numerical date
    del(splitted_date[0])
    # Create new string with month name
    new_date = f'{month_name} {splitted_date[1]}'
        
    return new_date   
        
def add_delete_barber_schedules(request, working_schedule, action):
    """Add or Delete schedules related to barber in 14 days"""
    # Get all hours in created working_schedule
    hour_lst = working_schedule.get_all_hours(working_schedule)
    print(hour_lst)
    
    # Remove schedules for 14 days
    for day in range(15):
        # Create timezone.now() + timedelta(days=day) to count current day
        current_day = timezone.now().date() + timedelta(days=day)

        # Check what day in the week the current day is
        current_weekday = current_day.weekday()

        # Add schedules for every hour in list
        for hour in hour_lst:
            print(hour)
            if current_weekday == working_schedule.day:
                if action == 'delete':
                    try:
                        schedule = Schedule.objects.get(date=current_day, time=hour)
                        request.user.barber.schedule.remove(schedule)
                    except:
                        continue
                elif action == 'add':
                    schedule, created = Schedule.objects.get_or_create(date=current_day, time=hour, is_available=True)
                    request.user.barber.schedule.add(schedule)


def date_time_dictionary(request):
    """Get dictionary of Key=Day, Values=Hours in barber's schedule"""
    # Dictionary in which Day is a key and hours in a day are the values
    date_and_time = {}
    # Iterate through all schedules from current barber
    for schedule in request.user.barber.schedule.all().order_by('date'):
        # Call display_pretty_datetime function
        schedule_ = display_pretty_datetime(schedule.__str__())

        # Add Schedule Day and Hours to the dict, Each Day appears one time and has a list of all hours
        if schedule_ in date_and_time.keys():
            date_and_time[schedule_].append(str(schedule.time))
        else:
            date_and_time[schedule_] = {}
            date_and_time[schedule_] = [str(schedule.time)]
    return date_and_time

def get_all_schedules(request):
    """Get all schedule's dates and ids from specific barber"""
    # Dictionary that holds Schedule Day and Id
    schedule_dict = {}
    # Get all schedules from barber
    for schedule in request.user.barber.schedule.all().order_by('date'):
        # Call display_pretty_datetime function
        schedule_ = display_pretty_datetime(schedule.__str__())

        # Prevent duplication in Day keys, and add Id as a value
        if schedule_ not in schedule_dict.keys():
            schedule_dict[schedule_] = schedule.id
    return schedule_dict

def get_all_hours(queryset):
    """Get all schedule's hours and ids from specific barber"""
    # Dictionary that holds Schedule Hour and Id
    hour_dict = {}
    # Get all schedules from barber
    for schedule in queryset:  # queryset == schedule
        # Prevent duplication in Day keys, and add Id as a value
        if str(schedule.time.strftime("%H:%M %p")) not in hour_dict.keys():
            hour_dict[str(schedule.time.strftime("%I:%M %p"))] = schedule.id
    return hour_dict
