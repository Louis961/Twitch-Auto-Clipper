import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PeakFinder')
response = table.scan()
data = response['Items']

def lambda_handler(event, context):
    if event:
        #Constucting the response to the HTML
        responseObject = {}
        responseObject['statusCode'] = 200
        responseObject['headers'] = {}
        responseObject['headers']['Content-Type'] = 'application/json'
        responseObject['body'] = json.dumps(data)
            
            #Returning the response object 
        return responseObject
