import csv
import json
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    col,
    count,
    countDistinct,
    date_format,
    date_trunc,
    lower,
    lit,
    sum as spark_sum,
    to_timestamp,
    trim,
    when,
)
from pyspark.sql.types import (
    DoubleType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "pyspark_other_topics_data"
OUTPUT_DIR = BASE_DIR / "pyspark_other_topics_output"


# ============================================================
# CREATE SAMPLE DATASETS
# ============================================================

def create_sample_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # PROJECT 1: IoT Sensor Data (JSON)
    # --------------------------------------------------------

    sensor_rows = [
        {
            "device_id": "sensor-01",
            "timestamp": "2026-10-16 10:00:00",
            "temperature_c": 29.4,
            "humidity_pct": 55.0,
        },
        {
            "device_id": "sensor-02",
            "timestamp": "2026-10-16 10:05:00",
            "temperature_c": 36.2,
            "humidity_pct": 48.0,
        },
        {
            "device_id": "sensor-01",
            "timestamp": "2026-10-16 10:15:00",
            "temperature_c": 30.1,
            "humidity_pct": 54.0,
        },
        {
            "device_id": "sensor-03",
            "timestamp": "2026-10-16 10:20:00",
            "temperature_c": None,
            "humidity_pct": 62.0,
        },
        {
            "device_id": "sensor-02",
            "timestamp": "2026-10-16 11:01:00",
            "temperature_c": 37.5,
            "humidity_pct": 45.0,
        },
        {
            "device_id": "sensor-04",
            "timestamp": "2026-10-16 11:05:00",
            "temperature_c": 22.0,
            "humidity_pct": 120.0,
        },
        {
            "device_id": "sensor-01",
            "timestamp": "2026-10-16 11:10:00",
            "temperature_c": 28.7,
            "humidity_pct": 58.0,
        },
    ]

    sensor_file = DATA_DIR / "sensor_readings.json"

    sensor_file.write_text(
        "\n".join(json.dumps(row) for row in sensor_rows) + "\n",
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # PROJECT 2: Website Logs (CSV)
    # --------------------------------------------------------

    web_rows = [
        ["2026-10-16 10:00:01", "u101", "GET", "/home", 200, 120],
        ["2026-10-16 10:01:15", "u102", "GET", "/products", 200, 240],
        ["2026-10-16 10:02:18", "u101", "GET", "/products", 200, 210],
        ["2026-10-16 10:04:00", "u103", "POST", "/login", 401, 180],
        ["2026-10-16 10:08:30", "u104", "GET", "/products", 500, 900],
        ["2026-10-16 10:12:10", "u102", "GET", "/home", 200, 130],
        ["2026-10-16 11:00:04", "u105", "GET", "/home", 200, 100],
        ["2026-10-16 11:01:44", "u101", "GET", "/orders", 503, 1100],
        ["2026-10-16 11:05:21", "", "GET", "/health", 200, 10],
        ["2026-10-16 11:08:45", "u106", "GET", "/products", 404, 250],
    ]

    web_file = DATA_DIR / "web_requests.csv"

    with web_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "timestamp",
                "user_id",
                "method",
                "path",
                "status_code",
                "response_ms",
            ]
        )

        writer.writerows(web_rows)

    # --------------------------------------------------------
    # PROJECT 3: Movie Streaming Events (CSV)
    # --------------------------------------------------------

    movie_rows = [
        ["2026-10-16 09:10:00", "v101", "Space Journey", "Sci-Fi", 110, "true"],
        ["2026-10-16 09:20:00", "v102", "City Detectives", "Thriller", 45, "false"],
        ["2026-10-16 10:05:00", "v101", "Ocean Life", "Documentary", 50, "true"],
        ["2026-10-16 10:40:00", "v103", "Space Journey", "Sci-Fi", 95, "true"],
        ["2026-10-16 11:15:00", "v104", "City Detectives", "Thriller", 70, "true"],
        ["2026-10-16 12:00:00", "v102", "Ocean Life", "Documentary", 35, "false"],
        ["2026-10-16 12:30:00", "v101", "Comedy Nights", "Comedy", 25, "true"],
        ["2026-10-16 13:20:00", "v105", "Comedy Nights", "Comedy", 40, "false"],
        ["2026-10-16 13:40:00", "v106", "Space Journey", "Sci-Fi", 80, "true"],
    ]

    movie_file = DATA_DIR / "watch_events.csv"

    with movie_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "watched_at",
                "viewer_id",
                "title",
                "genre",
                "watch_minutes",
                "completed",
            ]
        )

        writer.writerows(movie_rows)

    print(f"Sample datasets created in: {DATA_DIR}")

