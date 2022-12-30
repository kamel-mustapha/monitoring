import requests, threading, time, multiprocessing
from api.models import Monitor
from task.models import Task


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