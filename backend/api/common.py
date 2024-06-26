import requests, threading, time, multiprocessing
from task.models import Task
from django.utils import timezone
from datetime import timedelta as td
from zoneinfo import ZoneInfo
from api.models import *


from logging import getLogger
logger = getLogger(__name__)

def validate_entry(entry, validators):
    if all(x in entry for x in validators):
        return True
    return False

def start_task(monitor):
    r = requests.get(f"http://jobs:8000/create-task?monitor_id={monitor.id}")
    if r and r.status_code == 200:
            logger.info(f"Created job for monitor {monitor.id}")


def delete_task(monitor):
    tasks = Task.objects.filter(verbose_name=str(monitor.id))
    if tasks:
        for task in tasks:
            task.delete()
        logger.info(f"Paused job for monitor {monitor.id}")

def sync_jobs():
    monitors = Monitor.objects.all()
    for monitor in monitors:
        jobs = Task.objects.filter(verbose_name=str(monitor.id))
        if not jobs and monitor.running:
            start_task(monitor)
        elif jobs.count() > 1 and monitor.running:
            for job in jobs[1:]:
                job.delete()
        elif jobs and not monitor.running:
            for job in jobs:
                job.delete()

def calculate_percentage(response, max):
    percentage = (response * 100) / max
    return percentage

def get_verbose_date(date):
    return f"{date.strftime('%d')} {date.strftime('%b')} {date.year}"

def get_verbose_datetime(date):
    return f"{date.strftime('%d')} {date.strftime('%b')} {date.year} - {date.strftime('%H')}:{date.strftime('%M')}:{date.strftime('%S')}"

def calculate_response(events):
    response_time = 0
    for event in events:
        response_time += event.time
    response = round(response_time/events.count(), 2) if events else 0
    return response

def calculate_uptime(events):
    downtimes = events.filter(failure_start=True)
    downtimes_end = events.filter(failure_end=True)
    if downtimes or downtimes_end:
        incident_time = 0
        for downtime in downtimes:
            downtime_fixed = events.filter(created_time__gt=downtime.created_time, failure_end=True).order_by("id")
            if downtime_fixed:
                downtime_fixed = downtime_fixed[0]
                time_of_incident = downtime_fixed.created_time - downtime.created_time
                time_of_incident = time_of_incident.total_seconds()*1000
                incident_time += time_of_incident
            else:
                today = timezone.datetime(day=downtime.created_time.day, month=downtime.created_time.month, year=downtime.created_time.year, tzinfo=ZoneInfo("UTC")) 
                if timezone.now().date() == today.date():
                    time_of_incident = timezone.now() - downtime.created_time
                    time_of_incident = time_of_incident.total_seconds()*1000
                else:
                    time_of_incident = (today + td(days=1)) - downtime.created_time
                    time_of_incident = time_of_incident.total_seconds()*1000
                incident_time += time_of_incident
        if downtimes_end:
            downtime_end = downtimes_end[0]
            no_uptime = events.filter(created_time__lt=downtime_end.created_time, failure_start=True)
            if not no_uptime:
                start_of_day = timezone.datetime(day=downtime_end.created_time.day, month=downtime_end.created_time.month, year=downtime_end.created_time.year, tzinfo=ZoneInfo("UTC")) 
                time_of_incident = downtime_end.created_time - start_of_day
                time_of_incident = time_of_incident.total_seconds()*1000
                incident_time += time_of_incident
        uptime = (incident_time*100)/86400000 #total milliseconds in a day
        uptime = round(100-uptime, 2)
        return uptime
    else:
        if events.count() == events.filter(is_success=False).count():
            return 0
        else:
            return 100

# def filter_events_by_date(events, date):
#     date_start = timezone.datetime(year=date.year, month=date.month, day=date.day, tzinfo=ZoneInfo("UTC"))
#     date_end = date_start + td(days=1)
#     events = events.filter(created_time__gte=date_start, created_time__lt=date_end)
#     response =  calculate_response(events) if events else None
#     uptime = calculate_uptime(events) if events else None
#     return response, uptime

def calculate_response_percentage(responses):
    max_response = max(map(lambda x: x["value"], responses))
    for response in responses:
        response["percentage"] = calculate_percentage(response["value"], max_response)

def build_responses_time(events, date):
    response = calculate_response(events)
    if response or response == 0:
        response = {
            "date": get_verbose_date(date),
            "value": response
        }
    uptime = calculate_uptime(events)
    if uptime or uptime == 0:
        uptime = {
            "date": get_verbose_date(date),
            "value": uptime
        }
    # calculate_response_percentage(response)
    return response, uptime

def calculate_mean(array):
    total = 0
    for x in array:
        total += x
    return total/len(array)

def round_monitor_results(data):
    data["uptime_week"] = round(data["uptime_week"], 2)
    data["uptime_month"] = round(data["uptime_month"], 2)
    data["uptime_ninty"] = round(data["uptime_ninty"], 2)
    data["response_week"] = round(data["response_week"], 2)
    data["response_month"] = round(data["response_month"], 2)
    data["response_ninty"] = round(data["response_ninty"], 2)

def create_monitor_data(monitor, date):
    today_start_date = timezone.datetime(year=date.year, day=date.day, month=date.month, tzinfo=ZoneInfo("UTC"))
    today_end_date = today_start_date + td(days=1)
    monitor_events = MonitorEvent.objects.filter(monitor=monitor, created_time__gte=today_start_date, created_time__lt=today_end_date)
    response, uptime = build_responses_time(monitor_events, date)
    return response, uptime