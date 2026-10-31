
from datetime import timedelta

from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import (
    col, to_date, dayofweek, lag, avg,
    max as spark_max
)
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator


# STEP 1: Start Spark
spark = SparkSession.builder \
    .appName("DailyOrderPrediction") \
    .master("local[*]") \
    .getOrCreate()


# STEP 2: Read CSV
df = spark.read.option("header", True) \
    .option("inferSchema", True) \
    .csv("daily_orders.csv")

df = df.withColumn(
    "date", to_date(col("date"), "yyyy-MM-dd")
).withColumn(
    "orders", col("orders").cast("double")
).orderBy("date")


# STEP 3: Create features
window = Window.orderBy("date")

df = df.withColumn("day", dayofweek("date")) \
    .withColumn("yesterday_orders",
                lag("orders", 1).over(window)) \
    .withColumn("last_week_orders",
                lag("orders", 7).over(window)) \
    .withColumn(
        "weekly_average",
        avg("orders").over(window.rowsBetween(-7, -1))
    )

df = df.dropna()


# STEP 4: Prepare training and testing data
count = df.count()
split_date = df.orderBy("date") \
    .limit(int(count * 0.8)) \
    .agg(spark_max("date")).first()[0]

train = df.filter(col("date") <= split_date)
test = df.filter(col("date") > split_date)

assembler = VectorAssembler(
    inputCols=[
        "day",
        "yesterday_orders",
        "last_week_orders",
        "weekly_average"
    ],
    outputCol="features"
)

train = assembler.transform(train)
test = assembler.transform(test)


# STEP 5: Train ML model
lr = LinearRegression(
    featuresCol="features",
    labelCol="orders"
)

model = lr.fit(train)


# STEP 6: Evaluate model
predictions = model.transform(test)

evaluator = RegressionEvaluator(
    labelCol="orders",
    predictionCol="prediction",
    metricName="mae"
)

print("Prediction Error:", evaluator.evaluate(predictions))

predictions.select(
    "date", "orders", "prediction"
).show()


# STEP 7: Predict tomorrow
history = spark.read.option("header", True) \
    .option("inferSchema", True) \
    .csv("daily_orders.csv")

records = history.orderBy("date").collect()

last_seven = records[-7:]
last_date = records[-1]["date"]
tomorrow = last_date + timedelta(days=1)

future_data = spark.createDataFrame([(
    tomorrow,
    tomorrow.isoweekday() % 7 + 1,
    float(records[-1]["orders"]),
    float(records[-7]["orders"]),
    sum(float(r["orders"]) for r in last_seven) / 7
)], [
    "date", "day",
    "yesterday_orders",
    "last_week_orders",
    "weekly_average"
])

future_data = assembler.transform(future_data)

final_model = lr.fit(assembler.transform(df))

forecast = final_model.transform(future_data)

print("Tomorrow's Order Prediction:")
forecast.select("date", "prediction").show()


# STEP 8: Stop Spark
spark.stop()
