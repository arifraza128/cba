    print(f"\\n{'=' * 60}")
    print(title)
    print("=" * 60)
    print(f"Training Accuracy: {accuracy_score(y_train, train_pred):.3f}")
    print(f"Testing Accuracy : {accuracy_score(y_test, test_pred):.3f}")
    print(f"Precision        : {precision_score(y_test, test_pred, zero_division=0):.3f}")
    print(f"Recall           : {recall_score(y_test, test_pred, zero_division=0):.3f}")
    print(f"F1-score         : {f1_score(y_test, test_pred, zero_division=0):.3f}")
    print("\\nConfusion Matrix:")
    print(confusion_matrix(y_test, test_pred))
    print("\\nClassification Report:")
    print(classification_report(y_test, test_pred, zero_division=0))

    cm = confusion_matrix(y_test, test_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f"{title} - Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.show()


def compare_depths(X_train, X_test, y_train, y_test, criterion="gini",
                  depths=(2, 3, 4, 5, 6, 8, 10, None)):
    """Compare train and test accuracy at different tree depths."""
    rows = []

    for depth in depths:
        clf = DecisionTreeClassifier(
            criterion=criterion,
            max_depth=depth,
            random_state=RANDOM_STATE
        )
        clf.fit(X_train, y_train)

        rows.append({
            "max_depth": str(depth),
            "train_accuracy": accuracy_score(y_train, clf.predict(X_train)),
            "test_accuracy": accuracy_score(y_test, clf.predict(X_test))
        })

    results = pd.DataFrame(rows)
    print(f"\\nDepth comparison ({criterion}):")
    print(results.to_string(index=False))

    plt.figure(figsize=(9, 5))
    plt.plot(results["max_depth"], results["train_accuracy"],
             marker="o", label="Training Accuracy")
    plt.plot(results["max_depth"], results["test_accuracy"],
             marker="o", label="Testing Accuracy")
    plt.title(f"Training vs Testing Accuracy ({criterion})")
    plt.xlabel("Maximum Depth")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Select the depth with highest test accuracy; ties prefer simpler trees.
    results["depth_numeric"] = results["max_depth"].replace("None", "999").astype(int)
    best_row = results.sort_values(
        ["test_accuracy", "depth_numeric"],
        ascending=[False, True]
    ).iloc[0]
    best_depth = None if best_row["max_depth"] == "None" else int(best_row["max_depth"])
    print(f"Selected depth based on test accuracy: {best_depth}")
    return best_depth, results


def show_tree(model, feature_names, class_names, title):
    plt.figure(figsize=(22, 12))
    plot_tree(
        model,
        feature_names=list(feature_names),
        class_names=list(class_names),
        filled=True,
        rounded=True,
        fontsize=8
    )
    plt.title(title)
    plt.tight_layout()
    plt.show()


def show_feature_importance(model, feature_names, title, top_n=10):
    importance = pd.Series(
        model.feature_importances_,
        index=feature_names
    ).sort_values(ascending=False)

    print(f"\\n{title} - Feature Importance:")
    print(importance.head(top_n))

    plt.figure(figsize=(9, 5))
    importance.head(top_n).sort_values().plot(kind="barh")
    plt.title(title)
    plt.xlabel("Importance")
    plt.tight_layout()
    plt.show()
    return importance
diabetes.hist(figsize=(14, 10), bins=20)
plt.suptitle("Diabetes Dataset - Feature Distributions")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 7))
sns.heatmap(diabetes.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Diabetes Feature Correlation")
plt.tight_layout()
plt.show()

sns.countplot(data=diabetes, x="Outcome")
plt.title("Diabetes Outcome Distribution")
plt.xlabel("Outcome (0 = Non-diabetic, 1 = Diabetic)")
plt.tight_layout()
plt.show()

# In the original Pima dataset, zero is invalid for these measurements.
zero_invalid_columns = [
    "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"
]

for col in zero_invalid_columns:
    if col in diabetes.columns:
        diabetes[col] = diabetes[col].replace(0, np.nan)

print("\\nInvalid zero values converted to missing:")
print(diabetes[zero_invalid_columns].isnull().sum())

# Median imputation preserves rows and is robust to skewed medical measurements.
for col in zero_invalid_columns:
    diabetes[col] = diabetes[col].fillna(diabetes[col].median())

# Remove duplicate rows if any.
diabetes = diabetes.drop_duplicates()

print("\\nMissing values after preprocessing:")
print(diabetes.isnull().sum())

# Save cleaned dataset as required in the deliverable.
diabetes.to_csv("diabetes_cleaned.csv", index=False)
print("\\nCleaned diabetes dataset saved as diabetes_cleaned.csv")

X_diabetes = diabetes.drop("Outcome", axis=1)
y_diabetes = diabetes["Outcome"]

X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(
    X_diabetes, y_diabetes,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y_diabetes
)

print("\\nDiabetes training shape:", X_train_d.shape)
print("Diabetes testing shape :", X_test_d.shape)

# Compare different maximum depths.
best_depth_d, depth_results_d = compare_depths(
    X_train_d, X_test_d, y_train_d, y_test_d, criterion="gini"
)

# Experiment with criterion, depth, and minimum split.
diabetes_model = DecisionTreeClassifier(
    criterion="gini",            # Try "entropy" as well
    max_depth=best_depth_d,
    min_samples_split=10,        # Try 2, 5, 10, 20
    min_samples_leaf=5,          # Helps reduce overfitting
    random_state=RANDOM_STATE
)

diabetes_model.fit(X_train_d, y_train_d)

evaluate_model(
    diabetes_model, X_train_d, X_test_d, y_train_d, y_test_d,
    "Diabetes Decision Tree"
)

show_tree(
    diabetes_model,
    X_diabetes.columns,
    ["Non-diabetic", "Diabetic"],
    "Decision Tree - Diabetes Prediction"
)

diabetes_importance = show_feature_importance(
    diabetes_model, X_diabetes.columns,
    "Diabetes - Important Features"
)

# Compare Gini and Entropy using the selected depth.
for criterion in ["gini", "entropy"]:
    model = DecisionTreeClassifier(
        criterion=criterion,
        max_depth=best_depth_d,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=RANDOM_STATE
    )
    model.fit(X_train_d, y_train_d)
    print(
        f"Diabetes | {criterion} | "
        f"Train: {accuracy_score(y_train_d, model.predict(X_train_d)):.3f} | "
        f"Test: {accuracy_score(y_test_d, model.predict(X_test_d)):.3f}"
    )
    # ============================================================
# PRACTICAL 2: HEART DISEASE PREDICTION
# Dataset: UCI Cleveland Heart Disease
# ============================================================

print("\\n\\n******** HEART DISEASE PREDICTION ********")

# Download processed.cleveland.data from the UCI repository and save it
# as heart.csv, OR use a Cleveland CSV containing the named columns below.
heart_columns = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"
]

