# ============================================
# ASR for dialect classification
# ============================================

import os
import sys
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Plot libraries
from matplotlib import pyplot as plt
import math
from matplotlib.colors import LinearSegmentedColormap

# Machine Learning libraries
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.svm import SVC
from gtts import gTTS

# -----------------------------
# Configuration
# -----------------------------
RANDOM_STATE = 1
TEST_SIZE = 0.20
TEST_SIZE_perc = TEST_SIZE * 100

# -----------------------------
# Load dataset
# -----------------------------
root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)

dataset_path = filedialog.askopenfilename(
    title="Select the tab-delimited dataset file",
    filetypes=[
        ("Tab-delimited text files", "*.txt *.tsv"),
        ("Text files", "*.txt"),
        ("TSV files", "*.tsv"),
        ("All files", "*.*")
    ]
)

if not dataset_path:
    raise SystemExit("No dataset was selected. Script interrupted.")

output_dir = os.path.dirname(dataset_path)

df = pd.read_csv(dataset_path, sep='\t', header=0)

# Standardize labels just in case
df.columns = df.columns.str.strip()
df['dialect'] = df['dialect'].astype(str).str.strip().str.upper()

print("Preview of dataset:")
print(df.head())
print("\nDescriptive statistics:")
print(df.describe())
print("\nSamples per dialect:")
print(df.groupby('dialect').size())
print("\nDialect unique values:", df['dialect'].unique())
print()

# -----------------------------
# Select predictors and target
# -----------------------------
# Statistically significant features only
selected_feature_names = [
    'f0sd', 'f0SAQ', 'df0mean_pos', 'df0sd_pos',
    'sl_LTAS_alpha', 'cvint', 'pause_sd', 'pause_meandur', 'pause_rate'
]

print("Selected features used for training:\n")
print('\n'.join(selected_feature_names))
print()

X = df[selected_feature_names].copy()
y = df['dialect'].copy()

# -----------------------------
# Split FIRST (before scaling)
# -----------------------------
X_train, X_validation, Y_train, Y_validation = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y
)

print("Training samples:", len(X_train))
print("Validation samples:", len(X_validation))
print("Training dialect counts:")
print(pd.Series(Y_train).value_counts())
print("Validation dialect counts:")
print(pd.Series(Y_validation).value_counts())
print()

# -----------------------------
# Scale using TRAINING data only
# -----------------------------
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_validation = scaler.transform(X_validation)

# -----------------------------
# Define models and hyperparameter grids
# -----------------------------
model_grid_list = [
    ('LDA', LinearDiscriminantAnalysis(), {
        'solver': ['lsqr', 'eigen'],
        'shrinkage': [None, 'auto']
    }),
    ('k-NN', KNeighborsClassifier(), {
        'n_neighbors': [3, 5, 7],
        'weights': ['uniform', 'distance']
    }),
    ('DT', DecisionTreeClassifier(random_state=RANDOM_STATE), {
        'max_depth': [None, 5, 10],
        'criterion': ['gini', 'entropy']
    }),
    ('RF', RandomForestClassifier(random_state=RANDOM_STATE), {
        'n_estimators': [100, 200],
        'max_depth': [None, 10],
        'max_features': ['sqrt']
    }),
    ('SVM', SVC(), {
        'C': [0.1, 1, 10],
        'kernel': ['linear', 'rbf'],
        'gamma': ['scale', 'auto']
    }),
    ('GBM', GradientBoostingClassifier(random_state=RANDOM_STATE), {
        'n_estimators': [100, 200],
        'learning_rate': [0.05, 0.1],
        'max_depth': [3, 5],
        'subsample': [0.8, 1.0]
    })
]

# -----------------------------
# Tune models
# -----------------------------
tuned_models = []
best_params_dict = {}

