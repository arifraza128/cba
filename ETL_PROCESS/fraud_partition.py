from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("FraudPartition") \
    .master("local[*]") \
    .getOrCreate()

data = [
    ("T001", 500),
    ("T002", 15000),
    ("T003", 800),
    ("T004", 25000),
    ("T005", 1200),
    ("T006", 50000)
]

rdd = spark.sparkContext.parallelize(data, 3)

def process_partition(records):
    print("Opening fraud service connection...")

    results = []

    for transaction_id, amount in records:

        if amount >= 10000:
            risk = "HIGH"
        else:
            risk = "LOW"

        results.append(
            (transaction_id, amount, risk)
        )

    print("Closing fraud service connection...")

    return iter(results)

result = rdd.mapPartitions(
    process_partition
)

for record in result.collect():
    print(record)

spark.stop()
