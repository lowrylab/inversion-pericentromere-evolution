# Fresh audit of slim-inversion-agent

Audit scope: newer two-population antagonistic-pleiotropy project. No new simulations were launched. The audit used the current templates, scripts, raw revised-run outputs, run parameters/manifests where present, decision logs, result TSVs, representative PNGs, and the bundled SLiM 5.1 manual (last revised 12 September 2025).

## Executive finding

The main qualitative pattern is real within the existing runs: the constitutively suppressed control becomes highly variable and often fixes or loses A at intermediate/high migration, while the inversion model retains a more consistent divergent pattern. However, the present model and diagnostics do not support the stronger interpretation that the inversion itself is purging deleterious load more effectively.

Important model-specification correction: the project intentionally does **not** implement the canonical SLiM inversion recipe. The intended model is genotype-dependent suppression: A/A and B/B permit recombination within the focal interval, while A/B removes all internal breakpoints; the pericentromeric comparator removes internal breakpoints in every genotype. Therefore, the current A/B branch is directionally correct for this custom hypothesis. It must be validated directly, not replaced with the conventional even-breakpoint heterokaryotype recipe.

A standalone smoke test was added at `<audit workspace>/slim_recombination_smoke_test.slim` and run successfully under SLiM 5.1. With a deliberately high recombination rate, it produced nonzero internal breakpoint counts after the callback for inversion A/A and B/B, exactly zero for inversion A/B, and exactly zero for all three permanent-suppression genotypes. This validates the intended suppression logic at the callback level; it does not yet validate long-run haplotype outcomes.

## Evidence from the current code

### Model implementation

- The population-specific adaptive effects are implemented coherently: m2/m3 are favored in p1 and m5/m6 in p2, with multiplicative effects `exp(+S_A)`/`exp(-S_A)` per copy. Symmetric migration is set with `p1.setMigrationRates(p2, MIG)` and the reciprocal call.
- Initial A haplosomes carry m1+m2+m3; initial B haplosomes carry m5+m6. This is a clean antagonistic-pleiotropy starting state, but it is a maintenance-from-standing-variation design, not an inversion-establishment design.
- The inversion callback returns unchanged breakpoints for B/B, permits internal recombination for A/A while applying the SLiM coordinate/boundary correction, and removes all internal breakpoints for A/B. That matches the explicit custom model specification. A smoke test is still required to demonstrate zero post-callback internal breakpoints in A/B and nonzero permitted internal breakpoints in A/A and B/B.
- Initialization occurs in `1 early()` with `addNewDrawnMutation()`. In WF, offspring generation occurs after early events but before late-event fitness recalculation. The recorded SLiM warning is therefore meaningful: the seeded mutations may not affect the first offspring-generation fitness cache. This is probably a one-generation offset, but it should be removed or explicitly tested.
- The pericentromeric comparator is internally consistent as a constitutively recombination-suppressed interval, but it is not a literal centromere model. It has the same mutation rate, map rate, focal length, and DFE as the inversion scenario; only the recombination rule differs. It should be described as “permanent suppression control,” unless a realistic centromeric recombination/mutation landscape is intended.
- The two-chromosome map is internally coherent as a synthetic comparison: 1 Mb focal chromosome plus 1 Mb control chromosome, with a 0.5 boundary rate approximating independent assortment. The 400,001-bp focal interval is 20% of the 2-Mb modeled genome, not 40%.
- The deleterious DFE is gamma-distributed with `H_DEL=0.5` and negative mean. The current “load” outputs are sums of allele frequencies, hence counts/copy burden; they are not effect-weighted fitness load. Fixed m4 mutations are converted to substitutions and excluded from `sim.mutationsOfType(m4)`, so the outputs omit fixed deleterious substitutions.

### Latest run parameters

The raw revised runs under `results/ap_2chr_patch_revised_*_r50_2026-06-06` used:

- `GENS=10000`
- `INV_MAP_CM=30`
- `MU_DEL=2e-7`
- `S_DEL=0.05`, which the template converts to `S_DEL_MEAN=-0.05`
- `S=0.05`
- 50 replicates for migration 0 through 0.03, and 100 at 0.05

These are materially stronger mutation input and DFE parameters than the template defaults (`MU_DEL=5e-8`, mean `-0.02`). The latest result directory has `run_parameters.tsv` and model snapshots but no complete run manifest, so reproducibility metadata is weaker than in the earlier sweep directories.

## Independent reanalysis of raw revised runs

The existing revised raw files reproduce the reported means. At `m=0.05`:

| model | A p1 mean (SD) | A p2 mean (SD) | p1 loss/fix | p2 loss/fix |
|---|---:|---:|---:|---:|
| inversion | 0.754 (0.036) | 0.244 (0.036) | 0/0 | 0/0 |
| permanent suppression | 0.548 (0.477) | 0.510 (0.481) | 41/48 | 41/47 |

The permanent-suppression distribution is therefore a mixture of near-loss and near-fixation outcomes. Its mean is not a good description of a typical replicate.

In the raw inversion runs, A frequency, m2 frequency, and m3 frequency are exactly equal in every checked replicate at `m=0.01` and `m=0.05`. This is expected from the initial coupling plus the current all-internal-breakpoint suppression, but it means the existing adaptive-allele analysis is not independent evidence about adaptive content. The scripts also summarize only m2/m3 and omit the p2-favored m5/m6 frequencies.

The 10,000-generation endpoint is not clearly an equilibrium for load. For example, inversion A-class burden in p1 rises from about 183 at generation 8,000 to 227 at generation 10,000 at `m=0.05`; permanent-suppression burden declines from about 76 to 50 while A is being lost or fixed. This is precisely the pattern that makes endpoint conditional means hard to interpret.

## Diagnostic audit

