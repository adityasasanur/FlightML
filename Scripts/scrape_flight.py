import csv
import datetime
import json
import boto3

def lambda_handler(event, context):
    BATCH_SIZE = 10
    client = boto3.client('lambda')

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    with open('flightLinks.csv','r',encoding='utf-8-sig') as csvfile: 
        reader = csv.reader(csvfile, delimiter='\n')
        links = [x[0]+tomorrow.strftime("%Y-%m-%d") for x in reader]

    for i in range(0, len(links), BATCH_SIZE):
        batch = links[i:i+BATCH_SIZE]
        response = client.invoke(
            FunctionName='get_batch_flight_data',
            InvocationType='Event',
            Payload=json.dumps({'links': batch})
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Completed starting lambdas!')
    }