
from django.urls import path
from api.views import *


urlpatterns = [
    path('monitor/', monitors, name="monitors"),
]
