from rest_framework import serializers
from api.models import *
from website.models import Notification



class MonitorData(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ('id', 'name', 'type', 'link', 'interval', 'alert_emails', 'running')
        depth = 1

class EventData(serializers.ModelSerializer):
    class Meta:
        model = MonitorEvent
        fields = ('id', 'monitor', 'status', 'time', 'message', 'created_time', 'is_success')


