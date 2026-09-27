from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType
)
from pyspark.sql.functions import (
    col,
    avg,
    max,
    sum
)

spark = SparkSession.builder \
    .appName("EmployeePayrollETL") \
    .getOrCreate()

schema = StructType([
    StructField("emp_id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("department", StringType(), True),
    StructField("salary", IntegerType(), True),
    StructField("bonus", IntegerType(), True)
])

df = spark.read.csv(
    "employees.csv",
    header=True,
    schema=schema
)

print("Schema:")
df.printSchema()

print("Employee Data:")
df.show()

# TRANSFORM

df = df.withColumn(
    "total_salary",
    col("salary") + col("bonus")
)

print("Employee payroll:")
df.show()

print("Average salary by department:")
df.groupBy("department") \
    .agg(avg("salary").alias("average_salary")) \
    .show()

print("Maximum salary by department:")
df.groupBy("department") \
    .agg(max("salary").alias("maximum_salary")) \
    .show()

payroll_summary = df.groupBy("department") \
    .agg(
        sum("total_salary").alias("total_payroll")
    )

print("Total payroll:")
payroll_summary.show()

print("Employees with salary > 70000:")
df.filter(col("salary") > 70000).show()

print("Employees sorted by salary:")
df.orderBy(col("salary").desc()).show()

# LOAD
payroll_summary.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv("output/payroll_summary")

spark.stop()
