import json
import boto3


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    tableDistance = dynamodb.Table('Distance')
    # if event['invocationSource'] == 'FulfillmentCodeHook':
    source = event['currentIntent']['slots']['source']
    destination = event['currentIntent']['slots']['destination']

    result = tableDistance.get_item(Key={'source': source, 'destination': destination})
    distance = result['Item']['distance']

    return {
        'sessionAttributes': event['sessionAttributes'],
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': str(distance)
            }
        }
    }
# this is can return the log to lex bot to check otherwise use cloudwatch
#     return {
#           "dialogAction": {
#               "type": "Close",
#               "fulfillmentState": "Fulfilled",
#               "message": {
#                   "contentType": "SSML",
#                   "content": str(event)
#               },
#           }
#       }
