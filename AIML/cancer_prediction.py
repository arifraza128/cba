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
# 5. Experiment with Gini, Entropy and tree parameters
results = []
best_model = None
best_score = -1
best_gap = float("inf")
best_name = ""

for criterion in ["gini", "entropy"]:
    for depth in [2, 3, 5, 7, 10]:
        for min_split in [2, 5, 10]:
            for min_leaf in [1, 2, 4]:
                model = DecisionTreeClassifier(
                    criterion=criterion,
                    max_depth=depth,
                    min_samples_split=min_split,
                    min_samples_leaf=min_leaf,
                    random_state=42
                )
                model.fit(X_train, y_train)
                train_acc = model.score(X_train, y_train)
                test_acc = model.score(X_test, y_test)
                gap = abs(train_acc - test_acc)

                results.append({
                    "Criterion": criterion,
                    "Max Depth": depth,
                    "Min Samples Split": min_split,
                    "Min Samples Leaf": min_leaf,
                    "Training Accuracy": train_acc,
                    "Testing Accuracy": test_acc,
                    "Accuracy Difference": gap
                })

                if test_acc > best_score or (
                    test_acc == best_score and gap < best_gap
                ):
                    best_score = test_acc
                    best_gap = gap
                    best_model = model
                    best_name = (
                        f"{criterion}, depth={depth}, "
                        f"min_split={min_split}, min_leaf={min_leaf}"
                    )

results_df = pd.DataFrame(results).sort_values(
    ["Testing Accuracy", "Accuracy Difference"],
    ascending=[False, True]
)
print("\nTop 10 model configurations:")
print(results_df.head(10).to_string(index=False))
results_df.to_csv("breast_cancer_model_comparison.csv", index=False)
