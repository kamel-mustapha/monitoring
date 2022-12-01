import requests, time
from django.db import models
from website.models import User
from django.dispatch import receiver


from logging import getLogger
logger = getLogger(__name__)

class Monitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    link = models.CharField(max_length=255)
    interval = models.IntegerField(default=300)
    alert_emails = models.ManyToManyField("AlertEmail", through="MonitorAlertEmail")
    running = models.BooleanField(default=False)
    success_status = models.IntegerField(default=200)
    timeout = models.IntegerField(default=30)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "Monitors"

# @receiver(models.signals.post_save, sender = Monitor)
# def monitor_created(sender, instance, created, **kwargs):
#     try:
#         if created:
#             instance.save()
#             r = requests.get(f"http://jobs:8000/create-task?monitor_id={instance.id}")
#             if r and r.status_code == 200:
#                 logger.info(f"Created job for monitor {instance.id}")
#     except Exception as e:
#         logger.exception(e)

class Page(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "Pages"

class AlertEmail(models.Model):
    email = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "AlertEmails"

class MonitorAlertEmail(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    alert_email = models.ForeignKey(AlertEmail, on_delete=models.CASCADE)

    def __str__(self):
        return self.alert_email

    class Meta:
        db_table = "MTM_MonitorsAlertEmails"

class MonitorEvent(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    status = models.IntegerField(null=True, blank=True)
    time = models.FloatField(null=True, blank=True)
    message = models.CharField(max_length=300)

    def __str__(self):
        return self.status
    
    class Meta:
        db_table = "Events"