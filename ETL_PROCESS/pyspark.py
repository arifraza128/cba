from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, count, max, min

spark = SparkSession.builder \
    .appName("BankingAdvanced") \
    .master("local[*]") \
    .getOrCreate()

data = [
    ("T001", "ACC101", "Hyderabad", 5000),
    ("T002", "ACC102", "Bangalore", 15000),
    ("T003", "ACC101", "Hyderabad", 25000),
    ("T004", "ACC103", "Chennai", 3000),
    ("T005", "ACC102", "Bangalore", 50000),
    ("T006", "ACC101", "Hyderabad", 7000)
]

columns = [
    "transaction_id",
    "account_id",
    "city",
    "amount"
]

df = spark.createDataFrame(data, columns)

print("===== ORIGINAL DATA =====")
df.show()

partitioned = df.repartition(3, "city")

print("Number of partitions:")
print(partitioned.rdd.getNumPartitions())

def partition_info(index, records):
    for record in records:
        yield (
            index,
            record.transaction_id,
            record.city,
            record.amount
        )

partition_data = partitioned.rdd.mapPartitionsWithIndex(
    partition_info
)

print("===== PARTITION INFORMATION =====")

for record in partition_data.collect():
    print(record)

print("===== CITY AGGREGATION =====")

result = partitioned.groupBy("city").agg(
    sum("amount").alias("total_amount"),
    avg("amount").alias("average_amount"),
    count("transaction_id").alias("transaction_count"),
    max("amount").alias("maximum_transaction"),
    min("amount").alias("minimum_transaction")
)

result.show()

print("===== HIGH VALUE TRANSACTIONS =====")

fraud = partitioned.filter(
    partitioned.amount >= 10000
)

fraud.show()

def fraud_processing(records):
    print("Starting partition processing")

    for record in records:

        if record.amount >= 10000:
            yield (
                record.transaction_id,
                record.account_id,
                record.amount,
                "HIGH_RISK"
            )
        else:
            yield (
                record.transaction_id,
                record.account_id,
                record.amount,
                "NORMAL"
            )

processed = partitioned.rdd.mapPartitions(
    fraud_processing
)

print("===== FINAL RESULT =====")

for record in processed.collect():
    print(record)

spark.stop()
