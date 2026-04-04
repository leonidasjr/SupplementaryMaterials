# SuppMat_VVunitAligner
**Praat script for webMAUS-based VV phonetic re-alignment**

Silva Jr., L. (2021–2026)

---

## Overview

`SuppMat_VVunitAligner.praat` is a Praat pre-processing script connecting the webMAUS forced aligner (Kisler et al., 2017) to SpeechRhythmExtractor (Silva Jr. & Barbosa, 2019–2026). It converts webMAUS phone units (G2P→MAUS→PHO2SYL) into phonetic V-to-V (vowel-onset-to-vowel-onset) intervals and produces a 6-tier TextGrid ready for prosodic-acoustic feature extraction.

---

## Repository contents

- `SuppMat_VVunitAligner.praat` — the main script
- `SuppMat_VVunitAligner_UserManual` (step-by-step; line-by-line)
- `SuppMat_VVunitAligner_README` — this file

---

## Three-stage pipeline

1. **STAGE 1 — webMAUS:** upload `.wav` + `.txt` → G2P→MAUS→PHO2SYL → Language: English (US) or Italian (IT) for BP → Praat (TextGrid) → Keep everything: false → Download ZIP → extract `.TextGrid`
2. **STAGE 2 — VVUnitAligner:** script + `.wav` + `.TextGrid` in same folder → run → inspect `Complete_` output
3. **STAGE 3 — SpeechRhythmExtractor:** `filename.TextGrid` with `V_to_V_tier=1`, `V_C_Pause_tier=2`, `Word_tier=4`, `Chunk_tier=5`

---

## Requirements

- Praat 5+ → https://www.praat.org
- Audio: `.wav` file
- Annotation: `.TextGrid` from webMAUS G2P→MAUS→PHO2SYL (same folder, same base name as `.wav`)

---

## webMAUS settings

| Setting | Value |
|---|---|
| Pipeline name | G2P → MAUS → PHO2SYL |
| Language | English (US) · Italian (IT) ⚠ No BP protocol in webMAUS |
| Output format | Praat (TextGrid) |
| Keep everything | false |

> ℹ For Brazilian Portuguese, always select Italian (IT) in webMAUS and Portuguese (BR) in this script. Manual correction of the VC tier is strongly recommended.

---

## Step-by-step usage

1. Place `SuppMat_VVunitAligner.praat`, `.wav`, and `.TextGrid` files in the same folder.
2. Open Praat.
3. **Praat → Open Praat script…** → select `SuppMat_VVunitAligner.praat`.
4. **Script Editor → Run → Run** (`Ctrl+R` / `Cmd+R`).
5. Select **Language:** Portuguese (BR) [1] or English (US) [2].
6. Select **Chunk_segmentation:** Automatic [1], Forced/manual [2], or None [3].
7. Set **Pause_duration_(s)** (default 0.35 s).
8. Click **OK**. Monitor progress in the Info window.
9. When done: `'Realignment process ended.'` + elapsed time appear in Info.
10. Inspect `MAUS_[filename]` (original) and `Complete_[filename]` (10-tier output).

---

## Input form fields

| Field (line) | Default | Type | Description |
|---|---|---|---|
| Language (17) | 1 = PT(BR) | optionmenu | 1 = Portuguese (BR) — use Italian (IT) in webMAUS. 2 = English (US). |
| Chunk_segmentation (23) | 1 = Automatic | optionmenu | 1 = Automatic (intensity); 2 = Forced/manual (interactive); 3 = None. |
| Pause_duration_(s) (28) | 0.35 | positive | Min. silence gap (s) for Automatic chunk boundaries. |
| Save_TextGrid_files (29) | 1 = true | boolean | 0 = Objects window only; 1 = also save `.TextGrid` to disk. |

---

## Output tier structure (Complete)

