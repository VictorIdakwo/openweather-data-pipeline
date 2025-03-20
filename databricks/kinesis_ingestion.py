from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, FloatType, IntegerType

# Initialize Spark session
spark = SparkSession.builder.appName("OpenWeatherKinesisIngestion").getOrCreate()

# Define Kinesis Stream
STREAM_NAME = "openweather-kinesis-stream"
AWS_REGION = "eu-north-1"

kinesis_df = spark.readStream \
    .format("kinesis") \
    .option("streamName", STREAM_NAME) \
    .option("region", AWS_REGION) \
    .option("startingPosition", "latest") \
    .load()

# Define Schema
weather_schema = StructType() \
    .add("city", StringType()) \
    .add("temperature", FloatType()) \
    .add("humidity", IntegerType()) \
    .add("weather", StringType()) \
    .add("timestamp", IntegerType())

# Parse JSON Data
parsed_df = kinesis_df.selectExpr("CAST(data AS STRING) as json").select(from_json(col("json"), weather_schema).alias("data")).select("data.*")

# Write to Delta Table
parsed_df.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/delta/kinesis_checkpoint") \
    .outputMode("append") \
    .start("/delta/weather_data")
