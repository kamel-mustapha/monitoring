from django.http import JsonResponse
from api.models import *
from api.common import *

# logging
from logging import getLogger
logger = getLogger(__name__)

def index(req):
    res = {
        "status": 500
    }
    try:
        req_data = req.GET
        monitor = Monitor.objects.get(id=int(req_data.get("monitor_id")))
        alert_emails = list(monitor.alert_emails.all().values_list("email" , flat=True))
        if monitor.type == "http":
            monitor_http(monitor.id, monitor.link, monitor.success_status, monitor.timeout, alert_emails, repeat=monitor.interval, creator=monitor.user, verbose_name=monitor.name)
        res["status"] = 200    
    except Exception as e:
        logger.exception(e)
    return JsonResponse(res, status=res.get("status"))