| Tier | Name | Labels | Content |
|---|---|---|---|
| 1 | VowelOnsets | (points) | Point tier — one point per vowel onset |
| 2 | VC | V, C, # | Phoneme classification: V=vowel, C=consonant, #=pause |
| 3 | ORT-MAU | orthographic | Orthographic tier from webMAUS |
| 4 | Word | orthographic | Word-level intervals (orthographic transcription) |
| 5 | Chunk | CH1, CH2 … | Utterance chunk intervals → Chunk_tier in SpeechRhythmExtractor |
| 6 | Tone | H1, L1 … | Tone points: H = F0 peak, L = F0 valley (auto or empty) |

---

## Citation

- **Script:** SILVA JR., L. SuppMat_VVunitAligner. [Praat script], 2021–2026. https://github.com/leonidasjr/VVunitAlignerCode_webMAUS.
- **webMAUS:** KISLER, T.; REICHEL, U. D.; SCHIEL, F. *Computer Speech & Language,* v. 45, p. 326–347, 2017. DOI: https://doi.org/10.1016/j.csl.2016.11.005.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| TextGrid not found | Filename mismatch (`.wav` vs `.TextGrid`). Check case sensitivity. |
| No V labels produced | Wrong language or wrong webMAUS pipeline. Verify G2P→MAUS→PHO2SYL. |
| 'TextGrid merged' error | Previous run left an object. Close all TextGrids and re-run. |
| Chunk tier empty | Chunk_segmentation = None, or no qualifying silence found. |

---

## References (ABNT)

BARBOSA, P. A.; MADUREIRA, S. *Manual de fonética acústica experimental: aplicações a dados do português.* São Paulo: Cortez, 2015.

BISOL, L. *Introdução a estudos de fonologia do português brasileiro.* 5. ed. Porto Alegre: EDIPUCRS, 2010.

BOERSMA, P.; WEENINK, D. Praat: doing phonetics by computer. [Programa de computador], versão 6.3+. Amsterdam: University of Amsterdam, 1992–2026. Available at: https://www.praat.org.

CALLOU, D.; LEITE, Y. *Iniciação à fonética e à fonologia.* 11. ed. Rio de Janeiro: Zahar, 2009.

CANEPARI, L. *Italian phonology.* München: LINCOM Europa, 1999.

KRALJEVSKI, I.; TAN, Z.-H.; BISSIRI, M. P. Comparison of forced-alignment speech recognition and humans for generating reference VAD. In: *Proceedings of INTERSPEECH, 2015.,* p. 1–5, 2015.

KISLER, T.; REICHEL, U.; SCHIEL, F. Multilingual processing of speech via web services. *Computer Speech & Language,* v. 45, p. 326–347, 2017. DOI: https://doi.org/10.1016/j.csl.2016.11.005.

LADEFOGED, P. *Phonetic data analysis: an introduction to fieldwork and instrumental techniques.* Malden: Blackwell Publishing, 2003.

LEE, A. Using forced alignment for automatic acoustic-phonetic segmentation. *Proceedings of the International Conference on Acoustics, Speech and Signal Processing (ICASSP),* p. 1–4, 2012.

MAJOR, R. *Foreign accent: the ontogeny and phylogeny of second language phonology.* Mahwah: Lawrence Erlbaum Associates, 2001.

RAMÍREZ, J.; GÓRRIZ, J.; SEGURA, J. Voice activity detection: fundamentals and speech recognition system robustness. In: RAMÍREZ, J. (ed.). *Robust speech recognition and understanding.* Rijeka: InTech, 2007. p. 1–22.

SILVA JR., L.; BARBOSA, P. SpeechRhythmExtractor. [Programa de computador para Praat], 2019–2026. Available at: https://github.com/leonidasjr/SpeechRhythmCode.

YEGNANARAYANA, B. *Speech processing: a dynamic and optimization-oriented approach.* New York: McGraw-Hill, 1999.

YUAN, J.; LAI, W.; CIERI, C.; LIBERMAN, M. Using forced alignment for phonetics research. In: HUANG, Chu-Ren; HSIEH, Shu-Kai; JIN, Pei (eds.). *Chinese language resources.* Springer, 2023. p. 395–414. (Text, Speech and Language Technology, v. 49). DOI: https://doi.org/10.1007/978-3-031-38913-9_17.
