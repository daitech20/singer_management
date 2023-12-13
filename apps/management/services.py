# -*- coding: utf-8 -*-
import http.client
import json

api_notify = "https://exp.host/--/api/v2/push/send"
headers = {
    'Accept-encoding': 'gzip, deflate',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def send_notify(expoPushToken, message):
    conn = http.client.HTTPSConnection("exp.host")
    payload = json.dumps({
        "to": expoPushToken,
        "sound": "default",
        "title": "Bạn có lịch trình diễn sắp tới",
        "body": message,
        "data": {
            "abc": "1122"
        }
    })

    conn.request("POST", "/--/api/v2/push/send", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
