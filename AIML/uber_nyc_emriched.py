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
