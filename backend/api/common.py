import requests, threading, time, multiprocessing
from api.models import Monitor
from task.models import Task
from django.utils import timezone
from datetime import timedelta as td
from zoneinfo import ZoneInfo

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
    response = int(response_time/events.count()) if events else 0
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
        return 100

def filter_events_by_date(events, date):
    date_start = timezone.datetime(year=date.year, month=date.month, day=date.day, tzinfo=ZoneInfo("UTC"))
    date_end = date_start + td(days=1)
    events = events.filter(created_time__gte=date_start, created_time__lt=date_end)
    response =  calculate_response(events)
    uptime = calculate_uptime(events) if events else None
    return response, uptime

def calculate_response_percentage(responses):
    max_response = max(map(lambda x: x["value"], responses))
    for response in responses:
        response["percentage"] = calculate_percentage(response["value"], max_response)

def build_responses_time(events, event_time, today):
    responses = []
    uptimes = []
    for event_day in range(event_time):
        response, uptime = filter_events_by_date(events, today-td(days=event_day))
        if response:
            responses.append({
                "date": get_verbose_date(today-td(days=event_day)),
                "value": response
            })
        if uptime:
            uptimes.append({
                "date": get_verbose_date(today-td(days=event_day)),
                "value": uptime
            })
    calculate_response_percentage(responses)
    return responses, uptimes

def calculate_mean(array):
    total = 0
    for x in array:
        total += x
    return total/len(array)

def round_monitor_results(data):
    data["uptime_week"] = round(data["uptime_week"], 2)
    data["uptime_month"] = round(data["uptime_month"], 2)
    data["uptime_ninty"] = round(data["uptime_ninty"], 2)
    data["response_week"] = int(data["response_week"])
    data["response_month"] = int(data["response_month"])
    data["response_ninty"] = int(data["response_ninty"])

def create_monitor_data(monitor, events, events_time):
    today = timezone.datetime.now()
    responses, uptimes = build_responses_time(events, events_time, today)
    data = {
        "name": monitor.name,
        "check_interval": monitor.interval/60,
        "uptimes": uptimes,
        "responses": responses,
    }
    # building stats
    for x in ["uptime", "response"]:
        data[f"{x}_week"] = calculate_mean(list(map(lambda k: k['value'], data[f"{x}s"][:7]))) if len(data[f"{x}s"]) >= 7 else calculate_mean(list(map(lambda k: k['value'], data[f"{x}s"])))
        data[f"{x}_month"] = calculate_mean(list(map(lambda k: k['value'], data[f"{x}s"][:30]))) if len(data[f"{x}s"]) >= 30 else calculate_mean(list(map(lambda k: k['value'], data[f"{x}s"])))
        data[f"{x}_ninty"] = calculate_mean(list(map(lambda k: k['value'], data[f"{x}s"][:90]))) if len(data[f"{x}s"]) >= 90 else calculate_mean(list(map(lambda k: k['value'], data[f"{x}s"])))
    # reversing data for display
    data["responses"].reverse()
    data["uptimes"].reverse()
    # rounding results
    round_monitor_results(data)
    return data