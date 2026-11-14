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
y_train = y.iloc[:split]
y_test = y.iloc[split:]

print(X_train.shape)
print(X_test.shape)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)

from sklearn.linear_model import LinearRegression

model = LinearRegression()

model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)

print("Model training completed!")

import numpy as np
from sklearn.metrics import mean_squared_error, r2_score

rmse = np.sqrt(mean_squared_error(y_test, y_pred))

r2 = r2_score(y_test, y_pred)

print("RMSE:", rmse)
print("R2 Score:", r2)

baseline_pred = np.full(
    len(y_test),
    y_train.mean()
)

baseline_rmse = np.sqrt(
    mean_squared_error(y_test, baseline_pred)
)

baseline_r2 = r2_score(y_test, baseline_pred)

print("Baseline RMSE:", baseline_rmse)
print("Model RMSE:", rmse)

print("Baseline R2:", baseline_r2)
print("Model R2:", r2)

# pyrefly: ignore[missing-import]
from statsmodels.stats.outliers_influence import variance_inflation_factor
# pyrefly: ignore[missing-import]
from statsmodels.tools.tools import add_constant

X_vif = add_constant(X_train)

vif_df = pd.DataFrame()

vif_df['Feature'] = X_vif.columns

vif_df['VIF'] = [
    variance_inflation_factor(X_vif.values, i)
    for i in range(X_vif.shape[1])
]

print(vif_df)

df['pickup_dt'] = pd.to_datetime(df['pickup_dt'])

print("First 10 records:")
print(df[['pickup_dt', 'borough', 'pickups']].head(10))

print("\nTime interval distribution:")
print(
    df.sort_values('pickup_dt')['pickup_dt']
      .drop_duplicates()
      .diff()
      .value_counts()
      .head(10)
)

print("\nUnique boroughs:")
print(df['borough'].unique())
