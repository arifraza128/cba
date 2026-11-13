import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    mean_absolute_error
)

print("All libraries imported successfully!")

import os

files = os.listdir()

print(files)

df = pd.read_csv("archive/uber_nyc_enriched.csv")

print("Dataset loaded successfully!")

df.head()

df.shape

df.columns
df['pickup_dt'] = pd.to_datetime(df['pickup_dt'])

print("Dataset start:", df['pickup_dt'].min())
print("Dataset end:", df['pickup_dt'].max())

print("\nTime intervals:")
print(df['pickup_dt'].sort_values().diff().value_counts().head())

print("Missing values:")
print(df.isnull().sum())

print("\nDuplicate records:")
print(df.duplicated().sum())

df.info()

borough_demand = (
    df.groupby('borough')['pickups']
    .sum()
    .sort_values(ascending=False)
)

print(borough_demand)

borough_demand.plot(
    kind='bar',
    figsize=(10,5),
    title='Total Uber Pickups by Borough'
)

plt.ylabel('Total Pickups')
plt.show()

df = df.sort_values(['borough', 'pickup_dt'])

df['historical_ride_requests'] = (
    df.groupby('borough')['pickups'].shift(1)
)
df = df.dropna(subset=['historical_ride_requests'])

features = [
    'historical_ride_requests',
    'temp',
    'spd',
    'vsb',
    'pcp01',
    'pcp06',
    'pcp24'
]

X = df[features]
y = df['pickups']

df = df.sort_values('pickup_dt')

split = int(len(df) * 0.80)

X = df[features]
y = df['pickups']

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]