# If using the original UCI processed Cleveland file, it has no header
# and uses '?' for missing values and target values 0-4.
# This block detects and loads that original format.
try:
    heart = pd.read_csv("heart.csv")
    if heart.shape[1] == 14 and not set(heart_columns).issubset(heart.columns):
        heart.columns = heart_columns
except FileNotFoundError:
    raise FileNotFoundError(
        "Please download the Cleveland dataset and save it as heart.csv."
    )

# Normalize column names for common downloaded datasets.
heart.columns = [str(c).strip().lower() for c in heart.columns]

# Common Kaggle/UCI naming variants.
rename_map = {
    "num": "target",
    "heartdisease": "target",
    "condition": "target"
}
heart = heart.rename(columns=rename_map)

print("\\nFirst five records:")
print(heart.head())

print("\\nDataset shape:", heart.shape)
print("\\nDataset information:")
heart.info()

print("\\nStatistical summary:")
print(heart.describe(include="all"))

# Replace UCI missing marker '?' and convert columns to numeric.
heart = heart.replace("?", np.nan)

for col in heart.columns:
    heart[col] = pd.to_numeric(heart[col], errors="coerce")

print("\\nMissing values:")
print(heart.isnull().sum())

print("\\nDuplicate records:", heart.duplicated().sum())

heart = heart.drop_duplicates()
# Convert original Cleveland target: 0 = no disease, 1-4 = disease.
# If target already contains only 0 and 1, this also works.
heart["target"] = (heart["target"] > 0).astype(int)

# Impute missing numeric values using median.
for col in heart.columns:
    if col != "target":
        heart[col] = heart[col].fillna(heart[col].median())

print("\\nMissing values after preprocessing:")
print(heart.isnull().sum())

heart.to_csv("heart_cleaned.csv", index=False)
print("\\nCleaned heart dataset saved as heart_cleaned.csv")

# EDA
heart.hist(figsize=(15, 11), bins=20)
plt.suptitle("Heart Disease Dataset - Feature Distributions")
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 9))
sns.heatmap(heart.corr(numeric_only=True), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Heart Disease Feature Correlation")
plt.tight_layout()
plt.show()

sns.countplot(data=heart, x="target")
plt.title("Heart Disease Target Distribution")
plt.xlabel("0 = No disease, 1 = Disease")
plt.tight_layout()
plt.show()

