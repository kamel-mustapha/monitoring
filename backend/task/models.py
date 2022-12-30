from django.db import models


class Task(models.Model):
    verbose_name = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = "background_task"
   