from django.db import models


class Monitor(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    link = models.CharField(max_length=255)
    page = models.ForeignKey("Page", on_delete=models.SET_NULL, null=True)
    interval = models.IntegerField(default=30)
    alert_emails = models.ManyToManyField("AlertEmail", through="MonitorAlertEmail")
    def __str__(self):
        return self.name

class Page(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class AlertEmail(models.Model):
    email = models.CharField(max_length=150)
    def __str__(self):
        return self.email
        
class MonitorAlertEmail(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    alert_email = models.ForeignKey(AlertEmail, on_delete=models.CASCADE)