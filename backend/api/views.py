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


from logging import getLogger
logger = getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class Monitoring(View):
        def get(self, req, *args, **kwargs):
                try:
                        if req.user.is_authenticated:
                                user_monitors = Monitor.objects.filter(user=req.user)
                                monitors_data = MonitorData(user_monitors, many=True)
                                if monitors_data.data:
                                        req.res["monitors"] = monitors_data.data
                                        req.res["status"] = 200
                                        req.res["message"] = "success"
                                else:
                                        req.res["status"] = 404
                                        req.res["message"] = "you have no monitors"
                except: pass
                return JsonResponse(req.res, status=req.res["status"])

        
        def post(self, req, *args, **kwargs):
                try:
                        if req.user.is_authenticated:
                                data = json.loads(req.body)
                                if validate_entry(
                                        data, 
                                        ["name", "type", "link", "page", "interval", "alert_emails", "success_status", "timeout"]
                                        ):
                                        page_id = data.get("page") if data.get("page") and type(data.get("page")) == int else int(data.get("page"))
                                        monitor = Monitor.objects.create(
                                                user=req.user,
                                                name=data.get("name"),
                                                type=data.get("type"),
                                                link=data.get("link"),
                                                page=Page.objects.get(id=page_id),
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
                                                r = requests.get(f"http://jobs:8000/create-task?monitor_id={monitor.id}")
                                                if r and r.status_code == 200:
                                                        logger.info(f"Created job for monitor {monitor.id}")
                except Exception as e: print(e)
                return JsonResponse(req.res, status=req.res["status"])
