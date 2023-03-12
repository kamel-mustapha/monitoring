import uuid, hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser
from payment.models import Plan

class User(AbstractUser):
    PLANS = (
        ("Free", "Free"),
        ("Pro", "Pro"),
        ("Business", "Business")
    )
    PERIODS = (
        ("monthly", "Monthly"),
        ("annually", "Annually")
    )
    email = models.EmailField(max_length=200, unique=True)
    api_key = models.CharField(max_length=200, unique=True, blank=True, null=True)
    sub = models.CharField(max_length=50, blank=True, null=True, default="Free", choices=PLANS)
    period = models.CharField(max_length=20, choices=PERIODS, default="monthly")
    stripe_id = models.CharField(max_length=200, blank=True, null=True)
    payment_method = models.CharField(max_length=200, blank=True, null=True)
    card_last_digit = models.IntegerField(blank=True, null=True)
    stripe_sub = models.CharField(max_length=200, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = hashlib.md5(f"{self.email}{self.username}{self.password}".encode()).hexdigest()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "User"

class Activation(models.Model):
    code = models.CharField(max_length=200, default=uuid.uuid4)
    used = models.BooleanField(default = False)

    class Meta:
        db_table = "Activation"

class Notification(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="notification_for_user")
    for_all = models.BooleanField(default=False)
    seen_by = models.ManyToManyField(User, through="NotificationUser", related_name="notification_seen_by")
    image = models.CharField(max_length=250, null=True, blank=True)
    deleted_by = models.ManyToManyField(User, through="NotificationUserDeleted", related_name="notification_deleted_by")
    def __str__(self):
        return self.title


    # def seen(self, user):
    #     if user in self.seen_by.all():
    #         return True
    #     else:
    #         return False

    class Meta:
        db_table = "Notification"

class NotificationUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    class Meta:
        db_table = "Notification_Seen"

class NotificationUserDeleted(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    class Meta:
        db_table = "Notification_Deleted"