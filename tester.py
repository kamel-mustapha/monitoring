import requests
import time

while True:
    try:
        req_start = time.time()
        r = requests.get("http://127.0.0.1:8000/api/monitor")
        req_end = time.time()
        if(r.status_code == 200):
            print(r.status_code, (req_end - req_start)*1000)
        else:
            print(f"error {r.status_code}")
        time.sleep(2)
    except:
        print(f"Server unreachable")