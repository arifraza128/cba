from pyspark.sql import SparkSession
from pyspark.sql.functions import avg

def main():
    spark = SparkSession.builder \
        .appName("StudentAnalysis") \
        .master("local[*]") \
        .getOrCreate()

    data = [
        (1, "Arif", 85),
        (2, "Rahul", 65),
        (3, "Aman", 92),
        (4, "Priya", 45),
        (5, "Sara", 75)
    ]

    columns = ["id", "name", "marks"]

    df = spark.createDataFrame(data, columns)

    print("All Students")
    df.show()

    print("Students with marks above 70")
    df.filter(df.marks > 70).show()

    print("Students with Pass or Fail Status")
    df.withColumn(
        "status",
        df.marks >= 40
    ).show()

    print("Average Marks")
    df.select(avg("marks").alias("average_marks")).show()

    spark.stop()

if __name__ == "__main__":
    main()
