import json
from django.shortcuts import render
from django.views.generic import View
from api.serializers import *
from api.models import *
from rest_framework.response import Response
from django.http import JsonResponse
from api.common import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from website.models import Notification
from django.db.models import Q
from django.db.models import Count

from logging import getLogger
logger = getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class Monitoring(View):
        def get(self, req, *args, **kwargs):
                try:
                        if req.user.is_authenticated:
                                user_monitors = Monitor.objects.filter(user=req.user).order_by("-id")
                                monitors_data = MonitorData(user_monitors, many=True)
                                if monitors_data.data:
                                        req.res["monitors"] = monitors_data.data
                                        req.res["message"] = "success"
                                else:
                                        req.res["message"] = "you have no monitors"
                                req.res["status"] = 200
                except Exception as e:
                        logger.exception(e)
                return JsonResponse(req.res, status=req.res["status"])

        
        def post(self, req, *args, **kwargs):
                try:
                        if req.user.is_authenticated:
                                data = json.loads(req.body)
                                if validate_entry(
                                        data, 
                                        ["name", "type", "link", "interval", "alert_emails", "success_status", "timeout"]
                                        ):
                                        monitor = Monitor.objects.create(
                                                user=req.user,
                                                name=data.get("name"),
                                                type="http",
                                                # type=data.get("type"),
                                                link=data.get("link"),
                                                interval=data.get("interval"), 
                                                success_status=data.get("success_status"),
                                                timeout=data.get("timeout"),
                                                running=True
                                        )
                                        if data.get("alert_emails"):
                                                for email in data.get("alert_emails"):
                                                        alert_email = AlertEmail.objects.get_or_create(email=str(email).lower().strip())
                                                        monitor.alert_emails.add(alert_email[0])
                                        else:
                                                alert_email = AlertEmail.objects.get_or_create(email=req.user.email.lower().strip())
                                                monitor.alert_emails.add(alert_email[0])
                                        if monitor:
                                                monitor_data = MonitorData(monitor)
                                                req.res["monitor"] = monitor_data.data
                                                req.res["status"] = 200
                                                req.res["message"] = "success"
                                                start_task(monitor)
                except Exception as e: 
                        logger.exception(e)
                return JsonResponse(req.res, status=req.res["status"])
        def delete(self, req, *args, **kwargs):
                data = json.loads(req.body)
                monitor = Monitor.objects.filter(id=int(data.get("monitor")))
                if monitor:
                        monitor = monitor[0]
                        delete_task(monitor)
                        monitor.delete()
                        req.res["status"] = 200
                        req.res["message"] = "success"
                return JsonResponse(req.res, status=req.res["status"])

@method_decorator(csrf_exempt, name='dispatch')
class Event(View):
        def get(self, req, *args, **kwargs):
                try:
                        if req.user.is_authenticated:
                                data = req.GET
                                monitor_events = MonitorEvent.objects.filter(monitor_id=int(data.get("monitor"))).order_by("-id")
                                events_data = EventData(monitor_events, many=True)
                                if events_data.data:
                                        req.res["events"] = events_data.data
                                        req.res["message"] = "success"
                                else:
                                        req.res["events"] = []
                                        req.res["message"] = "no events found for this monitor"
                                req.res["status"] = 200
                except Exception as e:
                        logger.exception(e)
                return JsonResponse(req.res, status=req.res["status"])


def pause_monitor(req):
        data = req.GET
        monitor = Monitor.objects.filter(id=int(data.get("monitor")))
        if monitor:
                monitor = monitor[0]
                delete_task(monitor)
                monitor.running = False
                monitor.save()
                req.res["status"] = 200
                req.res["message"] = "success"
        return JsonResponse(req.res)

def start_monitor(req):
        data = req.GET
        print(data)
        monitor = Monitor.objects.filter(id=int(data.get("monitor")))
        if monitor:
                monitor = monitor[0]
                start_task(monitor)
                monitor.running = True
                monitor.save()
                req.res["status"] = 200
                req.res["message"] = "success"
        return JsonResponse(req.res)


