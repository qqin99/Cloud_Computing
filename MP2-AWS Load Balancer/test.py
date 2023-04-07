import requests
import json

url = 'https://seorwrpmwh.execute-api.us-east-1.amazonaws.com/prod/mp2-autograder-2022-spring'

payload = {
		'ip_address1':  '18.206.232.101:5000', # <insert ip address:port of first EC2 instance>,
		'ip_address2':  '34.232.77.169:5000', # <insert ip address:port of second EC2 instance>,
		'load_balancer':  'mp2-80-1630334045.us-east-1.elb.amazonaws.com',# <insert address of load balancer>,
		'submitterEmail': 'qinq2@illinois.edu', # <insert your coursera account email>,
		'secret': 'hzlZ5753tlLx73SU' # <insert your secret token from coursera>
		}

r = requests.post(url, data=json.dumps(payload))

print(r.status_code, r.reason)
print(r.text)