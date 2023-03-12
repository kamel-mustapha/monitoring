import json, datetime
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
from django.utils import timezone
from payment.models import Plan, APIKey

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
                                user_plan = Plan.objects.filter(name=req.user.sub)[0]
                                user_monitors = Monitor.objects.filter(user=req.user)
                                if user_monitors.count() >= user_plan.monitors:
                                        req.res["status"] = 200
                                        req.res["message"] = "you have reached the maximum monitors, upgrade to get more"
                                else:
                                        data = json.loads(req.body)
                                        if validate_entry(
                                                data, 
                                                ["name", "link", "interval", "alert_emails", "success_status", "timeout"]
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
        
        def put(self, req, *args, **kwargs):
                try:
                        data = json.loads(req.body)
                        monitor = Monitor.objects.filter(id=int(data.get("monitor")))
                        if monitor:
                                monitor = monitor[0]
                                delete_task(monitor)
                                for email in monitor.alert_emails.all():
                                        monitor.alert_emails.remove(email)
                                for email in data.get("alert_emails"):
                                        alert_email = AlertEmail.objects.get_or_create(email=str(email).lower().strip())
                                        monitor.alert_emails.add(alert_email[0])
                                monitor.name = data.get("name")
                                monitor.link = data.get("link")
                                monitor.interval = data.get("interval")
                                monitor.status = data.get("success_status")
                                monitor.timeout = data.get("timeout")
                                monitor.save()
                                start_task(monitor)
                                req.res["status"] = 200
                                req.res["message"] = "success"
                except Exception as e:
                        logger.exception(e)
                return JsonResponse(req.res, status=req.res["status"])
        
        
        def delete(self, req, *args, **kwargs):
                try:
                        data = json.loads(req.body)
                        monitor = Monitor.objects.filter(id=int(data.get("monitor")))
                        if monitor:
                                monitor = monitor[0]
                                delete_task(monitor)
                                monitor.delete()
                                req.res["status"] = 200
                                req.res["message"] = "success"
                except Exception as e:
                        logger.exception(e)
                return JsonResponse(req.res, status=req.res["status"])

@method_decorator(csrf_exempt, name='dispatch')
class Event(View):
        def get(self, req, *args, **kwargs):
                try:
                        if req.user.is_authenticated:
                                data = req.GET
                                monitor_events = MonitorEvent.objects.filter(monitor_id=int(data.get("monitor"))).order_by("-id")
                                for event in monitor_events:
                                        event.created_time = get_verbose_datetime(event.created_time)
                                events_data = EventData(monitor_events, many=True)
                                if events_data.data:
                                        req.res["events"] = events_data.data[:1000]
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
        return JsonResponse(req.res, status=req.res["status"])

def start_monitor(req):
        data = req.GET
        monitor = Monitor.objects.filter(id=int(data.get("monitor")))
        if monitor:
                monitor = monitor[0]
                start_task(monitor)
                monitor.running = True
                monitor.save()
                req.res["status"] = 200
                req.res["message"] = "success"
        return JsonResponse(req.res, status=req.res["status"])


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
                return JsonResponse(req.res, status=req.res["status"])
        def put(self, req):
                data = json.loads(req.body)
                notifications = Notification.objects.filter(id__in=data.get("ids"))
                for notification in notifications:
                        notification.seen_by.add(req.user)
                req.res["status"] = 200
                req.res["message"] = "success"
                return JsonResponse(req.res, status=req.res["status"])

        def delete(self, req):
                data = json.loads(req.body)
                notifications = Notification.objects.filter(id__in=data.get("ids"))
                for notification in notifications:
                        notification.deleted_by.add(req.user)
                req.res["status"] = 200
                req.res["message"] = "success"
                return JsonResponse(req.res, status=req.res["status"])

def get_pages(req):
        try:
                pages = Page.objects.all()
                pages_serial = PagesData(pages, many=True)
                req.res["pages"] = pages_serial.data
                req.res["status"] = 200
                req.res["message"] = "success"
        except Exception as e:
                logger.exception(e)
        return JsonResponse(req.res, status=req.res["status"])

@method_decorator(csrf_exempt, name='dispatch')
class UserPages(View):
        def get(self, req, *args, **kwargs):
                try:
                        pages = UserPage.objects.filter(user=req.user).annotate(monitors_nb=Count('monitors'))
                        # pages_serial = UserPageData(pages, many=True)
                        req.res["pages"] = list(pages.values('id', 'name', 'link', 'seen', 'title', 'monitors_nb'))
                        req.res["status"] = 200
                        req.res["message"] = "success"
                except Exception as e:
                        logger.exception(e)
                return JsonResponse(req.res, status=req.res["status"])
        def post(self, req, *args, **kwargs):
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
                                user_page.icon_link = files.get('image')
                        user_page.save()
                        if data.get("monitors"):
                                monitors_ids = data.get("monitors").split(",")
                                for monitor in monitors_ids:
                                        monitor = Monitor.objects.get(id=int(monitor.strip()))
                                        user_page.monitors.add(monitor)
                        user_page.link = f"/monitor/{user_page.id}"
                        user_page.save()
                        req.res["message"] = "success"
                        req.res["status"] = 200
                except Exception as e:
                        print(e)
                return JsonResponse(req.res, status=req.res["status"])
        def delete(self, req, *args, **kwargs):
                try:
                        data = json.loads(req.body)
                        page = UserPage.objects.filter(id=int(data.get("page")))
                        if page:
                                page = page[0]
                                page.delete()
                                req.res["status"] = 200
                                req.res["message"] = "success"
                except Exception as e:
                        logger.exception(e)
                return JsonResponse(req.res, status=req.res["status"])

@csrf_exempt
def monitor_page_stats(req):
        try:
                data = req.GET
                page = UserPage.objects.filter(id=int(data.get("id")))
                if page:
                        page = page[0]
                        req.res["monitors"] = []
                        page_monitors = page.monitors.all()
                        for monitor in page_monitors:
                                three_month_date = timezone.now() - datetime.timedelta(days=90)
                                monitor_events = MonitorEvent.objects.filter(monitor=monitor, created_time__gte=three_month_date).order_by("id")
                                monitor_data = create_monitor_data(monitor, monitor_events, 90)
                                req.res["monitors"].append(monitor_data)
                        print(req.res)
                        req.res["status"] = 200
                        del req.res["message"]
        except Exception as e:
                logger.exception(e)
        return JsonResponse(req.res, status=req.res["status"])



def get_user_details(req):
        try:
                if req.user.is_authenticated:
                        user_monitors = Monitor.objects.filter(user=req.user).count()
                        user_plan = Plan.objects.filter(name=req.user.sub, period=req.user.period)[0]
                        req.res["user"] = {
                                "username": req.user.username,
                                "email": req.user.email,
                                "api_key": req.user.api_key,
                                "sub": req.user.sub,
                                "monitors": user_monitors,
                                "max_monitors": user_plan.monitors,
                                "usage": (user_monitors*100)/user_plan.monitors,
                                "payment_card": req.user.card_last_digit,
                                "min_interval": user_plan.interval,
                                "max_alert_emails": user_plan.alert_emails,
                                "stripe_public": APIKey.objects.filter(active=True)[0].public
                        }
                        req.res["status"] = 200
                        req.res["message"] = "success"
        except Exception as e:
                logger.exception(e)
        return JsonResponse(req.res, status=req.res["status"])