# ============================================================
# PROJECT 1: IoT SENSOR MONITORING
# ============================================================

def run_iot_sensor_monitoring(spark):

    print("\n" + "=" * 65)
    print("PROJECT 1: IoT SENSOR MONITORING")
    print("=" * 65)

    schema = StructType([
        StructField("device_id", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("temperature_c", DoubleType(), True),
        StructField("humidity_pct", DoubleType(), True),
    ])

    input_file = str(DATA_DIR / "sensor_readings.json")
    output_path = OUTPUT_DIR / "iot_sensor_monitoring"

    raw = spark.read.schema(schema).json(input_file)

    print("\nRaw sensor data:")
    raw.show(truncate=False)

    # Clean the data
    clean = (
        raw
        .withColumn("device_id", trim(col("device_id")))
        .withColumn(
            "event_time",
            to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss"),
        )
        .filter(
            col("device_id").isNotNull()
            & (col("device_id") != "")
        )
        .filter(col("event_time").isNotNull())
        .filter(col("temperature_c").between(-50, 100))
        .filter(col("humidity_pct").between(0, 100))
        .dropDuplicates(["device_id", "event_time"])
    )

    print("\nClean sensor data:")
    clean.show(truncate=False)

    # Calculate hourly metrics
    hourly = (
        clean
        .withColumn("hour", date_trunc("hour", col("event_time")))
        .groupBy("hour")
        .agg(
            count("*").alias("readings_count"),
            countDistinct("device_id").alias("active_devices"),
            avg("temperature_c").alias("avg_temperature_c"),
            avg("humidity_pct").alias("avg_humidity_pct"),
            spark_sum(
                when(col("temperature_c") >= 35, 1).otherwise(0)
            ).alias("hot_readings"),
        )
        .orderBy("hour")
    )

    print("\nHourly IoT metrics:")
    hourly.show(truncate=False)

    # Save results
    hourly.write.mode("overwrite").option(
        "header", True
    ).csv(str(output_path / "hourly_metrics"))

    clean.write.mode("overwrite").option(
        "header", True
    ).csv(str(output_path / "clean_readings"))

    print(f"IoT output saved to: {output_path}")
    =======================================================
# PROJECT 2: WEBSITE LOG ANALYTICS
# ============================================================

def run_web_log_analytics(spark):

    print("\n" + "=" * 65)
    print("PROJECT 2: WEBSITE LOG ANALYTICS")
    print("=" * 65)

    schema = StructType([
        StructField("timestamp", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("method", StringType(), True),
        StructField("path", StringType(), True),
        StructField("status_code", IntegerType(), True),
        StructField("response_ms", DoubleType(), True),
    ])

    input_file = str(DATA_DIR / "web_requests.csv")
    output_path = OUTPUT_DIR / "web_log_analytics"

    raw = (
        spark.read
        .option("header", True)
        .schema(schema)
        .csv(input_file)
    )

    print("\nRaw website logs:")
    raw.show(truncate=False)

    # Clean the logs
    clean = (
        raw
        .withColumn(
            "event_time",
            to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss"),
        )
        .withColumn("path", trim(col("path")))
        .withColumn("user_id", trim(col("user_id")))
        .filter(col("event_time").isNotNull())
        .filter(
            col("path").isNotNull()
            & (col("path") != "")
        )
        .filter(col("status_code").between(100, 599))
        .filter(
            col("response_ms").isNotNull()
            & (col("response_ms") >= 0)
        )
        .dropDuplicates([
            "timestamp",
            "user_id",
            "method",
            "path",
            "status_code",
            "response_ms",
        ])
    )

    print("\nClean website logs:")
    clean.show(truncate=False)

    # Analyze requests by hour
    hourly = (
        clean
        .withColumn("hour", date_trunc("hour", col("event_time")))
        .groupBy("hour")
        .agg(
            count("*").alias("request_count"),
            countDistinct(
                when(col("user_id") != "", col("user_id"))
            ).alias("active_users"),
            avg("response_ms").alias("avg_response_ms"),
            spark_sum(
                when(col("status_code") >= 500, 1).otherwise(0)
            ).alias("server_errors_5xx"),
            spark_sum(
                when(
                    col("status_code").between(400, 499), 1
                ).otherwise(0)
            ).alias("client_errors_4xx"),
        )
        .orderBy("hour")
    )

    # Find the most requested website pages
    popular_paths = (
        clean
        .groupBy("path")
        .agg(
            count("*").alias("request_count"),
            avg("response_ms").alias("avg_response_ms"),
        )
        .orderBy(col("request_count").desc(), col("path"))
    )

    print("\nHourly website metrics:")
    hourly.show(truncate=False)

    print("\nMost requested paths:")
    popular_paths.show(10, truncate=False)

    # Save results
    hourly.write.mode("overwrite").option(
        "header", True
    ).csv(str(output_path / "hourly_metrics"))

    popular_paths.write.mode("overwrite").option(
        "header", True
    ).csv(str(output_path / "popular_paths"))

    print(f"Website output saved to: {output_path}")

# ============================================================
# PROJECT 3: MOVIE STREAMING ANALYTICS
# ============================================================

def run_movie_streaming_analytics(spark):

    print("\n" + "=" * 65)
    print("PROJECT 3: MOVIE STREAMING ANALYTICS")
    print("=" * 65)

    schema = StructType([
        StructField("watched_at", StringType(), True),
        StructField("viewer_id", StringType(), True),
        StructField("title", StringType(), True),
        StructField("genre", StringType(), True),
        StructField("watch_minutes", IntegerType(), True),
        StructField("completed", StringType(), True),
    ])

    input_file = str(DATA_DIR / "watch_events.csv")
    output_path = OUTPUT_DIR / "movie_streaming_analytics"

    raw = (
        spark.read
        .option("header", True)
        .schema(schema)
        .csv(input_file)
    )

    print("\nRaw streaming data:")
    raw.show(truncate=False)

    # Convert completion values into Boolean values
    completed_text = lower(trim(col("completed")))

    clean = (
        raw
        .withColumn(
            "event_time",
            to_timestamp(col("watched_at"), "yyyy-MM-dd HH:mm:ss"),
        )
        .withColumn("viewer_id", trim(col("viewer_id")))
        .withColumn("title", trim(col("title")))
        .withColumn("genre", trim(col("genre")))
        .withColumn(
            "completed_bool",
            when(
                completed_text.isin("true", "1", "yes"),
                lit(True),
            ).when(
                completed_text.isin("false", "0", "no"),
                lit(False),
            ),
        )
        .filter(col("event_time").isNotNull())
        .filter(
            col("viewer_id").isNotNull()
            & (col("viewer_id") != "")
        )
        .filter(
            col("title").isNotNull()
            & (col("title") != "")
        )
        .filter(
            col("genre").isNotNull()
            & (col("genre") != "")
        )
        .filter(col("watch_minutes").between(1, 1440))
        .filter(col("completed_bool").isNotNull())
        .dropDuplicates([
            "watched_at",
            "viewer_id",
            "title",
            "watch_minutes",
        ])
    )

    print("\nClean streaming data:")
    clean.show(truncate=False)

    # Calculate performance by movie genre
    genre_metrics = (
        clean
        .groupBy("genre")
        .agg(
            count("*").alias("watch_events"),
            countDistinct("viewer_id").alias("unique_viewers"),
            spark_sum("watch_minutes").alias("total_watch_minutes"),
            avg("watch_minutes").alias("avg_watch_minutes"),
            spark_sum(
                when(col("completed_bool"), 1).otherwise(0)
            ).alias("completed_events"),
        )
        .withColumn(
            "total_watch_hours",
            col("total_watch_minutes") / 60.0,
        )
        .withColumn(
            "completion_rate_pct",
            col("completed_events") * 100.0 / col("watch_events"),
        )
        .orderBy(col("total_watch_minutes").desc())
    )

    # Calculate daily active viewers
    daily_viewers = (
        clean
        .withColumn(
            "watch_date",
            date_format(col("event_time"), "yyyy-MM-dd"),
        )
        .groupBy("watch_date")
        .agg(
            countDistinct("viewer_id").alias("daily_active_viewers"),
            count("*").alias("watch_events"),
            spark_sum("watch_minutes").alias("total_watch_minutes"),
        )
        .orderBy("watch_date")
    )

    print("\nGenre performance:")
    genre_metrics.show(truncate=False)

    print("\nDaily audience:")
    daily_viewers.show(truncate=False)

    # Save results
    genre_metrics.write.mode("overwrite").option(
        "header", True
    ).csv(str(output_path / "genre_metrics"))

    daily_viewers.write.mode("overwrite").option(
        "header", True
    ).csv(str(output_path / "daily_viewers"))

    print(f"Movie streaming output saved to: {output_path}")




