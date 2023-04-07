import requests
import json
import uuid

url = "https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp3-autograder-2022-spring"

payload = {
    "graphApi": "https://nbl89y0cy3.execute-api.us-east-1.amazonaws.com/devmp2/",  # <post api for storing the graph>,
    "botName": "distanceBot",  # <name of your Amazon Lex Bot>,
    "botAlias": "getDistance",  # <alias name given when publishing the bot>,
    "identityPoolId": "us-east-1:dcff0b1f-97a5-4a5f-a745-0faf22876d01",  # <cognito identity pool id for lex>,
    "accountId": "703508104068",  # <your aws account id used for accessing lex>,
    "submitterEmail": "qinq2@illinois.edu",  # <insert your coursera account email>,
    "secret": "Vzp98mSEN0OWcnLU",  # <insert your secret token from coursera>,
    "region": "us-east-1"  # <Region where your lex is deployed (Ex: us-east-1)>
}

r = requests.post(url, data=json.dumps(payload))

print(r.status_code, r.reason)
print(r.text)
