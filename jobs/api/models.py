from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name='username')

    class Meta:
        db_table = "User"

class Monitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    link = models.CharField(max_length=255)
    interval = models.IntegerField(default=30)
    alert_emails = models.ManyToManyField("AlertEmail", through="MonitorAlertEmail")
    running = models.BooleanField(default=False)
    success_status = models.IntegerField(null=True, blank=True)
    timeout = models.IntegerField(default=30)
    
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


class MonitorEvent(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE)
    status = models.IntegerField(null=True, blank=True)
    time = models.FloatField(null=True, blank=True)
    message = models.CharField(max_length=300)
    created_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    is_success = models.BooleanField(default=False)
    failure_start = models.BooleanField(default=False)
    failure_end = models.BooleanField(default=False)
    
    def __str__(self):
        return self.status
    
    class Meta:
        db_table = "Events"


