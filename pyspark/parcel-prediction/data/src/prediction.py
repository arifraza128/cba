
from datetime import timedelta

from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import (
    col, to_date, dayofweek, lag, avg,
    max as spark_max
)

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator


def main():

    # 1. Start Spark
    spark = SparkSession.builder \
        .appName("ParcelDeliveryPrediction") \
        .master("local[*]") \
        .getOrCreate()

    # 2. Load dataset
    df = spark.read \
        .option("header", True) \
        .option("inferSchema", True) \
        .csv("data/parcel_data.csv")

    df = df.withColumn(
        "date", to_date(col("date"), "yyyy-MM-dd")
    ).withColumn(
        "parcels", col("parcels").cast("double")
    ).filter(
        col("date").isNotNull() & col("parcels").isNotNull()
    ).orderBy("date")

    print("Original Parcel Data")
    df.show()

    # 3. Feature engineering
    window = Window.orderBy("date")

    features = df \
        .withColumn("day", dayofweek("date")) \
        .withColumn(
            "previous_day",
            lag("parcels", 1).over(window)
        ) \
        .withColumn(
            "previous_week",
            lag("parcels", 7).over(window)
        ) \
        .withColumn(
            "weekly_average",
            avg("parcels").over(
                window.rowsBetween(-7, -1)
            )
        ) \
        .dropna()

    if features.count() < 15:
        raise ValueError("Please collect more historical data.")

    # 4. Split data chronologically
    count = features.count()
    split_index = int(count * 0.8)

    split_date = features.orderBy("date") \
        .limit(split_index) \
        .agg(spark_max("date")) \
        .first()[0]

    train = features.filter(col("date") <= split_date)
    test = features.filter(col("date") > split_date)

    # 5. Prepare ML features
    assembler = VectorAssembler(
        inputCols=[
            "day",
            "previous_day",
            "previous_week",
            "weekly_average"
        ],
        outputCol="features"
    )

    train_data = assembler.transform(train)
    test_data = assembler.transform(test)

    # 6. Train model
    rf = RandomForestRegressor(
        featuresCol="features",
        labelCol="parcels",
        numTrees=50,
        maxDepth=5,
        seed=42
    )

    model = rf.fit(train_data)

    # 7. Evaluate model
    predictions = model.transform(test_data)

    evaluator = RegressionEvaluator(
        labelCol="parcels",
        predictionCol="prediction",
        metricName="mae"
    )

    error = evaluator.evaluate(predictions)

    print("Mean Absolute Error:", round(error, 2))

    print("Actual vs Predicted Parcels")
    predictions.select(
        "date",
        "parcels",
        "prediction"
    ).show()

    # 8. Predict tomorrow
    records = df.select(
        "date", "parcels"
    ).orderBy("date").collect()

    last_seven = records[-7:]
    last_date = records[-1]["date"]
    tomorrow = last_date + timedelta(days=1)

    future = spark.createDataFrame([(
        tomorrow,
        tomorrow.isoweekday() % 7 + 1,
        float(records[-1]["parcels"]),
        float(records[-7]["parcels"]),
        sum(float(r["parcels"]) for r in last_seven) / 7
    )], [
        "date",
        "day",
        "previous_day",
        "previous_week",
        "weekly_average"
    ])

    future_data = assembler.transform(future)

    # Retrain with all historical data
    all_data = assembler.transform(features)
    final_model = rf.fit(all_data)

    forecast = final_model.transform(future_data)

    print("Tomorrow's Parcel Prediction")

    forecast.select(
        "date",
        col("prediction").cast("int").alias("predicted_parcels")
    ).show()

    # 9. Stop Spark
    spark.stop()


if __name__ == "__main__":
    main()