for name, model, param_grid in model_grid_list:
    if param_grid:
        print(f"Tuning {name}...")
        grid = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=5,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        grid.fit(X_train, Y_train)
        best_model = grid.best_estimator_
        best_params_dict[name] = grid.best_params_
        tuned_models.append((name, best_model))
        print(f"Best parameters for {name}: {grid.best_params_}\n")
    else:
        print(f"Training {name} with default parameters...")
        model.fit(X_train, Y_train)
        best_params_dict[name] = "None (default model)"
        tuned_models.append((name, model))
        print()

# -----------------------------
# Storage for results
# -----------------------------
all_predictions = {}
accuracy_scores = {}
error_rates = {}
all_confusion_matrices = {}

# -----------------------------
# Helper for evaluation
# -----------------------------
def get_label_config(y_true):
    """
    Returns confusion-matrix labels and display names
    robustly for either string or numeric labels.
    """
    unique_values = set(pd.Series(y_true).unique())

    if unique_values.issubset({0, 1}):
        return [0, 1], ['PB', 'SP']

    return ['PB', 'SP'], ['PB', 'SP']

# -----------------------------
# Confusion matrices plots
# -----------------------------
def save_confusion_matrix_panel(
    tuned_models,
    X_train,
    Y_train,
    X_validation,
    Y_validation,
    accuracy_scores,
    error_rates,
    filename="SuppMat_confusion_matrices_panel.png"
):
    model_order = [name for name, _ in tuned_models]
    n_models = len(model_order)

    ncols = 3
    nrows = math.ceil(n_models / ncols)

    fig, axes = plt.subplots(nrows, ncols, figsize=(17, 10))
    axes = np.array(axes).reshape(-1)

    cmap = LinearSegmentedColormap.from_list(
        "rg_custom",
        ["red", "gold", "chartreuse"]
    )

    panel_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    last_im = None

    for idx, (ml_algorithm_name, model) in enumerate(tuned_models):
        ax = axes[idx]

        model.fit(X_train, Y_train)
        predictions = model.predict(X_validation)

        cm_labels, display_labels = get_label_config(Y_validation)
        cm = confusion_matrix(Y_validation, predictions, labels=cm_labels)

        row_sums = cm.sum(axis=1, keepdims=True)
        cm_prop = cm / row_sums

        display_cm = np.array([
            [cm[1, 0], cm[1, 1]],
            [cm[0, 0], cm[0, 1]]
        ])

        display_prop = np.array([
            [cm_prop[1, 0], cm_prop[1, 1]],
            [cm_prop[0, 0], cm_prop[0, 1]]
        ])

        im = ax.imshow(display_prop, cmap=cmap, vmin=0, vmax=1)
        last_im = im

        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(['PB', 'SP'], fontsize=17)
        ax.set_yticklabels(['SP', 'PB'], fontsize=17)

        ax.set_xticks(np.arange(-.5, 2, 1), minor=True)
        ax.set_yticks(np.arange(-.5, 2, 1), minor=True)
        ax.grid(which="minor", color="black", linestyle="-", linewidth=1.6)
        ax.tick_params(which="minor", bottom=False, left=False)
        ax.tick_params(axis='both', length=0)

        ax.set_xlabel("Predicted", fontsize=14)
        ax.set_ylabel("Actual", fontsize=14)

        acc_pct = accuracy_scores[ml_algorithm_name] * 100
        err_pct = error_rates[ml_algorithm_name] * 100
        ax.set_title(
            f"{panel_letters[idx]} - {ml_algorithm_name}\nAccuracy: {acc_pct:.1f}% | ER: {err_pct:.1f}%",
            fontsize=16,
            loc="left",
            pad=12
        )

        for i in range(2):
            for j in range(2):
                ax.text(
                    j, i, f"{display_cm[i, j]}",
                    ha="center",
                    va="center",
                    fontsize=24,
                    color="white",
                    fontweight="bold"
                )

    for k in range(n_models, len(axes)):
        axes[k].axis("off")

    fig.subplots_adjust(right=0.90, wspace=0.35, hspace=0.30)

    cbar_ax = fig.add_axes([0.92, 0.23, 0.015, 0.54])
    cbar = fig.colorbar(last_im, cax=cbar_ax)
    cbar.ax.tick_params(labelsize=14)
    cbar.set_label("Sample proportion", fontsize=16, rotation=90, labelpad=12)

    plt.savefig(filename, dpi=300, bbox_inches="tight")
    print(f"{'Confusion matrices plot':<25} saved as: '{filename}'")

