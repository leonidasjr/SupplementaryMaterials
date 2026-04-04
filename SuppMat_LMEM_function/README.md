# SuppMat_LMEM_function
**R function for automatic significant-parameter selection and mixed-effects modelling**

Silva Jr., L. (2019–2026)

https://github.com/leonidasjr/SupplementaryMaterials

**Cite as:**
SILVA JR., L. SuppMat_LMEM_function. [R function], 2019–2026. Available at: https://github.com/leonidasjr/SupplementaryMaterials.

---

## Overview

`SuppMat_LMEM_function.R` is a script for R that automatic selects significant-parameter and runs mixed-effects modelling. It reads the tab-separated dataset `SuppMat_ds_inferential_prosodic_features.txt` (produced by `SuppMat_SpeechRhythmExtractor.praat`) and applies a Linear Mixed-Effects Model (LMEM) of the form `d_var ~ DIALECT + (1 | SPEAKER)` to each of the 34 acoustic parameters. Parameters with a significant DIALECT fixed effect (p < 0.05, Satterthwaite) are reported with their full model summary and Nakagawa & Schielzeth (2013) R² effect sizes. All output is saved to `SuppMat_lmem_report.txt`.

---

## Repository contents

- `SuppMat_LMEM_function.R` — the main R script
- `SuppMat_ds_inferential_prosodic_features.txt` — example input dataset
- `SuppMat_LMEM_function_UserManual.docx` — User manual (step-by-step; line-by-line)
- `SuppMat_LMEM_function_README` — this file

---

## Requirements

- R 4.0+ — https://www.r-project.org
- RStudio (recommended) — https://posit.co
- R packages: `lme4`, `lmerTest`, `emmeans`, `tidyverse`, `MuMIn`

---

## Input dataset structure

**File:** `SuppMat_ds_inferential_prosodic_features.txt` | **Format:** tab-separated | 460 rows × 39 columns

| Columns | Type | Content |
|---|---|---|
| 1–5 | Metadata | AUDIOFILE, DIALECT (fixed effect), SPEAKER (random effect), SEX, CHUNK |
| 6–39 | 34 acoustic parameters | All numeric; automatically detected by `is.numeric()` |

---

## Step-by-step usage

1. Install packages: `install.packages(c('lme4','lmerTest','emmeans','tidyverse','MuMIn'))`
2. Open RStudio and load the script: **File → Open File → SuppMat_LMEM_function.R**
3. Run with **Source** button (or `Ctrl+Shift+Enter` / `Cmd+Shift+Enter`).
4. When `file.choose()` dialog appears, select `SuppMat_ds_inferential_prosodic_features.txt`.
5. Wait for analysis to finish. Significant parameters are printed to the Console.
6. Find `SuppMat_lmem_report.txt` in the same folder as the input dataset.

> ℹ If the `file.choose()` dialog does not appear, set `data_file` manually at line 51: `data_file <- '/full/path/to/SuppMat_ds_inferential_prosodic_features.txt'`

---

## LMEM model structure

For each dependent variable (one per acoustic parameter):

```
d_var ~ DIALECT + (1 | SPEAKER)
```

- **Fixed effect:** `DIALECT` — tests PB vs. SP group difference on each parameter
- **Random intercept:** `(1 | SPEAKER)` — accounts for between-speaker baseline variability
- **P-values:** Satterthwaite approximation via `lmerTest`
- **Significance threshold:** alpha = 0.05 (default; editable on line 7)
- **Effect size:** Marginal R² (fixed only) and Conditional R² (fixed + random) via `MuMIn::r.squaredGLMM()`

---

## Output file — SuppMat_lmem_report.txt

- **Location:** same folder as the input dataset
- **Format:** plain text
- **Content:** one block per significant parameter (p ≤ 0.05 on DIALECT)
- **Each block:** visual separator + variable name → full `lmerTest` summary → R² values
- Parameters with p > 0.05 are silently skipped

---

## R packages

| Package | Min. version | Role |
|---|---|---|
| lme4 | ≥ 1.1 | Core LMEM fitting via `lmer()` |
| lmerTest | ≥ 3.1 | Adds Satterthwaite p-values to `lmer()` summaries |
| emmeans | ≥ 1.7 | Loaded for post-hoc comparisons (available but not called automatically) |
| tidyverse | ≥ 1.3 | Data manipulation utilities |
| MuMIn | ≥ 1.46 | Computes R² effect sizes via `r.squaredGLMM()` (Nakagawa & Schielzeth, 2013) |

---

## Citation

- **Script:** SILVA JR., L. SuppMat_LMEM_function. [R function], 2019–2026. https://github.com/leonidasjr/SupplementaryMaterials.
- **lme4:** BATES et al. (2015). *Journal of Statistical Software,* 67(1), 1–48. DOI: https://doi.org/10.18637/jss.v067.i01.
- **R² method:** NAKAGAWA & SCHIELZETH (2013). *Methods in Ecology and Evolution,* 4(2), 133–142. DOI: https://doi.org/10.1111/j.2041-210x.2012.00261.x.
- **Context:** SILVA JR.; SILVA; MEER (2024). *Speech Prosody 2024,* DOI: 10.21437/SpeechProsody.2024-21.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| Error: package 'lme4' not found | Run: `install.packages(c('lme4','lmerTest','emmeans','tidyverse','MuMIn'))` |
| No p-values returned for [variable] | `lmerTest` is not loaded or its Satterthwaite method is unavailable. Ensure `library(lmerTest)` runs without error. |
| Error fitting model for [variable] | The model could not converge (e.g. singular fit, all-zero column, or insufficient variance). The function skips the variable and continues. |
| Report file is empty | No parameter had a significant fixed effect (p < 0.05). Check alpha value and dataset content. |
| file.choose() dialog does not appear | On some systems, RStudio or Rscript may suppress the dialog. Set `data_file` manually: `data_file <- '/path/to/SuppMat_ds_inferential_prosodic_features.txt'` |
| Encoding error reading the file | Ensure the `.txt` file was saved with UTF-8 or system-default encoding. Try: `read.delim(data_file, fileEncoding = 'UTF-8')` |
| Output file not saved | Check write permissions in the folder containing the dataset. Run from a folder where you have write access. |

---

## References (ABNT)

BATES, D.; MÄCHLER, M.; BOLKER, B.; WALKER, S. Fitting linear mixed-effects models using lme4. *Journal of Statistical Software,* v. 67, n. 1, p. 1–48, 2015. DOI: https://doi.org/10.18637/jss.v067.i01.

KUZNETSOVA, A.; BROCKHOFF, P. B.; CHRISTENSEN, R. H. B. lmerTest package: Tests in linear mixed effects models. *Journal of Statistical Software,* v. 82, n. 13, p. 1–26, 2017. DOI: https://doi.org/10.18637/jss.v082.i13.

NAKAGAWA, S.; SCHIELZETH, H. A general and simple method for obtaining R² from generalized linear mixed-effects models. *Methods in Ecology and Evolution,* v. 4, n. 2, p. 133–142, 2013. DOI: https://doi.org/10.1111/j.2041-210x.2012.00261.x.

R CORE TEAM. R: A language and environment for statistical computing. Vienna: R Foundation for Statistical Computing, 2024. Available at: https://www.r-project.org.

SILVA JR., L.; SILVA, J.; MEER, P. Prosodic aspects of Brazilian L2 English: A comparison of duration-based rhythm and F0 measures with American English, Indian English, and Brazilian Portuguese. In: *Proceedings of Speech Prosody 2024,* p. 101–105, 2024. DOI: 10.21437/SpeechProsody.2024-21.
