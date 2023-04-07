import requests
import json

url = 'https://ikm2evu584.execute-api.us-east-1.amazonaws.com/test/mp11-autograder'

payload = {
			"submitterEmail": "qinq2@illinois.edu", # <insert your coursera account email>,
			"secret": "b40pOlqE27BQwsgs", # <insert your secret token from coursera>,
			# "partId" : "G6U3L"
			"dbApi": "https://qvmfrch9w5.execute-api.us-east-1.amazonaws.com/post_test"
		}
print(json.dumps(payload))
r = requests.post(url, data=json.dumps(payload))

print(r.status_code, r.reason)
print(r.text)
