# -*- coding: utf-8 -*-
import http.client
import json

api_notify = "https://exp.host/--/api/v2/push/send"
headers = {
    'Accept-encoding': 'gzip, deflate',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def send_notify(expoPushToken):
    conn = http.client.HTTPSConnection("exp.host")
    payload = json.dumps({
        "to": expoPushToken,
        "sound": "default",
        "title": "Ban co lich trinh dien sap toi",
        "body": "Ban co lich trinh dien sap toi",
        "data": {
            "abc": "1122"
        }
    })

    conn.request("POST", "/--/api/v2/push/send", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
