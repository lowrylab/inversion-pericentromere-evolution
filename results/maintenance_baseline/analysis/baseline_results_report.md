# Corrected maintenance baseline results

## A. Completion and QA

All 700 treatment runs completed: 7 migration values × 50 replicates × 2 models. The manifest records completion at 2026-09-28 06:53:57 -0400, SLiM 5.1, model SHA256 `f49e03a9d63ef8ac10697aded0a8916eb0bdc735b9bf75d0a597d5f30f3aa9df`, parameter values, seeds, completed pairs, and an empty failed/incomplete section.

The production callback remains the requested model: inversion A/A and B/B allow internal recombination, inversion A/B removes all internal breakpoints, and permanent suppression removes internal breakpoints in all genotype states. The direct smoke test remains the implementation validation.

Raw-to-summary checks passed for 700 endpoint records, 700 paired records per requested endpoint metric, and 1,200 trajectory summaries. For every endpoint, A-class total copy/effect burden agrees with class mean × class haplotype count, and population contribution agrees with class total divided by 2N. Fixed m4 substitutions are included in these measures and are emitted in `FIXED` records. The focal interval is 0.4 Mb of a 2 Mb chromosome, so the reference fraction is 0.2.

One important QA result is negative: m2 and m3 remain identical at every endpoint, and m5 and m6 remain identical at every endpoint. This is not evidence that the A/A or B/B callback failed. The initial A and B haplotypes carry perfectly coupled adaptive marker pairs, and there is no segregating within-orientation adaptive-marker variation for permitted homozygote recombination to separate. Consequently, adaptive-marker differentiation and LD are redundant with orientation in this baseline; this is a design limitation for the requested introgression test.

## B. Adaptive maintenance

Endpoint mean A frequencies (p1; p2 is the reciprocal B-adapted population pattern) were:

| m | inversion p1 | permanent p1 | inversion p2 | permanent p2 |
|---:|---:|---:|---:|---:|
| 0 | 1.000 | 1.000 | 0.000 | 0.000 |
| .001 | .993 | .899 | .007 | .013 |
| .005 | .969 | .893 | .030 | .081 |
| .01 | .939 | .752 | .064 | .152 |
| .02 | .888 | .656 | .115 | .279 |
| .03 | .830 | .621 | .169 | .475 |
| .05 | .762 | .498 | .251 | .468 |

The inversion preserves the locally favored orientation substantially better, especially in the high-migration tail. Permanent suppression becomes highly dispersed: at m=.05, p1 A-loss frequency is .46 and A-fixation frequency is .44; the corresponding p2 values are also .46 and .44. Inversion has no A-loss events by the endpoint threshold at m≥.02 and retains a much narrower distribution.

## C. Burden results

In p1, mean conditional A-class copy burden for inversion is approximately 291–303 across m=.001–.05. Permanent suppression is much more variable: approximately 372 at m=.001, 378 at .005, 334 at .01, 309 at .02, 274 at .03, and 218 at .05. The permanent-suppression mean is therefore not a simple purifying-selection advantage; it mixes surviving high-load A classes with replicates in which A has been lost or nearly lost.

Inversion population-wide focal burden remains near 285–303 copies per haplosome-equivalent p1 endpoint. Permanent suppression falls from approximately 402 at m=.001 to 387 at m=.05, but with a broad mixture of near-loss and near-fixation states. The chromosome-2 control should be interpreted alongside these values rather than as an isolated absolute reference.

## D. Evidence for a recombination-mediated burden effect

The baseline provides limited direct evidence for homozygote recombination-mediated purging because the adaptive-marker haplotypes are initially identical within each orientation and recombinant classes remain zero. The conditional inversion does, however, show a stable within-A burden distribution while adaptive orientation is maintained, consistent with protection of the locally favored class without the extreme collapse seen under constitutive suppression.

The correct causal diagnostic remains the joint comparison of within-class burden, A/A versus A/B occupancy, and recombinant classes. In this baseline, the recombinant-class component is uninformative because no within-orientation adaptive-marker variation was supplied.

## E. Evidence for selective loss of highly loaded A haplotypes

Selective loss is strongly supported in the permanent model. Across migration values, A frequency and conditional A burden are highly correlated among replicates (approximately r=.91–.96 for m=.001–.05 in p1), and A-frequency variance becomes very large. This means the lower mean A burden at high migration is substantially driven by which A classes survive, not solely by lower burden among otherwise comparable A haplotypes.

The inversion shows near-zero correlation between A frequency and conditional A burden across replicates (approximately |r|<.2), while A frequency tracks the A/A occupancy proportion. This is more consistent with orientation-frequency change without strong selective truncation of the surviving A burden distribution.

## F. Trajectory and unexpected results

Ten-thousand generations should not be called equilibrium. In inversion p1, mean A burden rose from approximately 239 to 295 between generations 8,000 and 10,000 at m=0, from 238 to 293 at m=.01, and from 245 to 302 at m=.05. Permanent suppression also changed substantially: from 313 to 390 at m=0, 323 to 334 at m=.01, and 203 to 218 at m=.05. These trajectories are still moving toward, but do not establish, a plateau.

The most important unexpected result is that permitted A/A and B/B recombination did not produce adaptive-marker recombinants. The callback is functioning, but the marker initialization makes the adaptive-locus comparison effectively an orientation comparison. m5/m6 are tracked correctly and are likewise perfectly coupled.

## G. Recommended next experiment

Do not begin the selection × migration grid or rare-invasion experiment yet. First add controlled within-orientation adaptive-haplotype variation or a neutral marker configuration that allows A/A and B/B recombination to generate measurable recombinant classes, while keeping the validated recombination callback unchanged. Then repeat a smaller paired diagnostic run at m=0, .01, and .05 to test whether homozygote recombination produces actual burden release. Treat the present baseline as the orientation-maintenance and selective-loss reference.

## Outputs

- [Endpoint replicate table](endpoint_replicates.tsv)
- [Endpoint summaries](endpoint_summary.tsv)
- [Matched replicate differences](paired_replicate_differences.tsv)
- [Trajectory summaries](trajectory_summary.tsv)
- [Endpoint figures](endpoint_distribution_mig_0.png)
- [Trajectory figures](trajectory_summary_mig_0.01.png)
