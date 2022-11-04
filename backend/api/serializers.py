from rest_framework import serializers
from api.models import *

class MonitorData(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ('id', 'name', 'type', 'link', 'page', 'interval', 'alert_emails')
        depth = 1