
from pathlib import Path
from pyspark.sql import SparkSession, functions as F, types as T

# 1. Project paths
BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
OUTPUT = BASE / "output"
ERRORS = OUTPUT / "errors"

OUTPUT.mkdir(parents=True, exist_ok=True)
ERRORS.mkdir(parents=True, exist_ok=True)

# 2. Start Spark
spark = (
    SparkSession.builder
    .appName("ECommerceETL")
    .config("spark.sql.session.timeZone", "UTC")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

try:
    # 3. Extract JSON clickstream
    click_schema = T.StructType([
        T.StructField("user_id", T.StringType(), True),
        T.StructField("session_id", T.StringType(), True),
        T.StructField("event_time", T.StringType(), True),
        T.StructField("event", T.StringType(), True),
        T.StructField("_corrupt_record", T.StringType(), True)
    ])

    raw_clicks = (
        spark.read.schema(click_schema)
        .option("mode", "PERMISSIVE")
        .option("columnNameOfCorruptRecord", "_corrupt_record")
        .json(str(DATA / "clickstream.json"))
    )

    # 4. Extract CSV sales
    sales_schema = T.StructType([
        T.StructField("user_id", T.StringType(), True),
        T.StructField("session_id", T.StringType(), True),
        T.StructField("purchase_time", T.StringType(), True),
        T.StructField("amount", T.StringType(), True),
        T.StructField("status", T.StringType(), True)
    ])

    raw_sales = (
        spark.read.option("header", True)
        .schema(sales_schema)
        .csv(str(DATA / "store_sales.csv"))
    )

    # 5. Handle malformed JSON records
    corrupt = raw_clicks.filter(F.col("_corrupt_record").isNotNull())
    corrupt.write.mode("overwrite").json(str(ERRORS / "corrupt_clickstream"))

    clicks = raw_clicks.filter(F.col("_corrupt_record").isNull()).drop(
        "_corrupt_record"
    )

    # 6. Clean clickstream
    clicks = (
        clicks
        .withColumn("user_id", F.trim("user_id"))
        .withColumn("session_id", F.trim("session_id"))
        .withColumn("event", F.lower(F.trim("event")))
        .withColumn(
            "event_time",
            F.to_timestamp("event_time", "yyyy-MM-dd HH:mm:ss")
        )
    )

    invalid_clicks = clicks.filter(
        F.col("user_id").isNull() | (F.col("user_id") == "") |
        F.col("session_id").isNull() | (F.col("session_id") == "") |
        F.col("event_time").isNull() |
        F.col("event").isNull() | (F.col("event") == "")
    )
    invalid_clicks.write.mode("overwrite").json(
        str(ERRORS / "invalid_clickstream")
    )

    clicks = clicks.filter(
        F.col("user_id").isNotNull() & (F.col("user_id") != "") &
        F.col("session_id").isNotNull() & (F.col("session_id") != "") &
        F.col("event_time").isNotNull() &
        F.col("event").isNotNull() & (F.col("event") != "")
    ).dropDuplicates(["user_id", "session_id", "event_time", "event"])

    # 7. Clean sales
    sales = (
        raw_sales
        .withColumn("user_id", F.trim("user_id"))
        .withColumn("session_id", F.trim("session_id"))
        .withColumn("status", F.lower(F.trim("status")))
        .withColumn(
            "purchase_time",
            F.to_timestamp("purchase_time", "yyyy-MM-dd HH:mm:ss")
        )
        .withColumn("amount", F.col("amount").cast(T.DecimalType(12, 2)))
    )

    invalid_sales = sales.filter(
        F.col("user_id").isNull() | (F.col("user_id") == "") |
        F.col("session_id").isNull() | (F.col("session_id") == "") |
        F.col("purchase_time").isNull() |
        F.col("amount").isNull() | (F.col("amount") < 0) |
        F.col("status").isNull() |
        (~F.col("status").isin("completed", "pending", "cancelled"))
    )
    invalid_sales.write.mode("overwrite").json(str(ERRORS / "invalid_sales"))

    sales = sales.filter(
        F.col("user_id").isNotNull() & (F.col("user_id") != "") &
        F.col("session_id").isNotNull() & (F.col("session_id") != "") &
        F.col("purchase_time").isNotNull() &
        F.col("amount").isNotNull() & (F.col("amount") >= 0) &
        F.col("status").isin("completed", "pending", "cancelled")
    ).dropDuplicates(
        ["user_id", "session_id", "purchase_time", "amount", "status"]
    )

    # 8. Create one row per user/session
    sessions = clicks.groupBy("user_id", "session_id").agg(
        F.min("event_time").alias("session_start")
    )

    completed = sales.filter(F.col("status") == "completed")

    # 9. Join sessions with completed purchases
    matched = sessions.join(
        completed.select(
            "user_id", "session_id", "purchase_time", "amount", "status"
        ),
        on=["user_id", "session_id"],
        how="left"
    )

    print("Matched sessions and purchases:")
    matched.show(truncate=False)

    # 10. Count unique sessions by the hour of first event
    session_metrics = (
        sessions
        .withColumn("hour_start", F.date_trunc("hour", "session_start"))
        .groupBy("hour_start")
        .agg(
            F.countDistinct(
                F.struct("user_id", "session_id")
            ).alias("active_sessions")
        )
    )

    # 11. Sum completed sales by purchase hour
    revenue_metrics = (
        completed
        .withColumn("hour_start", F.date_trunc("hour", "purchase_time"))
        .groupBy("hour_start")
        .agg(
            F.sum("amount").cast("decimal(14,2)").alias("total_sales")
        )
    )

    # 12. Combine hourly metrics
    hourly = (
        session_metrics.join(
            revenue_metrics, on="hour_start", how="full_outer"
        )
        .select(
            "hour_start",
            F.coalesce(
                F.col("total_sales"),
                F.lit(0).cast("decimal(14,2)")
            ).alias("total_sales"),
            F.coalesce(
                F.col("active_sessions"), F.lit(0).cast("long")
            ).alias("active_sessions")
        )
        .orderBy("hour_start")
    )

    print("Final hourly metrics:")
    hourly.show(truncate=False)

    # 13. Save processed output locally
    hourly.coalesce(1).write.mode("overwrite").option(
        "header", True
    ).csv(str(OUTPUT / "hourly_metrics_csv"))

    print(f"Output saved under: {OUTPUT / 'hourly_metrics_csv'}")

    # 14. Optional PostgreSQL load
    POSTGRES_ENABLED = False

    if POSTGRES_ENABLED:
        (
            hourly.write.format("jdbc")
            .option("url", "jdbc:postgresql://localhost:5432/ecommerce_etl")
            .option("dbtable", "hourly_sales_metrics")
            .option("user", "postgres")
            .option("password", "YOUR_PASSWORD")
            .option("driver", "org.postgresql.Driver")
            .mode("overwrite")
            .save()
        )

finally:
    spark.stop()
