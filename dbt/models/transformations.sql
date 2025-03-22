WITH raw_data AS (
    SELECT * FROM {{ source('hive_metastore', 'weather_data') }}  -- ✅ Correct source reference
)
SELECT
    location AS city,  -- ✅ Use `location` instead of `city`
    temperature,
    humidity,
    wind_speed,
    timestamp,
    CASE
        WHEN temperature > 35 THEN 'Hot'
        WHEN temperature BETWEEN 20 AND 35 THEN 'Moderate'
        ELSE 'Cold'
    END AS temperature_category
FROM raw_data;