Current definitions:

- `del_load_*`: sum of frequencies of extant m4 mutations; unweighted mutation-copy burden.
- `del_load_region_*`: same restricted to the focal interval.
- `del_load_chr2_*`: same restricted to the second 1-Mb chromosome.
- `a_del_load_region_*`: mean number of focal-region m4 mutations among surviving A haplosomes.
- `a_del_total_region_*`: total focal-region m4 copies among surviving A haplosomes.
- `a_del_burden_region_*`: A-class total divided by all haplosomes; mathematically A frequency times the conditional A-class mean.
- `cum_a_del_loss_region_*`: accumulated positive drops in A-class total between logging points.

The cumulative-loss statistic is not a purging statistic. A decline caused by loss of A haplosomes is counted exactly like loss of mutations within surviving A haplosomes; positive drops are accumulated even if later burden returns. The current diagnostic plan acknowledges this caveat, but the figures still visually invite a purging interpretation.

The `compare_deleterious_models.py` figure uses a 0.4 reference line for focal load fraction. The modeled focal region is 0.4 Mb of 2 Mb, so the corresponding geometric reference is 0.2. This plotting reference should be corrected.

## What remains supported

1. Under the current parameterization and standing-variation design, inversion-associated suppression preserves divergent A/B structure more consistently than permanent suppression through the tested migration range.
2. Permanent suppression produces a strongly bimodal/high-variance outcome distribution at higher migration; extinction/fixation frequencies are more informative than means there.
3. The model is useful for a maintenance experiment comparing conditional inversion suppression with constitutive suppression, after fixing the recombination callback and diagnostics.

## What must be softened or discarded

- Do not claim that the current inversion model uses the corrected inversion recombination recipe.
- Do not claim that lower A-class conditional burden demonstrates purging; it is confounded by A-class frequency and selective survival.
- Do not treat the permanent-suppression mean at high migration as a typical outcome.
- Do not treat A-orientation and adaptive-locus summaries as separate biological results; they are exactly coupled in the current raw runs.
- Do not generalize the latest load results across parameterizations. Earlier uDel/sDel sweeps show that orientation gaps and load penalties change substantially with mutation rate and DFE strength, and some signs reverse.

## Revised conceptual model

The clean comparison is not “inversion versus centromere load.” It is:

> Given the same two-deme antagonistic selection, migration, mutation process, interval length, and initial adaptive haplotypes, does genotype-dependent inversion recombination suppression preserve divergent haplotypes differently from constitutive recombination suppression?

That question has two separable outcomes:

1. **Adaptive maintenance:** A/B orientation and adaptive-allele differentiation across demes.
2. **Mutation consequences:** population-wide and haplotype-conditioned deleterious mutation burden, with explicit separation of within-A purging from loss of highly loaded A haplotypes.

## Recommended redesign

### A. Change immediately before new production runs

1. Preserve the deliberate genotype-dependent recombination rule. Do not replace the A/B branch with the canonical SLiM recipe. Add an explicit smoke test that records proposed and returned internal breakpoints separately for A/A, A/B, and B/B.
2. Move seeding to a controlled initialization sequence or force an explicit fitness recalculation, and test the first two generations against an equivalent delayed-seeding model.
3. Rename unweighted statistics as mutation-count/copy burden. Add effect-weighted burden and account for fixed substitutions or prevent m4 conversion to substitutions for diagnostic runs.
4. Log joint haplotype classes: A with m2/m3, B with m5/m6, recombinant marker/allele combinations, and LD between m1 and each adaptive locus.
5. Log A frequency, mean and quantiles of load among A haplosomes, unconditional A contribution, total population load, and class-size/load decomposition at every logging point.
6. Correct the focal-genome fraction reference from 0.4 to 0.2 and version the scripts that produced the June 8–9 figures.

### B. Next 3–5 analyses/runs

1. **Three-genotype recombination smoke test:** no deleterious mutations; expose A/A, A/B, and B/B parents to a high-enough map rate and log proposed versus returned internal breakpoints. The expected result is nonzero permitted internal recombination for A/A and B/B, zero returned internal breakpoints for A/B, and zero returned internal breakpoints for all pericentromeric genotypes.
2. **Revised maintenance baseline:** preserve the deliberate conditional-suppression rule, use the same current `N=1000`, `INV_INIT=0.5`, `S=0.05`, and DFE, and use matched seeds between inversion and permanent suppression. Report full endpoint distributions, not only means.
3. **Time-to-equilibrium/trajectory run:** extend the revised baseline long enough to establish whether orientation and load have plateaued; include an initial deleterious-load burn-in followed by controlled A/B seeding if maintenance, rather than origin, is the target.
4. **Small selection × migration pilot:** use at least `S={0.01,0.03,0.05,0.1}` and migration values spanning `0,0.001,0.01,0.05,0.1,0.25,0.4,0.5`. This determines whether the observed contrast is a narrow parameter effect.
5. **Rare-invasion/capture experiment:** introduce A at one or a few haplosomes on a locally adapted background, and analyze establishment probability, time to establishment, and subsequent maintenance separately from the A=0.5 experiment.

## Project-structure changes

- Treat `ap_2chr_patch_revised_*`, `ap_2chr_revised50_with_mig005_analysis_*`, and `ap_2chr_combined100_and_revised_analysis_*` as one analysis lineage, but add a manifest tying raw directories to every derived TSV/figure.
- Incorporate missing ad hoc plotting/reanalysis code into versioned scripts.
- Make antagonistic-pleiotropy models explicit defaults for AP pipelines; current general pipelines default to conditional-neutrality templates.
- Keep earlier conditional-neutrality and uDel/sDel sweeps as sensitivity evidence, but label them clearly as different model branches rather than merging them into the AP result.
