WITH raw_data AS (
    SELECT * FROM {{ source('hive_metastore', 'weather_data') }}  -- ✅ Correct reference
)
SELECT
    city,
    temperature,
    humidity,
    weather,
    timestamp,
    CASE
        WHEN temperature > 35 THEN 'Hot'
        WHEN temperature BETWEEN 20 AND 35 THEN 'Moderate'
        ELSE 'Cold'
    END AS temperature_category
FROM raw_data;
