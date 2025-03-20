# OpenWeather Data Pipeline

## Overview
This project ingests weather data from OpenWeather API, streams it into AWS Kinesis, processes it in Databricks, and visualizes it in Power BI/Tableau.

## Architecture
1. **AWS Lambda** fetches weather data from OpenWeather API.
2. **AWS Kinesis** streams real-time weather data.
3. **Databricks** processes and stores data in Delta Tables.
4. **DBT** transforms the data.
5. **Power BI/Tableau** visualizes the data.

## Deployment
Run GitHub Actions to deploy:
