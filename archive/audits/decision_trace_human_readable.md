# Decision Trace: Paper -> Evidence -> Model Adjustment

| Paper | Evidence (What was taken from the paper) | Model adjustment (What changed in your SLiM setup) |
|---|---|---|
| **Schaal, Haller, Lotterhos (2022; corrected 2025)** | Two-deme inversion simulations under divergent selection and migration; explicit migration grid (`m = 0.001, 0.01, 0.1, 0.25, 0.4, 0.5`); `N = 1000` per deme; replicate-based analysis and long simulation horizons. | Anchored migration-sweep design. Your `m <= 0.3` sweep is treated as an intermediate phase; next phase should include `m = 0.4` and `m = 0.5`. Also supports increasing replicate count and (if needed) generation length for stability. |
| **Hager et al. (Science, 2022)** | Opposite-sign selection on inversion by habitat/ecotype; methods include a two-locus decomposition perspective (`s_A + s_B` fixed in tests). | Justified your A/B orientation framing and the requirement that fitness differences are caused by **two additive loci inside the inversion**. Supports testing both symmetric and asymmetric selection magnitudes across populations. |
| **Harringmeyer & Hoekstra et al. (Nature Ecology & Evolution, 2022)** | SLiM-based local adaptation simulations with opposite selection across populations and broad selection ranges rather than one fixed effect size. | Motivated sensitivity-grid strategy: run multiple selection strengths, not a single `s`. This informs the next expansion beyond the baseline run configuration. |
| **Mackintosh et al. (Genetics, 2024; theory-focused)** | Theory emphasizes migration-selection balance and distinguishes inversion dynamics from captured vs newly gained adaptive content. | Supports a staged plan: first analyze the current “captured adaptive loci” model, then add a follow-up model where adaptive content can accumulate inside the inversion over time. |
| **SLiM Manual §14.4 + SLiM developer notes** | Legacy inversion callback logic is biologically incomplete; corrected `recombination()` logic handles homozygote-inverted breakpoint boundaries and heterokaryotype even-breakpoint constraints via redraw. | Triggered the key technical change: your model now uses the corrected inversion `recombination()` callback instead of naive suppression logic, improving biological validity at inversion boundaries and in heterokaryotypes. |

## Status Summary

- Implemented in your current model:
  - A/B orientation semantics.
  - Opposite population-specific selection through two additive loci inside inversion.
  - Initial inversion frequency `0.5` in each population.
  - Population-specific selection correction to avoid wrong-direction dynamics at `m=0`.
  - Corrected inversion `recombination()` callback behavior.

- Next literature-aligned extensions:
  1. Extend migration sweep to include `m = 0.4` and `0.5`.
  2. Use at least 5 replicates per setting.
  3. Run a selection-coefficient sensitivity grid.
  4. Add capture-vs-gain experiment block.
