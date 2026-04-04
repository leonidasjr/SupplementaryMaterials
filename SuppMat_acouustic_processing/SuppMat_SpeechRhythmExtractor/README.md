# SpeechRhythmExtractor
**A Praat script for multidimensional prosodic-acoustic feature extraction**

Silva Jr., L. & Barbosa, P. A. (2019–2026)

Cite as: SILVA JR., L.; BARBOSA, P. A. SuppMat_SpeechRhythmExtractor. [Computer program for Praat], 2019–2026. Available at https://github.com/leonidasjr/SupplementaryMaterials/tree/main/SuppMat_acouustic_processing/SuppMat_SpeechRhythmExtractor.

---

## Overview

`SuppMat_SpeechRhythmExtractor.praat` is a Praat (Boersma & Weenink, 2023) script for the automatic extraction of 34 prosodic-acoustic parameters from speech corpora. It operates on pairs of audio (`.wav`) and annotation (`.TextGrid`) files and produces three output files:

1. An inferential dataset (`.txt`, tab-separated) with full metadata and 34 features — for mixed-effects linear models (LMEM).
2. A predictive dataset (`.txt`, tab-separated) with a dialect label and 34 features — for binary classification experiments.
3. A speech annotation report (`.txt`) with per-file and grand-total counts of phonetic units.

---

## Repository contents

- `SuppMat_SpeechRhythmExtractor.praat` — the main script
- `SuppMat_SpeechRhythmExtractor_UserManual.pdf` (step-by-step, line-by-line)
- `README.md` — this file

---

## Requirements

- Praat (conducted in version 6.1+) — https://www.praat.org (free)
- Audio files in `.wav` format
- Corresponding `.TextGrid` annotation files (see Section 4)

---

## TextGrid annotation requirements

Each `.wav` file must have a matching `.TextGrid` (identical filename, different extension) with at least 5 tiers in the following order:

- **Tier 1 — V_to_V:** inter-vocalic (vowel-to-vowel) intervals labelled `VV` or `V_to_V` (phonetic syllables)
- **Tier 2 — V_C_Pause:** vowel (V), consonant (C), and pause intervals. Pause labels recognised: `#`, `PAUSE`, `_`, `sp`, `<sp>`, `sil`
- **Tier 3 —** Original MAUS phone tier reference
- **Tier 4 — Word:** word intervals with orthographic transcription
- **Tier 5 — Chunk:** utterance chunk intervals with non-empty labels (e.g. `CH1`, `CH2`…)

> ℹ If your TextGrid uses different tier numbers, update the corresponding fields in the Praat form before running.

---

## Filename convention (mandatory)

The script automatically derives metadata from the filename. The required pattern is:

```
[DIALECT][SEP][SEX][NUMBER].wav
```

Example: `PBAFEM001.wav`
- Characters 1–2 → DIALECT = `PB`
- Characters 4–6 → SEX = `FEM`
- Last 3 digits → SPEAKER = `pb01`

---

## Step-by-step usage

1. Place `SuppMat_SpeechRhythmExtractor.praat`, all `.wav` files, and all `.TextGrid` files in the same folder.
2. Open Praat.
3. In the Praat menu bar: **Praat → Open Praat script…**
4. Navigate to the folder and select `SuppMat_SpeechRhythmExtractor.praat`. The Script Editor opens.
5. In the Script Editor menu: **Run → Run** (or `Ctrl+R` / `Cmd+R`).
6. The input form appears. Fill in the fields (see below) and click **OK**.
7. Monitor progress in the Praat Info window. When finished, the three output filenames are printed.
8. Find the output files in the same folder as the script.

---

## Input form fields

| Field | Default | Description |
|---|---|---|
| Output_file | SuppMat_ds_inferential… | Name of the inferential dataset (no extension; `.txt` is appended automatically) |
| Output_file_ASR | SuppMat_ds_predictive… | Name of the predictive dataset (no extension) |
| Unit | 2 = Semitones | F0 unit: 1 = Hz, 2 = Semitones (recommended for cross-speaker comparison) |
| left_F0_threshold | 75 | Lower F0 bound in Hz (adults: 60–100) |
| right_F0_threshold | 500 | Upper F0 bound in Hz (adults: 400–600) |
| V_to_V_tier | 1 | TextGrid tier number for VV intervals |
| V_C_Pause_tier | 2 | TextGrid tier number for V/C/pause intervals |
| Word_tier | 4 | TextGrid tier number for word intervals |
| Chunk_tier | 5 | TextGrid tier number for chunk intervals |

---

## Output files

- `SuppMat_ds_inferential_prosodic_features.txt` — AUDIOFILE, DIALECT, SPEAKER, SEX, CHUNK + 34 acoustic parameters
- `SuppMat_ds_predictive_prosodic_features.txt` — dialect + 34 acoustic parameters (no metadata)
- `SuppMat_speech_annotation_report.txt` — phonetic unit counts per file + grand totals

---

## Extracted parameters (34)

