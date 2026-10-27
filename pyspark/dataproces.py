
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg

def main():
    spark = SparkSession.builder \
        .appName("EmployeeAnalysis") \
        .master("local[*]") \
        .getOrCreate()

    data = [
        (1, "Arif", "IT", 30000),
        (2, "Rahul", "HR", 25000),
        (3, "Aman", "IT", 40000),
        (4, "Priya", "HR", 35000)
    ]

    columns = ["id", "name", "department", "salary"]

    df = spark.createDataFrame(data, columns)

    print("All Employees")
    df.show()

    print("IT Department")
    df.filter(df.department == "IT").show()

    print("Department-wise Salary")
    df.groupBy("department").agg(
        sum("salary").alias("total_salary"),
        avg("salary").alias("average_salary")
    ).show()

    spark.stop()

if __name__ == "__main__":
    main()