# -----------------------------
# Feature importance plot
# -----------------------------
def save_feature_importance_plot_styled(
    rf_model,
    selected_feature_names,
    filename="SuppMat_feature_importance_plot.png"
):
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]

    sorted_features = [selected_feature_names[i] for i in indices]
    sorted_importances = importances[indices]

    fig, ax = plt.subplots(figsize=(8, 6))

    gray_values = np.linspace(0.15, 0.85, len(sorted_importances))
    bar_colors = [str(g) for g in gray_values]

    ax.bar(
        range(len(sorted_importances)),
        sorted_importances,
        color=bar_colors,
        edgecolor='black',
        linewidth=1.2
    )

    ax.set_axisbelow(True)
    ax.grid(axis='y', linestyle='--', linewidth=0.8, alpha=0.7)

    ax.set_ylabel("Importance score", fontsize=14)
    ax.set_xlabel("Acoustic features", fontsize=14)

    ax.set_xticks(range(len(sorted_features)))
    ax.set_xticklabels(sorted_features, rotation=90, fontsize=12)
    ax.tick_params(axis='y', labelsize=12)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight")

    print(f"{'Feature importance plot':<25} saved as: '{filename}'")

# -----------------------------
# Evaluate models
# -----------------------------
for ml_algorithm_name, model in tuned_models:
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)

    all_predictions[ml_algorithm_name] = predictions
    accuracy_scores[ml_algorithm_name] = accuracy_score(Y_validation, predictions)
    error_rates[ml_algorithm_name] = 1 - accuracy_scores[ml_algorithm_name]

    cm_labels, display_labels = get_label_config(Y_validation)
    cm = confusion_matrix(Y_validation, predictions, labels=cm_labels)
    all_confusion_matrices[ml_algorithm_name] = cm

    report = classification_report(
        Y_validation,
        predictions,
        labels=cm_labels,
        target_names=display_labels
    )

    print(f'===== {ml_algorithm_name} =====')
    print('Best hyperparameters:', best_params_dict[ml_algorithm_name])
    print('Accuracy:', round(accuracy_scores[ml_algorithm_name], 3))
    print('Error rate:', round(error_rates[ml_algorithm_name], 3))
    print('-----------------')
    print('Dialect Classification Matrix')
    print('                                Predicted')
    print('                             PB            SP')
    for i in range(len(cm)):
        print(f'Actual {display_labels[i]:<11}: {cm[i][0]:11}   {cm[i][1]:11}')
    print('-----------------')
    print('Classification report:')
    print(report)
    print()

# -----------------------------
# Accuracy comparison plot
# -----------------------------
# Sort models by accuracy (descending)
sorted_items = sorted(accuracy_scores.items(), key=lambda x: x[1], reverse=True)

model_names = [k for k, v in sorted_items]
accuracy_percent = [v * 100 for k, v in sorted_items]

fig, ax = plt.subplots(figsize=(8, 6))

# Darker (best) → lighter (worst)
gray_values = np.linspace(0.15, 0.85, len(model_names))
bar_colors = [str(g) for g in gray_values]

bars = ax.bar(
    model_names,
    accuracy_percent,
    color=bar_colors,
    edgecolor='black',
    linewidth=1.2
)

# Grid behind bars
ax.set_axisbelow(True)
ax.grid(axis='y', linestyle='--', linewidth=0.8, alpha=0.7)

# Labels
ax.set_ylabel("Accuracy (%)", fontsize=14)
ax.set_xlabel("Machine Learning Models", fontsize=14)

ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

# Values above bars
for i, v in enumerate(accuracy_percent):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha='center', fontsize=12)