| Output column | Script variable | Description |
|---|---|---|
| durnorm_Lobanov | durLobanov | Lobanov (1971) z-score of VV syllable durations |
| syl_sd | sylSD | Standard deviation of VV syllable durations in ms within the chunk |
| f0norm_Lobanov | f0Lobanov | Lobanov z-score of F0 sampled at f0step intervals |
| f0median | f0median | 50th percentile of F0 (semitones or Hz) |
| f0peak | f0peak | 99th percentile of F0 |
| f0min | f0min | 1st percentile of F0 |
| f0sd | f0sd | Standard deviation of F0 |
| f0skewness | f0skew | (mean−median)/SD of F0 |
| f0SAQ | f0SAQ | (Q3−Q1)/2 of F0 — robust tonal amplitude |
| f0rate | tonerate_total | Total melodic extrema (peaks+valleys) per second |
| f0peak_rate | tonerate_max | F0 peaks per second |
| f0min_rate | tonerate_min | F0 valleys per second |
| f0cv | f0cv | SD / mean of F0 |
| df0mean | meandf0 | Mean of F0 discrete first derivative |
| df0mean_pos | meandf0pos | Mean of positive F0 increments |
| df0mean_neg | meandf0neg | Mean of negative F0 increments |
| df0sd | sdf0 | SD of F0 derivative |
| df0sd_pos | sdf0pos | SD of positive F0 increments |
| df0sd_neg | sdf0neg | SD of negative F0 increments |
| df0skewness | skdf0 | Skewness of F0 derivative |
| spect_emphasis | emphasis | Band energy above vs. below 400 Hz |
| sl_LTAS_breath | sl_ltas_high | LTAS slope 0–1 kHz vs 4–8 kHz |
| sl_LTAS_alpha | sl_ltas_medium | LTAS slope 0–1 kHz vs 1–4 kHz |
| sl_LTAS_L1L0 | sl_ltas_low | LTAS slope 300–800 Hz vs 50–300 Hz |
| cvint | cvint | 100 × SD / mean of intensity |
| jitter | jitter | Local jitter (%) — period perturbation |
| shimmer | shimmer | Local shimmer (%) — amplitude perturbation |
| hnr | hnr | Harmonics-to-Noise Ratio (dB) |
| pause_sd | deltaPAUSE | SD of pause durations (ms) |
| pause_meandur | meanDurPAUSE | Mean pause duration (ms) |
| pause_rate | pauserate | Pauses / VV duration × 1000 |
| speech_rate | srate | 1000 / mean VV duration |
| artic_rate | artrate | Syllables / (VV dur − mean pause) × 1000 |

---

## Citation

- **Script:** SILVA JR., L.; BARBOSA, P. A. SpeechRhythmExtractor. [Computer program for Praat], 2019–2026. https://github.com/leonidasjr/SpeechRhythmCode.
- **F0 derivative algorithm:** BARBOSA, P. A. ProsodyDescriptorExtractor (Version 2.0). [Praat script], 2020. https://github.com/pabarbosa/prosody-scripts.
- **Parameter definitions:** SILVA JR., L.; BARBOSA, P. A. Voice disguise and foreign accent: Prosodic aspects of English produced by Brazilian Portuguese speakers. *Journal of Experimental Phonetics*, v. 32, p. 195–226, 2023. DOI: https://doi.org/10.1344/efe-2023-32-195-226.

---

## License

Copyright (C) 2019–2026 Silva Jr., L. & Barbosa, P. A. This script is distributed for academic use. Please cite appropriately when used in research.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| No output file generated | Script not in the same folder as `.wav` files. |
| TextGrid error | Filename mismatch between `.wav` and `.TextGrid` (check capitalisation). |
| All F0 values = 0.001 | F0 thresholds too narrow for your speakers. Adjust in the form. |
| Very slow processing | Expected for large corpora. Each chunk requires multiple Praat analyses. |

---

## References (ABNT)

BARBOSA, P. A. *Incursões em torno do ritmo da fala.* Campinas: Pontes Editores, 2006.

BARBOSA, P. A. ProsodyDescriptorExtractor (Version 2.0). [Computer program for Praat], 2020. Available at: https://github.com/pabarbosa/prosody-scripts.

BOERSMA, P. Accurate short-term analysis of the fundamental frequency and the harmonics-to-noise ratio of a sampled sound. *Proceedings of the Institute of Phonetic Sciences, University of Amsterdam,* v. 17, p. 97–110, 1993. Available at: https://www.fon.hum.uva.nl/paul/papers/Proceedings_1993.pdf.

BOERSMA, P.; WEENINK, D. Praat: Doing phonetics by computer. [Computer program], Version 6.3+. Amsterdam: University of Amsterdam, 1992–2026. Available at: https://www.praat.org.

HAMMARBERG, B.; FRITZELL, B.; GAUFFIN, J.; SUNDBERG, J.; WEDIN, L. Perceptual and acoustic correlates of abnormal voice qualities. *Acta Otolaryngologica,* v. 90, n. 5–6, p. 441–451, 1980. DOI: https://doi.org/10.3109/00016488009131746.

LOBANOV, B. M. Classification of Russian vowels spoken by different speakers. *The Journal of the Acoustical Society of America,* v. 49, n. 2B, p. 606–608, 1971. DOI: https://doi.org/10.1121/1.1912396.

SILVA JR., L.; BARBOSA, P. A. SpeechRhythmExtractor. [Computer program for Praat], 2019–2026. Available at: https://github.com/leonidasjr/SpeechRhythmCode.

SILVA JR., L.; BARBOSA, P. A. Voice disguise and foreign accent: Prosodic aspects of English produced by Brazilian Portuguese speakers. *Estudios de Fonética Experimental / Journal of Experimental Phonetics,* v. 32, p. 195–226, 2023. DOI: https://doi.org/10.1344/efe-2023-32-195-226.

TITZE, I. R. *Workshop on Acoustic Voice Analysis: Summary Statement.* Denver: National Center for Voice and Speech, 1995. Available at: https://ncvs.org/archive/freebooks/summary-statement.pdf.

TITZE, I. R.; HORII, Y.; SCHERER, R. C. Some technical considerations in voice perturbation measurements. *Journal of Speech and Hearing Research,* v. 30, n. 2, p. 252–260, 1987. DOI: https://doi.org/10.1044/jshr.3002.252.
