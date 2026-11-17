
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

# 1. Load dataset
df = pd.read_csv("iot_machine_data.csv")

# 2. Select input features and target
features = [
    "vibration_amplitude",
    "operating_temperature",
    "rpm_speed",
    "total_operating_hours",
    "oil_pressure"
]

target = "remaining_useful_life"
# Remove missing values
df = df[features + [target]].dropna()

X = df[features]
y = df[target]

# 3. Split data chronologically (80% training, 20% testing)
# Useful for continuous machine sensor data
df = df.sort_values("total_operating_hours")

X = df[features]
y = df[target]

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]
# 4. Polynomial Ridge Regression pipeline
model = Pipeline([
    ("polynomial", PolynomialFeatures(degree=2, include_bias=False)),
    ("scaler", StandardScaler()),
    ("ridge", Ridge(alpha=1.0))
])

# 5. Train model
model.fit(X_train, y_train)
# 6. Make predictions
y_pred = model.predict(X_test)

# 7. Calculate Mean Absolute Error
mae = mean_absolute_error(y_test, y_pred)

print("Mean Absolute Error (MAE):", round(mae, 2), "hours")
# 8. Calculate residuals
residuals = y_test - y_pred

print("Mean Residual:", round(residuals.mean(), 2), "hours")

# 9. Plot residuals
plt.figure(figsize=(12, 5))

# Residuals vs predicted values
plt.subplot(1, 2, 1)
plt.scatter(y_pred, residuals, alpha=0.6)
plt.axhline(y=0, color="red", linestyle="--")
plt.xlabel("Predicted Remaining Useful Life")
plt.ylabel("Residuals")
plt.title("Residuals vs Predicted Values")
