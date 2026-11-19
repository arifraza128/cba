import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    precision_score, recall_score, f1_score
)

# 1. Load dataset
cancer = load_breast_cancer()
df = pd.DataFrame(cancer.data, columns=cancer.feature_names)
df["diagnosis"] = cancer.target  # 0 = Malignant, 1 = Benign

print("First five rows:")
print(df.head())
print("\nDataset shape:", df.shape)
print("\nDataset information:")
df.info()
print("\nStatistical summary:")
print(df.describe())

# 2. EDA
print("\nMissing values:")
print(df.isnull().sum())
print("\nDuplicate records:", df.duplicated().sum())
print("\nDiagnosis distribution:")
print(df["diagnosis"].value_counts())

sns.countplot(data=df, x="diagnosis")
plt.title("Diagnosis Distribution (0=Malignant, 1=Benign)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 10))
sns.heatmap(df.corr(), cmap="coolwarm", annot=False)
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.show()

# 3. Preprocessing
df = df.drop_duplicates().copy()
X = df.drop("diagnosis", axis=1)
y = df["diagnosis"]

# 4. Split data: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))
