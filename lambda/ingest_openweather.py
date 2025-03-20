import json
import boto3
import requests
import os

# AWS Kinesis Stream Name
KINESIS_STREAM = "openweather-kinesis-stream"
REGION = "eu-north-1"

# OpenWeather API Config
OPENWEATHER_API_KEY = os.getenv("65dbc86abc7737f40e59113106bc3579")
CITY = "Maiduguri"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}"

# AWS Clients
kinesis_client = boto3.client("kinesis", region_name=REGION)

def lambda_handler(event, context):
    response = requests.get(URL)
    data = response.json()
    
    # Extract necessary fields
    weather_data = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "timestamp": data["dt"]
    }

    # Send data to Kinesis
    kinesis_client.put_record(
        StreamName=KINESIS_STREAM,
        Data=json.dumps(weather_data),
        PartitionKey="weather_data"
    )

    return {"statusCode": 200, "body": json.dumps("Data sent to Kinesis")}
