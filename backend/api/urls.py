
from django.urls import path
from api.views import *


urlpatterns = [
    path('monitor', Monitoring.as_view(), name="monitors"),
]
