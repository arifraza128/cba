from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    month,
    sum,
    avg,
    count,
    when
)

spark = SparkSession.builder \
    .appName("BankingTransactionETL") \
    .getOrCreate()

df = spark.read.csv(
    "cleaned_transactions.csv",
    header=True,
    inferSchema=True
)

df = df.withColumn(
    "transaction_date",
    col("transaction_date").cast("date")
)

# Transaction month
df = df.withColumn(
    "transaction_month",
    month(col("transaction_date"))
)

# Risk flag
df = df.withColumn(
    "risk_flag",
    when(
        col("amount") >= 100000,
        "HIGH_VALUE"
    ).otherwise("NORMAL")
)

print("Final transaction data:")
df.show()

# 1. Transaction summary

transaction_summary = df.groupBy(
    "transaction_type"
).agg(
    count("*").alias("total_transactions"),
    sum("amount").alias("total_amount"),
    avg("amount").alias("average_amount")
)

print("Transaction Summary:")
transaction_summary.show()

# 2. City summary

city_summary = df.groupBy(
    "city"
).agg(
    count("*").alias("transaction_count"),
    sum("amount").alias("total_amount"),
    avg("amount").alias("average_amount")
)

print("City Summary:")
city_summary.show()

# 3. High-value transactions

high_value = df.filter(
    col("amount") >= 100000
)

print("High Value Transactions:")
high_value.show()

# 4. Account analysis

account_summary = df.groupBy(
    "account_id"
).agg(
    count("*").alias("total_transactions"),
    sum("amount").alias("total_amount"),
    avg("amount").alias("average_transaction")
)

print("Account Summary:")
account_summary.show()

# 5. Daily transaction analysis

daily_summary = df.groupBy(
    "transaction_date"
).agg(
    count("*").alias("transaction_count"),
    sum("amount").alias("total_amount")
)

print("Daily Summary:")
daily_summary.show()

# LOAD

transaction_summary.write \
    .mode("overwrite") \
    .parquet("output/transaction_summary")

high_value.write \
    .mode("overwrite") \
    .parquet("output/high_value_transactions")

account_summary.write \
    .mode("overwrite") \
    .parquet("output/account_summary")

daily_summary.write \
    .mode("overwrite") \
    .partitionBy("transaction_date") \
    .parquet("output/daily_transactions")

spark.stop()
