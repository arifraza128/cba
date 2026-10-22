import pandas as pd

# EXTRACT
df = pd.read_csv("customers.csv")

print("DataFrame information:")
df.info()

print("\nNull values:")
print(df.isnull().sum())

print("\nDuplicate records:")
print(df.duplicated().sum())

# TRANSFORM
df["name"] = df["name"].str.title()

df["email"] = df["email"].str.lower()

df["city"] = df["city"].str.title()

average_age = df["age"].mean()

df["age"] = df["age"].fillna(average_age)

df["email"] = df["email"].fillna("unknown@email.com")

df = df[df["status"].str.lower() == "active"]

def age_group(age):
    if age < 30:
        return "Young"
    elif age <= 40:
        return "Adult"
    else:
        return "Senior"

df["age_group"] = df["age"].apply(age_group)

# LOAD
df.to_csv("active_customers.csv", index=False)

print("\nFinal active customers:")
print(df)

summary = df.groupby("city").size().reset_index(name="Customer_Count")

print("\nCity Summary:")
print(summary)

summary.to_csv("customer_summary.csv", index=False)
