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

