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
