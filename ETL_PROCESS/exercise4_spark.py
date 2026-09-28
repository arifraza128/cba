from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    sum,
    count
)

spark = SparkSession.builder \
    .appName("ECommerceETL") \
    .getOrCreate()

orders = spark.read.csv(
    "cleaned_orders.csv",
    header=True,
    inferSchema=True
)

products = spark.read.csv(
    "cleaned_products.csv",
    header=True,
    inferSchema=True
)

orders = orders.withColumn(
    "order_date",
    col("order_date").cast("date")
)

joined = orders.join(
    products,
    on="product_id",
    how="inner"
)

result = joined.withColumn(
    "order_amount",
    col("quantity") * col("price")
)

print("Final dataset:")
result.show()

print("Total revenue:")
result.select(
    sum("order_amount").alias("total_revenue")
).show()

print("Revenue by category:")
result.groupBy("category") \
    .agg(
        sum("order_amount").alias("revenue")
    ) \
    .show()

print("Revenue by product:")
result.groupBy("product_id", "product_name") \
    .agg(
        sum("order_amount").alias("revenue")
    ) \
    .show()

print("Revenue by customer:")
result.groupBy("customer_id") \
    .agg(
        sum("order_amount").alias("revenue")
    ) \
    .show()

print("Orders per day:")
result.groupBy("order_date") \
    .agg(
        count("order_id").alias("order_count")
    ) \
    .show()

print("Top 3 products:")
result.groupBy("product_id", "product_name") \
    .agg(
        sum("order_amount").alias("revenue")
    ) \
    .orderBy(col("revenue").desc()) \
    .limit(3) \
    .show()

result.write \
    .mode("overwrite") \
    .parquet("output/ecommerce_orders")

spark.stop()
