import json
import boto3
import requests
import os

# AWS Kinesis Config
KINESIS_STREAM = "openweather-kinesis-stream"
REGION = "eu-north-1"

# OpenWeather API Config
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
DEFAULT_CITY = "Maiduguri"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# AWS Clients
kinesis_client = boto3.client("kinesis", region_name=REGION)

def get_weather_data(city):
    """Fetch weather data from OpenWeather API."""
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "timestamp": data["dt"]
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def send_to_kinesis(data):
    """Send data to Kinesis stream."""
    try:
        response = kinesis_client.put_record(
            StreamName=KINESIS_STREAM,
            Data=json.dumps(data),
            PartitionKey="weather_data"
        )
        return response
    except Exception as e:
        print(f"Error sending data to Kinesis: {e}")
        return None

def lambda_handler(event, context):
    """AWS Lambda entry point."""
    city = event.get("city", DEFAULT_CITY)
    weather_data = get_weather_data(city)

    if weather_data:
        send_to_kinesis(weather_data)
        return {"statusCode": 200, "body": json.dumps("Data sent to Kinesis")}
    else:
        return {"statusCode": 500, "body": json.dumps("Failed to fetch weather data")}
