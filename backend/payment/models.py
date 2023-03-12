from django.db import models

class Plan(models.Model):
    PLANS = (
        ("Free", "Free"),
        ("Pro", "Pro"),
        ("Business", "Business")
    )
    PERIODS = (
        ("monthly", "Monthly"),
        ("annually", "Annually")
    )
    stripe_id = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=20, choices=PLANS)
    period = models.CharField(max_length=20, choices=PERIODS)
    price = models.FloatField(default=0)
    monitors = models.IntegerField(default=5)
    interval = models.IntegerField(default=300)
    page = models.IntegerField(default=1)
    alert_emails = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return f"{self.name} - {self.period}"
    

class APIKey(models.Model):
    private = models.CharField(max_length=300)
    public = models.CharField(max_length=300)
    active = models.BooleanField(default=True)