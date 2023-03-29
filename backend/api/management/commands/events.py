from django.core.management.base import BaseCommand
from api.models import *
from api.common import *
from django.utils import timezone
from datetime import datetime, timedelta

class Command(BaseCommand):
    def handle(self, *args, **options):
        monitors = Monitor.objects.all()
        now = timezone.now()
        yesterday = now - timedelta(days=1)
        for monitor in monitors:
            response, uptime = create_monitor_data(monitor, yesterday)
            if response.get("value") and uptime.get("value"):
                stat, created = EventStats.objects.get_or_create(
                    monitor=monitor,
                    date=yesterday
                )
                stat.uptime = uptime.get("value")
                stat.response = response.get("value")
                stat.save()