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

