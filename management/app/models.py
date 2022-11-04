import uuid, hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)
    api_key = models.CharField(max_length=200, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = hashlib.md5(f"{self.email}{self.username}{self.password}".encode()).hexdigest()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "User"


class Monitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    link = models.CharField(max_length=255)
    page = models.ForeignKey("Page", on_delete=models.SET_NULL, null=True)
    interval = models.IntegerField(default=30)
    alert_emails = models.ManyToManyField("AlertEmail", through="MonitorAlertEmail")
    running = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Monitors"

class Page(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = "Pages"

class AlertEmail(models.Model):
    email = models.CharField(max_length=150)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "AlertEmails"

class MonitorAlertEmail(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    alert_email = models.ForeignKey(AlertEmail, on_delete=models.CASCADE)

    class Meta:
        db_table = "MTM_MonitorsAlertEmails"