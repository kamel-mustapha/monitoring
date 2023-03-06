
from django.urls import path
from api.views import *


urlpatterns = [
    path('monitor', Monitoring.as_view(), name="monitors"),
    path('event', Event.as_view(), name="events"),
    path('pause-monitor', pause_monitor),
    path('start-monitor', start_monitor),
    path('notification', Notifications.as_view()),
    path('create-user-page', create_user_page),
    path('get-pages', get_pages),
    path('get-user-pages/', get_user_pages),
    path('monitor-page-stats/', monitor_page_stats),
    path('get-user-details', get_user_details)
]
