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
    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_success = models.BooleanField(default=False)
    failure_start = models.BooleanField(default=False)
    
    def __str__(self):
        return self.status
    
    class Meta:
        db_table = "Events"


class UserPage(models.Model):
    def personal_image_filename(self, filename):
        return f'userpages/{self.user.id}/{self.href_link}/{filename}'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, blank=True, null=True)
    monitors = models.ManyToManyField(Monitor, through="PageMonitors")
    name = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    href_link = models.CharField(max_length=300, blank=True, null=True)
    icon_link = models.ImageField(upload_to=personal_image_filename, blank=True, null=True)

    class Meta:
        db_table = "UserPage"


class PageMonitors(models.Model):
    user_page = models.ForeignKey(UserPage, on_delete=models.CASCADE)
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "MTM_UserPageMonitors"