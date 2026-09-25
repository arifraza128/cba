import pandas as pd

df = pd.read_csv("sales.csv")

print("First 5 records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

df["city"] = df["city"].str.title()
df["category"] = df["category"].str.title()

df["total_amount"] = df["quantity"] * df["price"]

print("\nTotal sales by city:")
city_sales = df.groupby("city")["total_amount"].sum()
print(city_sales)

print("\nTotal sales by category:")
category_sales = df.groupby("category")["total_amount"].sum()
print(category_sales)

highest_city = city_sales.idxmax()
highest_sales = city_sales.max()

print("\nCity with highest sales:")
print(highest_city, highest_sales)

df.to_csv("cleaned_sales.csv", index=False)

print("\nCleaned data saved as cleaned_sales.csv")
