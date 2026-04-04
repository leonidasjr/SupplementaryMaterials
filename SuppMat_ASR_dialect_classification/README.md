# SuppMatt_ASR_dialect_classification.py
**Automatic Speech-Based Dialect Classification using Machine Learning**

**Repository:** https://github.com/leonidasjr/SupplementaryMaterials

Python 3 | scikit-learn | MIT License

---

## Overview

This script classifies speech varieties (dialects) from tabular acoustic features using six supervised machine learning algorithms. It tunes hyperparameters via 5-fold cross-validated grid search, evaluates each model on a held-out validation set, and exports publication-ready figures and reports automatically.

> **Reproducibility** All stochastic parameters (RANDOM_STATE, TEST_SIZE, feature list, hyperparameter grids) are declared explicitly at the top of the script.

---

## Requirements

```bash
pip install pandas numpy matplotlib scikit-learn gtts
```

| Library | Min. Version | Purpose |
|---|---|---|
| pandas | 1.3 | Load and manipulate the tabular dataset |
| numpy | 1.21 | Numerical array operations |
| matplotlib | 3.4 | Figure generation |
| scikit-learn | 1.0 | All ML algorithms, scaling, and evaluation |
| gtts | 2.2 | Text-to-Speech (internal use) |
| tkinter | built-in | File-selection dialog |

---

## Input Data Format

A tab-delimited text file (`.txt` or `.tsv`) with a header row. The `dialect` column contains the class label (e.g., PB, SP). Minimum recommended: ≥ 30 samples per class/group.

| Column | Variable | Description |
|---|---|---|
| f0 SD | f0sd | Standard deviation of F0 |
| f0 SAQ | f0SAQ | Semi-Absolute Quantile of F0 |
| Δf0 mean (+) | df0mean_pos | Mean of positive F0 deltas |
| Δf0 SD (+) | df0sd_pos | SD of positive F0 deltas |
| LTAS α slope | sl_LTAS_alpha | Spectral tilt |
| CV intensity | cvint | CV of RMS intensity |
| Pause SD | pause_sd | SD of pause duration |
| Mean pause dur. | pause_meandur | Mean pause duration |
| Pause rate | pause_rate | Pauses per unit time |

---

## How to Run

1. Open a terminal and navigate to the script folder.
2. `python SuppMatt_ASR_dialect_classification.py`
3. A file-selection dialogue opens. Select your dataset file.
4. All outputs are saved in the same folder as the dataset.

> 💡 Tip: On macOS/Linux use `python3`; on Windows, `py` may also work.

---

## Output Files

| File | Format | Contents |
|---|---|---|
| SuppMat_classification_report.txt | Plain text | Per-model accuracy, error rate, confusion matrix, precision, recall, F1 |
| SuppMat_accuracy_comparison_plot.png | PNG 300 dpi | Bar chart comparing accuracy of all 6 models |
| SuppMat_confusion_matrices_panel.png | PNG 300 dpi | 6-panel color-coded confusion matrices with absolute counts |
| SuppMat_feature_importance_plot.png | PNG 300 dpi | Random Forest feature importances, sorted descending |
| SuppMat_predictions_by_model.csv | CSV | Per-sample: model name, true label, predicted label |

---

## ML Algorithms

| Abbrev. | Full Name | Key Reference |
|---|---|---|
| LDA | Linear Discriminant Analysis | Fisher (1936); McLachlan (2004) |
| k-NN | k-Nearest Neighbours | Cover & Hart (1967); Altman (1992) |
| DT | Decision Tree | Quinlan (1993); Breiman et al. (1984) |
| RF | Random Forest | Breiman (2001); Louppe (2014) |
| SVM | Support Vector Machine | Cortes & Vapnik (1995); Schölkopf & Smola (2002) |
| GBM | Gradient Boosting Machine | Friedman (2001); Chen & Guestrin (2016) |

---

## Key Configuration Parameters

```python
RANDOM_STATE = 1    ← fixed seed; guarantees identical results on every run
TEST_SIZE    = 0.20 ← 20% of data reserved for validation
```

---

## Selected References

BREIMAN, L. Random forests. *Machine Learning,* v. 45, n. 1, p. 5–32, 2001.

CORTES, C.; VAPNIK, V. Support-vector networks. *Machine Learning,* v. 20, n. 3, p. 273–297, 1995.

FISHER, R. A. The use of multiple measurements in taxonomic problems. *Annals of Eugenics,* v. 7, n. 2, p. 179–188, 1936.

FRIEDMAN, J. H. Greedy function approximation: a gradient boosting machine. *Annals of Statistics,* v. 29, n. 5, p. 1189–1232, 2001.

PEDREGOSA, F. et al. Scikit-learn: machine learning in Python. *Journal of Machine Learning Research,* v. 12, p. 2825–2830, 2011.

---

https://github.com/leonidasjr/SupplementaryMaterials
