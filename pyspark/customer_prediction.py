from datetime import timedelta

from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import (
    col, to_date, dayofweek, month, lag, avg,
    max as spark_max, round as spark_round
)
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator


def main():
    spark = SparkSession.builder \
        .appName("DailyCustomerPrediction") \
        .master("local[*]") \
        .getOrCreate()

    df = spark.read \
        .option("header", True) \
        .option("inferSchema", True) \
        .csv("daily_customers.csv")

    df = df.withColumn(
        "date", to_date(col("date"), "yyyy-MM-dd")
    ).withColumn(
        "customers", col("customers").cast("double")
    ).filter(
        col("date").isNotNull() & col("customers").isNotNull()
    ).orderBy("date")

    df.show()

    window = Window.orderBy("date")

    features = df \
        .withColumn("day_of_week", dayofweek("date")) \
        .withColumn("month", month("date")) \
        .withColumn("lag_1", lag("customers", 1).over(window)) \
        .withColumn("lag_7", lag("customers", 7).over(window)) \
        .withColumn(
            "avg_prev_7",
            avg("customers").over(window.rowsBetween(-7, -1))
        ) \
        .dropna(subset=["lag_1", "lag_7", "avg_prev_7"])

    total_rows = features.count()

    if total_rows < 30:
        raise ValueError(
            "Collect more daily historical data before training."
        )

    split_position = int(total_rows * 0.8)

    split_date = features.orderBy("date") \
        .limit(split_position) \
        .agg(spark_max("date")) \
        .first()[0]

    train = features.filter(col("date") <= split_date)
    test = features.filter(col("date") > split_date)

    input_columns = [
        "day_of_week",
        "month",
        "lag_1",
        "lag_7",
        "avg_prev_7"
    ]

    assembler = VectorAssembler(
        inputCols=input_columns,
        outputCol="features"
    )

    train_data = assembler.transform(train)
    test_data = assembler.transform(test)

    rf = RandomForestRegressor(
        featuresCol="features",
        labelCol="customers",
        numTrees=100,
        maxDepth=5,
        seed=42
    )

    model = rf.fit(train_data)

    test_predictions = model.transform(test_data)

    evaluator = RegressionEvaluator(
        labelCol="customers",
        predictionCol="prediction",
        metricName="mae"
    )

    mae = evaluator.evaluate(test_predictions)
    print("Test Mean Absolute Error:", round(mae, 2))

    print("Actual vs Predicted Customers")
    test_predictions.select(
        "date",
        "customers",
        spark_round(col("prediction")).alias("predicted")
    ).orderBy("date").show()

    # Retrain using all available historical data
    all_data = assembler.transform(features)
    final_model = rf.fit(all_data)

    history = df.select("date", "customers").orderBy("date").collect()

    if len(history) < 7:
        raise ValueError("At least 7 daily records are required.")

    last_seven = history[-7:]
    latest_date = history[-1]["date"]
