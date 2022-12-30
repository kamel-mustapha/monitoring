from rest_framework import serializers
from api.models import *

class MonitorData(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ('id', 'name', 'type', 'link', 'interval', 'alert_emails')
        depth = 1

class EventData(serializers.ModelSerializer):
    class Meta:
        model = MonitorEvent
        fields = ('id', 'monitor', 'status', 'time', 'message', 'created_time', 'is_success')