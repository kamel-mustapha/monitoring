from django.contrib import admin
from api.models import *


admin.site.register(Page)
admin.site.register(Monitor)
admin.site.register(AlertEmail)
admin.site.register(MonitorAlertEmail)