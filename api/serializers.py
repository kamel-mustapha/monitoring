from rest_framework import serializers
from api.models import *

class MonitorData(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        fields = ('__all__',)