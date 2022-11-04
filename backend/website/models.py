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

class Activation(models.Model):
    code = models.CharField(max_length=200, default=uuid.uuid4)
    used = models.BooleanField(default = False)

    class Meta:
        db_table = "Activation"