@method_decorator(csrf_exempt, name='dispatch')
class Notifications(View):
        def get(self, req):
                notifications = Notification.objects.filter(Q(user=req.user) | Q(for_all=True)).order_by("-id")
                req.res["notifications"] = []
                for notification in notifications:
                        if req.user not in notification.deleted_by.all():
                                notification_object = {
                                        "id": notification.id,
                                        "title": notification.title,
                                        "text": notification.text,
                                        "image": notification.image,
                                        "seen": True if req.user in notification.seen_by.all() else False
                                }
                                req.res["notifications"].append(notification_object)
                req.res["status"] = 200
                req.res["message"] = "success"
                return JsonResponse(req.res)
        def put(self, req):
                data = json.loads(req.body)
                notifications = Notification.objects.filter(id__in=data.get("ids"))
                for notification in notifications:
                        notification.seen_by.add(req.user)
                req.res["status"] = 200
                req.res["message"] = "success"
                return JsonResponse(req.res)

        def delete(self, req):
                data = json.loads(req.body)
                notifications = Notification.objects.filter(id__in=data.get("ids"))
                for notification in notifications:
                        notification.deleted_by.add(req.user)
                req.res["status"] = 200
                req.res["message"] = "success"
                return JsonResponse(req.res)
        
@csrf_exempt
def create_user_page(req):
        if req.method == "POST":
                try:
                        data = req.POST
                        files = req.FILES
                        user_page = UserPage(
                                user=req.user,
                                page_id=int(data.get('page_id')),
                                name=data.get('name'),
                                title=data.get('title'),
                                href_link=data.get('link'),
                        )
                        if files:
                                # files['image'] = "ss.jpg"
                                print(files.get('image'))
                                user_page.icon_link = files.get('image')
                        user_page.save()
                        if data.get("monitors"):
                                monitors_ids = data.get("monitors").split(",")
                                for monitor in monitors_ids:
                                        monitor = Monitor.objects.get(id=int(monitor.strip()))
                                        user_page.monitors.add(monitor)
                        req.res["message"] = "success"
                        req.res["status"] = 200
                except Exception as e:
                        print(e)
        return JsonResponse(req.res)


def get_pages(req):
        try:
                pages = Page.objects.all()
                pages_serial = PagesData(pages, many=True)
                req.res["pages"] = pages_serial.data
                req.res["status"] = 200
                req.res["message"] = "success"
        except Exception as e:
                logger.exception(e)
        return JsonResponse(req.res)

def get_user_pages(req):
        try:
                pages = UserPage.objects.filter(user=req.user).annotate(monitors_nb=Count('monitors'))
                # pages_serial = UserPageData(pages, many=True)
                req.res["pages"] = list(pages.values('id', 'name', 'href_link', 'seen', 'title', 'monitors_nb'))
                req.res["status"] = 200
                req.res["message"] = "success"
        except Exception as e:
                logger.exception(e)
        return JsonResponse(req.res)



@csrf_exempt
def monitor_page_stats(req):
        req.res["status"] = 200
        req.res["monitors"] = [
                {
                "id": 0,
                "name": 'API',
                "uptime_day": 95,
                "uptime_week": 97,
                "uptime_month": 98,
                "response_day": 400,
                "response_week": 540,
                "response_month": 450,
                "max_response_time": 500,
                "uptimes": [
                        { "date": '21 Feb 2023', "value": 100 },
                        { "date": '21 Feb 2023', "value": 98 },
                ],
                "responses": [
                        {
                        "date": '21 Feb 2023',
                        "value": 500,
                          "percentage": calculate_percentage(500, 500),
                        },
                        {
                        "date": '21 Feb 2023',
                        "value": 250,
                          "percentage": calculate_percentage(250, 500),
                        },
                        {
                        "date": '21 Feb 2023',
                        "value": 400,
                          "percentage": calculate_percentage(400, 500),
                        },
                ],
                },
        ]
        return JsonResponse(req.res)

