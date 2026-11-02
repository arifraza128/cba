
from datetime import timedelta

from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import (
    col, to_date, dayofweek, lag, avg
)

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator


def main():


    spark = SparkSession.builder \
        .appName("ElectricityPrediction") \
        .master("local[*]") \
        .getOrCreate()

    df = spark.read \
        .option("header", True) \
        .option("inferSchema", True) \
        .csv("electricity_data.csv")

    df = df.withColumn(
        "date", to_date(col("date"), "yyyy-MM-dd")
    ).withColumn(
        "units", col("units").cast("double")
    ).filter(
        col("date").isNotNull() & col("units").isNotNull()
    ).orderBy("date")

    print("Electricity Data")
    df.show()

    window = Window.orderBy("date")

    features = df \
        .withColumn("day", dayofweek("date")) \
        .withColumn("previous_day", lag("units", 1).over(window)) \
        .withColumn("previous_week", lag("units", 7).over(window)) \
        .withColumn(
            "weekly_average",
            avg("units").over(window.rowsBetween(-7, -1))
        ) \
        .dropna()

    if features.count() < 15:
        raise ValueError("Please provide more historical data.")

    count = features.count()

    split_index = int(count * 0.8)

    split_date = features.orderBy("date") \
        .limit(split_index) \
        .select("date") \
        .collect()[-1][0]

    train = features.filter(col("date") <= split_date)
    test = features.filter(col("date") > split_date)

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

    lr = LinearRegression(
        featuresCol="features",
        labelCol="units"
    )

    model = lr.fit(train_data)

    predictions = model.transform(test_data)

    evaluator = RegressionEvaluator(
        labelCol="units",
        predictionCol="prediction",
        metricName="mae"
    )

    error = evaluator.evaluate(predictions)

    print("Mean Absolute Error:", round(error, 2))

    print("Actual vs Predicted Usage")

    predictions.select(
        "date",
        "units",
        "prediction"
    ).show()

    records = df.select("date", "units") \
        .orderBy("date").collect()

    last_seven = records[-7:]

    last_date = records[-1]["date"]
    tomorrow = last_date + timedelta(days=1)

    future = spark.createDataFrame([(
        tomorrow,
        tomorrow.isoweekday() % 7 + 1,
        float(records[-1]["units"]),
        float(records[-7]["units"]),
        sum(float(r["units"]) for r in last_seven) / 7
    )], [
        "date",
        "day",
        "previous_day",
        "previous_week",
        "weekly_average"
    ])

    future_data = assembler.transform(future)

    all_data = assembler.transform(features)
    final_model = lr.fit(all_data)

    forecast = final_model.transform(future_data)

    print("Tomorrow Electricity Prediction")

    forecast.select(
        "date",
        "prediction"
    ).show()

    spark.stop()


if __name__ == "__main__":
    main()

