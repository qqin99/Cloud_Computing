import requests
import json
url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp12-grader"
payload = {
            "accountId": 123455100654,
            "submitterEmail": 'qinq2@illinois.edu',
            "secret": 'GDYk38EC5U0tE9WS',
            "ipaddress": '3.235.141.208:5000'
    }
r = requests.post(url, data=json.dumps(payload))
print(r.status_code, r.reason)
print(r.text)
