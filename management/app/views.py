import threading, time, prctl, os
from django.shortcuts import render
from django.http import JsonResponse
from app.models import *
from django.conf import settings


# logging
from logging import getLogger
logger = getLogger(__name__)


def monitor_thread(monitor):
    try:
        prctl.set_name(f"monitor:{str(monitor.id)}")
        while True:
            try:
                # r = requests.get(monitor.link)
                logger.info(monitor.id)
                # if r:
                #     print(r.status_code)
                time.sleep(monitor.interval)
            except:
                logger.exception(e)
    except Exception as e:
        logger.exception(e)


def index(req):
    res = {}
    try:
        command = os.system(f"ps -T > {settings.BASE_DIR}/threads.txt")
        with open(f"{settings.BASE_DIR}/threads.txt", "r") as f:
            f = f.read()
            print(f.split("\n"))
        monitors = Monitor.objects.all()
        for monitor in monitors:
            t = threading.Thread(name=monitor.id, target=monitor_thread, args=(monitor,))
            t.start()
        res["status"] = 200
    except Exception as e:
        logger.exception(e)

    return JsonResponse(res)
