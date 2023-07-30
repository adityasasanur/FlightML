import datetime
import boto3
import csv
import io

# AWS S3 credentials and settings
AWS_REGION_NAME = 'us-east-2'
BUCKET_NAME = 'google-flight-data-db'
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
FOLDER_PATH = tomorrow.strftime("%Y-%m-%d") 

def lambda_handler(event, context):
    s3 = boto3.client('s3', region_name=AWS_REGION_NAME)
    file_names = get_file_names_in_folder(s3, BUCKET_NAME, FOLDER_PATH)
    if not file_names:
        return {
            'statusCode': 200,
            'body': 'No CSV files found in the folder.'
        }


    csv_data = combine_csv_files(s3, BUCKET_NAME, file_names)
    save_combined_csv(s3, BUCKET_NAME, FOLDER_PATH+'combined_file.csv', csv_data)
    return {
        'statusCode': 200,
        'body': 'Combined CSV file created successfully.'
    }

def get_file_names_in_folder(s3_client, bucket, folder_path):
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=folder_path)

    file_names = []
    for obj in response.get('Contents', []):
        key = obj['Key']
        if key.endswith('.csv'):
            file_names.append(key)

    return file_names

def combine_csv_files(s3_client, bucket, file_names):
    csv_data = ["departure_airport_int",
            "arriving_airport_int",
            "departure_time_float",
            "airline_int",
            "date_year",
            "date_month",
            "date_day",
            "date_dow",
            "duration_hours",
            "numStops",
            "price_min_day",
            "price_min",
            "Day 0",
            "Day 1",
            "Day 2",
            "Day 3",
            "Day 4",
            "Day 5",
            "Day 6",
            "Day 7",
            "Day 8",
            "Day 9",
            "Day 10",
            "Day 11",
            "Day 12",
            "Day 13",
            "Day 14",
            "Day 15",
            "Day 16",
            "Day 17",
            "Day 18",
            "Day 19",
            "Day 20",
            "Day 21",
            "Day 22",
            "Day 23",
            "Day 24",
            "Day 25",
            "Day 26",
            "Day 27",
            "Day 28",
            "Day 29",
            "Day 30",
            "Day 31",
            "Day 32",
            "Day 33",
            "Day 34",
            "Day 35",
            "Day 36",
            "Day 37",
            "Day 38",
            "Day 39",
            "Day 40",
            "Day 41",
            "Day 42",
            "Day 43",
            "Day 44",
            "Day 45",
            "Day 46",
            "Day 47",
            "Day 48",
            "Day 49",
            "Day 50",
            "Day 51",
            "Day 52",
            "Day 53",
            "Day 54",
            "Day 55",
            "Day 56",
            "Day 57",
            "Day 58",
            "Day 59",
            "Day 60",
            ]
    for file_name in file_names:
        response = s3_client.get_object(Bucket=bucket, Key=file_name)
        content = response['Body'].read().decode('utf-8')
        content = content.split('\n')[1:]
        content = '\n'.join(content)
        csv_reader = csv.reader(io.StringIO(content))
        csv_data.extend(list(csv_reader))

    return csv_data

def save_combined_csv(s3_client, bucket, combined_file_name, csv_data):
    combined_csv = io.StringIO()
    csv_writer = csv.writer(combined_csv)
    csv_writer.writerows(csv_data)

    s3_client.put_object(Bucket=bucket, Key=combined_file_name, Body=combined_csv.getvalue())
