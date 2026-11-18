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
