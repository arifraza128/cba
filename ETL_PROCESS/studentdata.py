SOURCE FILE: students.csv

ID,Name,Marks,Department
101,Arif,85,CSE
102,Rahul,78,CSE
103,John,,ECE
104,Anil,92,CSE
105,Arif,85,CSE

import pandas as pd
import sqlite3

# EXTRACT
df = pd.read_csv("students.csv")

print("Extracted Data:")
print(df)

# TRANSFORM
df = df.drop_duplicates()
df["Marks"] = df["Marks"].fillna(0)
df["Marks"] = df["Marks"].astype(int)
df["Department"] = df["Department"].replace({
    "CSE": "Computer Science",
    "ECE": "Electronics"
})

print("\nTransformed Data:")
print(df)

# LOAD
conn = sqlite3.connect("StudentDB.db")

df.to_sql("students", conn, if_exists="replace", index=False)

print("\nData loaded successfully into StudentDB")

conn.close()
