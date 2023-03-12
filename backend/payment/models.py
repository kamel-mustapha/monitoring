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
    
    def __str__(self) -> str:
        return f"{self.name} - {self.period}"