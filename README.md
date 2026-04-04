# SupplementaryMaterials

**Supplementary Materials for Speech Science Research — Acoustic Processing, Rhythm Extraction, and Automatic Dialect Classification**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Praat](https://img.shields.io/badge/Praat-6.x-lightgrey.svg)](https://www.praat.org/)
[![R](https://img.shields.io/badge/R-4.x-blue.svg)](https://www.r-project.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0%2B-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

This repository provides fully documented, open-access tools for **phonetic and linguistic research** on speech prosody, rhythm, voice quality, and dialect classification. The materials span acoustic feature extraction, vocalic unit alignment, statistical modelling, and supervised machine learning — covering a complete research workflow from raw audio to classification and modelling results.

All scripts are designed with **reproducibility** as the primary goal: every parameter, random seed, feature list, and modelling decision is declared explicitly so that any researcher can re-run the analyses and obtain identical results.

The tools are suitable for researchers and students in **phonetics, phonology, sociolinguistics, speech science, and related areas** — including those with no prior background in programming or machine learning. Detailed User Manuals (English and Portuguese) are provided for each tool.

---

## Repository Structure

```
SupplementaryMaterials/
│
├── SuppMat_acoustic_processing/
│   │
│   ├── SuppMat_SpeechRhythmExtractor/
│   │   ├── SuppMat_ds_inferential_prosodic_features.*     ← inferential dataset
│   │   ├── SuppMat_ds_predictive_prosodic_features.*      ← ML dataset
│   │   ├── SuppMat_speech_annotation_report.txt
│   │   ├── SuppMat_SpeechRhythmExtractor.praat            ← main script
│   │   ├── SuppMat_SpeechRhythmExtractor_README_EN.md
│   │   ├── SuppMat_SpeechRhythmExtractor_README_PT.md
│   │   ├── SuppMat_SpeechRhythmExtractor_UserManual_EN.docx
│   │   └── SuppMat_SpeechRhythmExtractor_UserManual_PT.docx
│   │
│   └── SuppMat_VVUnitAligner/
│       ├── SuppMat_VVUnitAligner.praat                    ← main script
│       ├── SuppMat_VVUnitAligner_README.docx
│       ├── SuppMat_VVUnitAligner_README.pdf
│       ├── SuppMat_VVUnitAligner_UserManual.docx
│       └── SuppMat_VVUnitAligner_UserManual.pdf
│
├── SuppMat_ASR_dialect_classification/
│   ├── SuppMat_ds_inferential_prosodic_features.*         ← inferential dataset
│   ├── SuppMat_ds_predictive_prosodic_features.*          ← ML training/validation dataset
│   ├── SuppMatt_ASR_dialect_classification.py             ← main script
│   ├── SuppMat_ASR_dialect_classification_README.*        ← EN + PT
│   ├── SuppMat_ASR_dialect_classification_UserManual.*    ← EN + PT
│   ├── SuppMat_accuracy_comparison_plot.png
│   ├── SuppMat_confusion_matrices_panel.png
│   ├── SuppMat_feature_importance_plot.png
│   ├── SuppMat_classification_report.txt
│   └── SuppMat_predictions_by_model.csv
│
└── SuppMat_LMEM_function/
    ├── SuppMat_ds_inferential_prosodic_features.*         ← inferential dataset
    ├── SuppMat_LMEM_function.R                            ← main script
    ├── SuppMat_LMEM_function_README.docx
    ├── SuppMat_LMEM_function_README.pdf
    ├── SuppMat_LMEM_function_UserManual.docx
    ├── SuppMat_LMEM_function_UserManual.pdf
    └── SuppMat_lmem_report.txt
```

---

## Tools at a Glance

### 🗂️ `SuppMat_acoustic_processing/`

This folder contains two Praat-based tools for extracting acoustic features from speech recordings.

---

#### 📁 `SuppMat_SpeechRhythmExtractor/`

**Language:** Praat scripting language  
**Purpose:** Extracts a comprehensive set of prosodic and rhythmic acoustic features from speech recordings, including F0 statistics, intensity measures, spectral features (LTAS), and pause/rhythm metrics.

The features produced here serve as direct input to both `SuppMat_LMEM_function` (inferential modelling) and `SuppMat_ASR_dialect_classification` (machine learning classification).

**Key output features:**

| Output column | Script variable | Description | In practice | Reference |
|---|---|---|---|---|
| f0 SD | `f0sd` | Standard deviation of F0 | Global pitch variability | Ladd (2008) |
| f0 SAQ | `f0SAQ` | Semi-Absolute Quantile of F0 | Robust spread measure | Dellwo et al. (2012) |
| Δf0 mean (+) | `df0mean_pos` | Mean of positive F0 deltas | Steepness of rising pitch | Hirst & Di Cristo (1998) |
| Δf0 SD (+) | `df0sd_pos` | SD of positive F0 deltas | Intonational complexity | — |
| LTAS α slope | `sl_LTAS_alpha` | Spectral tilt | Vocal effort / brightness | Leino et al. (2011) |
| CV intensity | `cvint` | CV of RMS intensity | Rhythmic regularity | Dellwo (2006) |
| Pause SD | `pause_sd` | SD of pause duration | Phrasal planning variability | Christodoulides (2016) |
| Mean pause dur. | `pause_meandur` | Mean silent pause duration | Speech rate / planning | — |
| Pause rate | `pause_rate` | Pauses per unit time | Prosodic break frequency | — |

**Files:**

| File | Description |
|---|---|
| `SuppMat_SpeechRhythmExtractor.praat` | Main Praat script |
| `SuppMat_ds_inferential_prosodic_features.*` | Dataset for LMEM analyses |
| `SuppMat_ds_predictive_prosodic_features.*` | Dataset for ML classification |
| `SuppMat_speech_annotation_report.txt` | Speech annotation summary |
| `SuppMat_SpeechRhythmExtractor_README_EN.md` | Quick-start guide (English) |
| `SuppMat_SpeechRhythmExtractor_README_PT.md` | Guia rápido (português) |
| `SuppMat_SpeechRhythmExtractor_UserManual_EN.docx` | Full User Manual (English) |
| `SuppMat_SpeechRhythmExtractor_UserManual_PT.docx` | Manual do Usuário (português) |

---

#### 📁 `SuppMat_VVUnitAligner/`

**Language:** Praat scripting language  
**Purpose:** Automatically detects and aligns vocalic (V-to-V) intervals in speech, producing the TextGrid segmentation required as input for `SuppMat_SpeechRhythmExtractor`.

**Files:**

| File | Description |
|---|---|
| `SuppMat_VVUnitAligner.praat` | Main Praat script |
| `SuppMat_VVUnitAligner_README.docx` | Quick-start guide (.docx) |
| `SuppMat_VVUnitAligner_README.pdf` | Quick-start guide (.pdf) |
| `SuppMat_VVUnitAligner_UserManual.docx` | Full User Manual (.docx) |
| `SuppMat_VVUnitAligner_UserManual.pdf` | Full User Manual (.pdf) |

---

### 📁 `SuppMat_ASR_dialect_classification/`

**Language:** Python 3  
**Purpose:** Performs **automatic dialect classification** from tabular acoustic features using six supervised ML algorithms. Implements a complete, reproducible pipeline with hyperparameter tuning via 5-fold cross-validated grid search.

**ML algorithms:**

| Abbreviation | Full Name | Key Reference |
|---|---|---|
| LDA | Linear Discriminant Analysis | Fisher (1936); McLachlan (2004) |
| k-NN | k-Nearest Neighbours | Cover & Hart (1967) |
| DT | Decision Tree | Quinlan (1993) |
| RF | Random Forest | Breiman (2001) |
| SVM | Support Vector Machine | Cortes & Vapnik (1995) |
| GBM | Gradient Boosting Machine | Friedman (2001) |

**Files:**

| File | Description |
|---|---|
| `SuppMatt_ASR_dialect_classification.py` | Main Python script |
| `SuppMat_ds_inferential_prosodic_features.*` | Inferential dataset |
| `SuppMat_ds_predictive_prosodic_features.*` | ML training/validation dataset |
| `SuppMat_ASR_dialect_classification_README.*` | Quick-start guide (EN + PT) |
| `SuppMat_ASR_dialect_classification_UserManual.*` | Full User Manual (EN + PT) |
| `SuppMat_accuracy_comparison_plot.png` | Accuracy bar chart (all 6 models) |
| `SuppMat_confusion_matrices_panel.png` | 6-panel colour-coded confusion matrices |
| `SuppMat_feature_importance_plot.png` | Random Forest feature importances |
| `SuppMat_classification_report.txt` | Full textual classification report |
| `SuppMat_predictions_by_model.csv` | Per-sample predictions (all models) |

---

### 📁 `SuppMat_LMEM_function/`

**Language:** R  
**Purpose:** Provides a reusable R function for fitting and reporting **Linear Mixed-Effects Models (LMEMs)** on phonetic data. Handles repeated measures typical of speech datasets (multiple tokens per speaker, per condition), with automated model comparison and assumption diagnostics.

**Files:**

| File | Description |
|---|---|
| `SuppMat_LMEM_function.R` | Main R script |
| `SuppMat_ds_inferential_prosodic_features.*` | Inferential dataset for LMEM analyses |
| `SuppMat_LMEM_function_README.docx` | Quick-start guide (.docx) |
| `SuppMat_LMEM_function_README.pdf` | Quick-start guide (.pdf) |
| `SuppMat_LMEM_function_UserManual.docx` | Full User Manual (.docx) |
| `SuppMat_LMEM_function_UserManual.pdf` | Full User Manual (.pdf) |
| `SuppMat_lmem_report.txt` | LMEM output report |

---

## Suggested Workflow

The tools form a coherent research pipeline, though each can also be used independently:

```
Raw audio recordings
        │
        ▼
SuppMat_VVUnitAligner               ← Praat: align vocalic units → TextGrids
        │
        ▼
SuppMat_SpeechRhythmExtractor       ← Praat: extract acoustic features
        │
        ├─────────────────────────────────────────────────┐
        ▼                                                 ▼
SuppMat_LMEM_function           SuppMat_ASR_dialect_classification
← R: statistical modelling      ← Python: ML-based classification
        │                                                 │
        ▼                                                 ▼
SuppMat_lmem_report.txt         accuracy plots · confusion matrices
                                feature importances · predictions CSV
```

---

## Quick Start

### Praat tools
```
Open Praat → Open script... → select .praat file → Run
```

### Python tool
```bash
pip install pandas numpy matplotlib scikit-learn gtts
python SuppMatt_ASR_dialect_classification.py
```

### R tool
```r
install.packages(c("lme4", "lmerTest", "MuMIn"))
source("SuppMat_LMEM_function.R")
```

---

## Reproducibility

- **Praat:** all thresholds and window settings declared at the top of each script.
- **Python:** `RANDOM_STATE`, `TEST_SIZE`, feature list, and hyperparameter grids are fixed constants.
- **R:** model structure, random effects, and optimizer settings are fully documented.
- **Data:** open, human-readable formats throughout (TSV, CSV, Praat TextGrid).

---

## Requirements Summary

| Tool | Language | Key Dependencies |
|---|---|---|
| SuppMat_VVUnitAligner | Praat | Praat 6.x |
| SuppMat_SpeechRhythmExtractor | Praat | Praat 6.x |
| SuppMat_ASR_dialect_classification | Python 3.8+ | pandas, numpy, matplotlib, scikit-learn, gtts |
| SuppMat_LMEM_function | R 4.x | lme4, lmerTest, MuMIn |

---

## Citation

If you use any of these tools in your research, please cite this repository:

```
[Author(s)]. (2025). SupplementaryMaterials: Tools for Speech Science Research
[Software]. GitHub. https://github.com/leonidasjr/SupplementaryMaterials
```

---

## References

- Breiman, L. (2001). Random Forests. *Machine Learning, 45*(1), 5–32.
- Christodoulides, G. (2016). Disfluency and speech rhythm. *Proceedings of Speech Prosody 2016*.
- Cortes, C., & Vapnik, V. (1995). Support-vector networks. *Machine Learning, 20*(3), 273–297.
- Cover, T., & Hart, P. (1967). Nearest neighbor pattern classification. *IEEE TIT, 13*(1), 21–27.
- Dellwo, V. (2006). Rhythm and speech rate. *Language and Language Processing*, 231–241.
- Dellwo, V., et al. (2012). Speaker-idiosyncratic features in the speech signal. *Proceedings of Interspeech 2012*.
- Fisher, R. A. (1936). The use of multiple measurements in taxonomic problems. *Annals of Eugenics, 7*(2), 179–188.
- Friedman, J. H. (2001). Greedy function approximation: a gradient boosting machine. *Annals of Statistics, 29*(5), 1189–1232.
- Hirst, D., & Di Cristo, A. (Eds.). (1998). *Intonation Systems*. Cambridge University Press.
- Ladd, D. R. (2008). *Intonational Phonology* (2nd ed.). Cambridge University Press.
- Leino, T., et al. (2011). Long-term average spectrum in screening of voice quality. *Journal of Voice, 25*(6), 671–676.
- McLachlan, G. J. (2004). *Discriminant Analysis and Statistical Pattern Recognition*. Wiley.
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR, 12*, 2825–2830.
- Quinlan, J. R. (1993). *C4.5: Programs for Machine Learning*. Morgan Kaufmann.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

[https://github.com/leonidasjr/SupplementaryMaterials](https://github.com/leonidasjr/SupplementaryMaterials)
