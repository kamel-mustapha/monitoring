import requests, threading, time, multiprocessing
from api.models import Monitor


def validate_entry(entry, validators):
    if all(x in entry for x in validators):
        return True
    return False

def monitor_thread(monitor):
    while True:
        try:
            # r = requests.get(monitor.link)
            print(monitor.id)
            # if r:
            #     print(r.status_code)
            time.sleep(monitor.interval)
        except:
            pass

def launch_monitor(monitor):
    t = threading.Thread(target=monitor_thread, args=(monitor,))
    t.start()


def launch_all_monitors():
    monitors = Monitor.objects.all()
    for monitor in monitors:
        t = threading.Thread(target=monitor_thread, args=(monitor,))
        t.start()