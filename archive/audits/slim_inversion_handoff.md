# SLiM inversion analysis — handoff for ChatGPT

## Scope

Prior work is in `<source slim-inversion-agent>`. It contains two related projects:

1. A newer two-population SLiM analysis of inversions/recombination-suppressed regions under divergent selection, migration, and deleterious mutation accumulation.
2. An older full-scale *Drosophila melanogaster* ICE (interchromosomal effect) suite based on Berdan et al. (2021), with models for no recombination modification, simple inversion suppression, and ICE.

The newer two-population project is the recommended starting point for a new analysis unless the question specifically concerns full-genome ICE.

## Current model framework

Primary templates:

- `<source slim-inversion-agent>/assets/templates/two_pop_inversion_antagonistic_pleiotropy.slim`
- `<source slim-inversion-agent>/assets/templates/two_pop_pericentromeric_antagonistic_pleiotropy.slim`

The models use two Wright–Fisher populations (`p1`, `p2`) of `N=1000`, symmetric migration, and a two-chromosome layout (`L=2,000,000`; chromosome 1 contains the focal region and chromosome 2 is a control). The focal region is `[300000,700000]`, with the marker at `500000` and adaptive loci at `400000` and `600000`; the focal map length is set to 30 cM.

The A orientation carries marker `m1` plus the `p1`-favored alleles `m2` and `m3`. The B orientation carries the `p2`-favored alleles `m5` and `m6`. Selection is antagonistic at both loci: A is favored in `p1` and B in `p2`, with default `S_A=S_B=S=0.05`. Initial A frequency is 0.5 in each population. Background deleterious mutations are generated with `MU_DEL=5e-8`, dominance `H_DEL=0.5`, and a gamma DFE with mean `S_DEL_MEAN=-0.02`, shape `S_DEL_SHAPE=0.2`.

The inversion model uses corrected SLiM inversion recombination logic based on Manual §14.4: standard recombination in same-orientation homozygotes, boundary-aware handling for inverted homozygotes, and redraw until the heterokaryotype has an even number of internal breakpoints. The pericentromeric control suppresses recombination inside the focal interval in all genotypes.

The newer models log orientation frequencies, adaptive allele frequencies, total and regional deleterious load, chromosome-2 control load, A-orientation-specific burden, and cumulative A-class burden loss. The cumulative-loss metric is a logging-interval diagnostic, not a lineage-resolved reconstruction of extinct haplotypes.

## Latest completed results

Main result file:

`<source slim-inversion-agent>/results/ap_2chr_revised50_with_mig005_analysis_2026-06-09/revised50_with_mig005_summary.tsv`

The comparison includes migration values `0, 0.001, 0.005, 0.01, 0.02, 0.03, 0.05`; generally 49–50 replicates per setting, and 100 inversion/pericentromeric replicates at `m=0.05`.

At `m=0.05`:

- Inversion: final A frequency is `0.7537` in `p1` and `0.2443` in `p2`; regional A-class burden is about `227.1` and `73.5`, respectively.
- Pericentromeric: final A frequency is `0.5479` in `p1` and `0.5105` in `p2`, with very large SDs (`0.4767` and `0.4810`); among surviving A haplotypes, burden is substantially more variable than in the inversion model.
- Across low/intermediate migration, the inversion retains the expected divergent orientation pattern more consistently. Regional load comparisons must be interpreted together with A frequency because selective loss of A haplotypes can reduce the surviving-A burden in the pericentromeric model.

The combined 100-replicate endpoint summary is also available at:

`<source slim-inversion-agent>/results/ap_2chr_combined100_and_revised_analysis_2026-06-08/combined100_A_orientation_endpoint_summary.tsv`

The 50-replicate burden summary is:

`<source slim-inversion-agent>/results/ap_2chr_combined100_and_revised_analysis_2026-06-08/revised50_A_orientation_burden_summary.tsv`

Relevant figures are in those same result directories, including orientation-by-migration, deleterious-load-by-migration, total burden, cumulative loss, and diagnostic plots in PNG/SVG formats.

## Earlier two-population findings

- The original conditional-neutrality model showed a smooth migration-selection response through `m=0.3`, with A decreasing in `p1` and increasing in `p2` as migration rises.
- A direct orientation run is summarized in `<source slim-inversion-agent>/results/ab_orientation_run_mig_to_0.3/summary.tsv`.
- The 20/50-replicate comparison runs show that the pericentromeric control has much larger between-replicate variation in orientation frequencies and A-class load at intermediate migration.
- A control-chromosome analysis suggests that the focal-region burden difference is not simply a genome-wide load artifact; the chromosome-2 control is comparatively similar between models.
- A rare-invasion branch exists at `assets/templates/two_pop_inversion_rare_invasion.slim`, with strict introduction of one inversion haplotype in `p1` only when it carries both adaptive alleles. The associated analyses are under `results/invasion_*` and `results/pilot10_harmonized_*`.

## Older full-genome ICE branch

The older suite is under `<source slim-inversion-agent>/Slim_ICE-main` and includes:

- `inversion_forall_nogc-m1.slim`: no recombination modification
- `inversion_forall_nogc-m2.slim`: simple suppression inside the inversion in heterokaryotypes
- `inversion_forall_nogc-m3.slim`: ICE model with chromosome-arm-specific breakpoint thinning

It uses a full-scale *D. melanogaster* genome architecture, a roughly 5 Mb 2R inversion, a deleterious DFE, and very long runs. A small 2026 pilot comparison is in `results/dmel_ice_vs_no_ice_comparison_r5_g1000_2026-04-16`. It is not directly comparable to the newer two-population antagonistic-pleiotropy model because the genome architecture, demography, inversion introduction, fitness model, and runtime differ.

## Known caveats

- Initialization uses `addNewDrawnMutation()` in an early event, which can trigger a SLiM warning that seeded mutations may not affect fitness during that same offspring-generation cycle. This is treated as a short initialization timing offset, but it should be documented or eliminated in a future cleanup.
- The current comparisons are mostly finite-generation endpoint analyses. They do not establish long-term equilibrium.
- Migration values above 0.05 have not yet been completed for the latest antagonistic-pleiotropy/burden analysis. Literature-aligned next values are `m=0.1, 0.25, 0.4, 0.5`.
- Selection sensitivity is still needed; the current work is centered on `S=0.05`.
- The cumulative A-class burden-loss statistic depends on `LOG_EVERY` and does not track burden carried by extinct haplotypes.
- The pericentromeric comparator is a recombination-suppressed control region, not necessarily a literal centromere model.

## Recommended next questions for ChatGPT

Please first help decide which analysis question is primary:

1. Extend the antagonistic-pleiotropy inversion/pericentromeric comparison to higher migration and a selection grid.
2. Resolve whether the current deleterious-load result reflects purging within A haplotypes versus selective loss of heavily loaded A haplotypes.
3. Build a rare-invasion/capture-versus-gain experiment.
4. Return to the full-genome ICE model and design a properly powered comparison.

Before interpreting the existing figures as final biological conclusions, check the model code, run manifests, replicate counts, and endpoint definitions. Use the decision logs for literature alignment:

- `<source slim-inversion-agent>/docs/methods_decision_log.md`
- `<source slim-inversion-agent>/docs/decision_trace_human_readable.md`
- `<source slim-inversion-agent>/docs/a_orientation_time_series_tracking_plan.md`
