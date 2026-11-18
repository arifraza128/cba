from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score,
)


# --------------------------- CONFIGURATION ---------------------------
BASE_DIR = Path(__file__).resolve().parent
DIABETES_CSV = BASE_DIR / "diabetes.csv"
HEART_CSV = BASE_DIR / "heart.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
RANDOM_STATE = 42
TEST_SIZE = 0.20

OUTPUT_DIR.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid")


# --------------------------- COMMON FUNCTIONS ---------------------------
def save_figure(path: Path):
    """Save the current Matplotlib figure and close it."""
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()
    print(f"Saved chart: {path}")


def show_basic_eda(df: pd.DataFrame, dataset_name: str):
    print("\n" + "=" * 75)
    print(f"EXPLORATORY DATA ANALYSIS: {dataset_name}")
    print("=" * 75)
    print("\nFirst five rows:\n", df.head())
    print("\nDataset shape:", df.shape)
    print("\nData types and non-null counts:")
    df.info()
    print("\nDescriptive statistics:\n", df.describe(include="all").T)
    print("\nMissing values per column:\n", df.isna().sum())
    print("\nDuplicate records:", df.duplicated().sum())
    # EDA plots: class balance, distributions, and correlations.
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="target")
    plt.title("Heart Disease Target Distribution")
    plt.xlabel("Target (0 = No disease, 1 = Disease)")
    plt.ylabel("Number of patients")
    save_figure(OUTPUT_DIR / "heart_target_distribution.png")

    numeric_for_hist = [c for c in df.columns if c != "target"]
    df[numeric_for_hist].hist(figsize=(14, 10), bins=20, edgecolor="black")
    plt.suptitle("Heart Disease Feature Distributions")
    save_figure(OUTPUT_DIR / "heart_feature_histograms.png")

    plt.figure(figsize=(11, 8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm", center=0)
    plt.title("Heart Disease Correlation Heatmap")
    save_figure(OUTPUT_DIR / "heart_correlation_heatmap.png")

    # Compare a few continuous clinical measurements by target class.
    box_features = [c for c in ["age", "trestbps", "chol", "thalach", "oldpeak"] if c in df.columns]
    if box_features:
        plot_df = df.melt(
            id_vars="target", value_vars=box_features,
            var_name="medical_feature", value_name="measurement"
        )
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=plot_df, x="medical_feature", y="measurement", hue="target")
        plt.title("Heart Disease: Medical Measurements by Target Class")
        plt.xlabel("Feature")
        plt.ylabel("Recorded measurement")
        save_figure(OUTPUT_DIR / "heart_features_by_target.png")

    X = df.drop(columns="target")
    y = df["target"].rename("target")

    # These fields are coded categories in the Cleveland dataset, not continuous measurements.
    categorical_features = [
        c for c in ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]
        if c in X.columns
    ]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    save_cleaned_dataset(
        X, y, X_train, categorical_features, OUTPUT_DIR / "heart_cleaned.csv"
    )

    # Compare Gini and Entropy using the same training folds and parameter ranges.
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    criterion_results = []
    criterion_models = {}
    heart_param_grid = {
        "tree__max_depth": [2, 3, 4, 5, 6, None],
        "tree__min_samples_leaf": [1, 2, 4],
        "tree__min_samples_split": [2, 5],
    }

    for criterion in ["gini", "entropy"]:
        pipeline = build_pipeline(X, categorical_features, criterion=criterion)
        search = GridSearchCV(
            pipeline,
            param_grid=heart_param_grid,
            scoring="f1",
            cv=cv,
            n_jobs=-1,
            refit=True,
        )
        search.fit(X_train, y_train)
        criterion_models[criterion] = search.best_estimator_
        predictions = search.best_estimator_.predict(X_test)
        criterion_results.append({
            "criterion": criterion,
            "best_cv_f1": search.best_score_,
            "best_parameters": str(search.best_params_),
            "test_accuracy": accuracy_score(y_test, predictions),
            "test_precision": precision_score(y_test, predictions, zero_division=0),
            "test_recall": recall_score(y_test, predictions, zero_division=0),
            "test_f1": f1_score(y_test, predictions, zero_division=0),
        })
        print(f"\nBest {criterion} parameters:", search.best_params_)
        print(f"Best {criterion} mean CV F1:", round(search.best_score_, 4))

    comparison_df = pd.DataFrame(criterion_results)
    comparison_df.to_csv(OUTPUT_DIR / "heart_gini_entropy_comparison.csv", index=False)
    print("\nGini vs Entropy comparison:\n", comparison_df.to_string(index=False))

    # Select using training cross-validation F1, not the held-out test score.
    selected_criterion = comparison_df.sort_values("best_cv_f1", ascending=False).iloc[0]["criterion"]
    best_model = criterion_models[selected_criterion]
    print("\nSelected heart model criterion (based on CV F1):", selected_criterion)

    metrics = evaluate_model(
        best_model, X_train, X_test, y_train, y_test,
        ["No heart disease", "Heart disease"], "Heart"
    )
    pd.DataFrame([metrics]).to_csv(OUTPUT_DIR / "heart_final_metrics.csv", index=False)

    plot_tree_diagram(
        best_model, ["No heart disease", "Heart disease"],
        OUTPUT_DIR / "heart_decision_tree.png", max_depth=4
    )

    importance_df = aggregate_feature_importance(best_model, list(X.columns))
    importance_df.to_csv(OUTPUT_DIR / "heart_feature_importance.csv", index=False)
    print("\nTop three original features influencing the heart model:")
    print(importance_df.head(3).to_string(index=False))

    top_features = importance_df.head(10).sort_values("importance", ascending=True)
    plt.figure(figsize=(9, 5))
    sns.barplot(data=top_features, x="importance", y="feature")
    plt.title("Heart Disease: Top Feature Importances")
    plt.xlabel("Aggregated feature importance")
    plt.ylabel("Original feature")
    save_figure(OUTPUT_DIR / "heart_feature_importance.png")

    joblib.dump(best_model, OUTPUT_DIR / "heart_decision_tree_model.joblib")
    print("Saved trained heart-disease model.")


# --------------------------- MAIN ---------------------------
if __name__ == "__main__":
    print("Decision Tree Classification Practical")
    print("Expected input files:")
    print(" -", DIABETES_CSV)
    print(" -", HEART_CSV)
    print("Output folder:", OUTPUT_DIR)
