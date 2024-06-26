import requests
import json
import time

proxies = {'https':"http://disrct:etsps2024401@10.224.200.26:8080"}

FIREBASE_URL = "https://iiot-7276b-default-rtdb.firebaseio.com/Amilton.json"

while True:
    data = json.loads(requests.get(FIREBASE_URL, proxies=proxies).content)

    print(data)

    time.sleep(1)