# L-shape axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

plt.ylim(0, 100)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "SuppMat_accuracy_comparison_plot.png"), dpi=300)

print(f"{'Accuracy comparison plot':<25} saved as: '{os.path.join(output_dir, 'SuppMat_accuracy_comparison_plot.png')}'")

# -----------------------------
# Confusion matrices plots
# -----------------------------
save_confusion_matrix_panel(
    tuned_models=tuned_models,
    X_train=X_train,
    Y_train=Y_train,
    X_validation=X_validation,
    Y_validation=Y_validation,
    accuracy_scores=accuracy_scores,
    error_rates=error_rates,
    filename=os.path.join(output_dir, "SuppMat_confusion_matrices_panel.png")
)

# -----------------------------
# Feature importance plot
# -----------------------------
rf_model = None
for name, model in tuned_models:
    if name == 'RF':
        rf_model = model
        break

if rf_model is not None:
    rf_model.fit(X_train, Y_train)
    save_feature_importance_plot_styled(
        rf_model=rf_model,
        selected_feature_names=selected_feature_names,
        filename=os.path.join(output_dir, "SuppMat_feature_importance_plot.png")
    )
else:
    print("Random Forest model not found. Skipping feature importance plot.")

# -----------------------------
# Save report to file
# -----------------------------
def save_console_output_to_file(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        original_stdout = sys.stdout
        sys.stdout = f

        print("=" * 25)
        print("ASR classification report")
        print("=" * 25)
        print("")
        print(f"Random state: {RANDOM_STATE}")
        print(f"Test size: {TEST_SIZE_perc}%")
        print("")
        print("Training samples:", len(X_train))
        print("Validation samples:", len(X_validation))
        print("Training dialect counts:")
        print(pd.Series(Y_train).value_counts())
        print("Validation dialect counts:")
        print(pd.Series(Y_validation).value_counts())
        print("")
        print("Selected features:")
        for feat in selected_feature_names:
            print(f"- {feat}")
        print()

        for ml_algorithm_name, model in tuned_models:
            model.fit(X_train, Y_train)
            predictions = model.predict(X_validation)

            acc = accuracy_score(Y_validation, predictions)
            err = 1 - acc

            cm_labels, display_labels = get_label_config(Y_validation)
            cm = confusion_matrix(Y_validation, predictions, labels=cm_labels)
            report = classification_report(
                Y_validation,
                predictions,
                labels=cm_labels,
                target_names=display_labels
            )

            print(f'===== {ml_algorithm_name} =====')
            print('Best hyperparameters:', best_params_dict[ml_algorithm_name])
            print('Accuracy:', round(acc, 3))
            print('Error rate:', round(err, 3))
            print('-----------------')
            print('Dialect Classification Matrix')
            print('                                Predicted')
            print('                             PB            SP')
            for i in range(len(cm)):
                print(f'Actual {display_labels[i]:<11}: {cm[i][0]:11}   {cm[i][1]:11}')
            print('-----------------')
            print('Classification report:')
            print(report)
            print()

        sys.stdout = original_stdout

save_console_output_to_file(os.path.join(output_dir, 'SuppMat_classification_report.txt'))
print(f"{'Classification report':<25} saved as: '{os.path.join(output_dir, 'SuppMat_classification_report.txt')}'")

# -----------------------------
# Per-sample predictions export
# -----------------------------
results_rows = []
for ml_algorithm_name, predictions in all_predictions.items():
    for true_label, pred_label in zip(Y_validation, predictions):
        results_rows.append({
            "model": ml_algorithm_name,
            "true_label": true_label,
            "predicted_label": pred_label
        })

results_df = pd.DataFrame(results_rows)
results_df.to_csv(os.path.join(output_dir, "SuppMat_predictions_by_model.csv"), index=False)
print(f"{'Per-sample prediction':<25} saved as: '{os.path.join(output_dir, 'SuppMat_predictions_by_model.csv')}'")

print("\nASR classification completed.")
