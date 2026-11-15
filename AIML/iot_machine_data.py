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
