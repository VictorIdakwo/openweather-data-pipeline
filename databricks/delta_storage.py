from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("DeltaStorage") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Read Delta Table
df = spark.read.format("delta").load("/delta/weather_data")

# Show Data
df.show()
