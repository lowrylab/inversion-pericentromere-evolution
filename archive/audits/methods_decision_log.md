# Inversion Model Methods Decision Log

_Date: 2026-03-02_

This document records how each literature source influenced decisions in the SLiM two-population inversion model.

## Decision Trace

| Paper | Evidence used | How it changed the model |
|---|---|---|
| Schaal, Haller, Lotterhos (2022; corrected 2025) | Two-deme inversion simulations under divergent selection; explicit migration grid `m = {0.001, 0.01, 0.1, 0.25, 0.4, 0.5}`; `N=1000` per deme; 5 replicates; long runs (60,000 generations). | Drove migration-sweep design and extension beyond low migration. Current sweep to `m <= 0.3` is treated as an intermediate stage; next stage should include `m=0.4` and `m=0.5`. Supports increasing replicate count and run length for stable inference. |
| Hager et al. (Science, 2022) | Opposite-sign selection on inversion by habitat/ecotype; methods include testing two-locus decomposition where `s_A + s_B` is fixed. | Motivated A/B orientation framing with opposite population-specific fitness effects and two additive loci within the inversion. Supports testing symmetric and asymmetric selection magnitudes across populations. |
| Harringmeyer & Hoekstra et al. (Nat Ecol Evol, 2022) | SLiM local-adaptation simulations with opposite per-population selection effects on inversion allele; broad explored `s` range. | Supports parameter-grid strategy (selection sensitivity analysis) instead of relying on a single fixed selection coefficient. |
| Mackintosh et al. (Genetics, 2024; theory) | Theory of inversion establishment/persistence under migration-selection balance; highlights capture-vs-gain dynamics. | Supports experimental staging: (1) captured adaptive content at inversion origin (current model), then (2) gained content over time as an extension. |
| SLiM Manual, inversion recipe section 14.4 and SLiM developer notes | Earlier inversion callback logic is biologically incomplete; corrected recombination callback handles homozygote-inverted boundary case and heterokaryotype even-breakpoint redraw logic. | Triggered core implementation upgrade: use corrected `recombination()` callback for inversion behavior rather than naive suppression logic. |

## Adjustments Implemented

- `A_orientation`/`B_orientation` semantics in the model.
- A favored in `p1`; B favored in `p2` through two additive loci inside inversion.
- Initial inversion frequency set to `0.5` in each population.
- Population-specific selection logic fixed (`mutationEffect` by population) to prevent wrong-direction dynamics at `m=0`.
- Corrected inversion `recombination()` callback implemented per manual section 14.4 guidance.

## Adjustments Recommended Next

1. Extend migration sweep to include `m = 0.4` and `m = 0.5`.
2. Use at least 5 replicates per parameter set.
3. Add a selection-coefficient sensitivity grid.
4. Add a second experiment block for capture-vs-gain dynamics.

## Sources

- Schaal et al. 2022: https://pmc.ncbi.nlm.nih.gov/articles/PMC9189506/
- Correction note (2025): https://pmc.ncbi.nlm.nih.gov/articles/PMC12409365/
- Hager et al. 2022 (Science): https://pmc.ncbi.nlm.nih.gov/articles/PMC9571565/
- Harringmeyer et al. 2022: https://www.nature.com/articles/s41559-022-01890-0
- Mackintosh et al. 2024: https://academic.oup.com/genetics/article/doi/10.1093/genetics/iyae073/7665473
- SLiM Manual: https://www.benhaller.com/slim/SLiM_Manual.pdf
- SLiM 3.7 inversion note: https://groups.google.com/g/slim-announce/c/gjjfqIlGd_8
