# Claims and evidence

This document separates results demonstrated by the completed baseline from
mechanistic interpretations that remain hypotheses.

| Claim | Status | Evidence | Interpretation |
|---|---|---|---|
| Conditional suppression maintains the locally favored orientation better at higher migration in the completed baseline. | Demonstrated for this parameterization | `results/maintenance_baseline/analysis/endpoint_summary.tsv`; `baseline_results_report.md`; endpoint figures | This is a result for N=1000, S=0.05, h=0.5, the specified DFE, seven migration values, and 50 paired replicates. |
| Constitutive suppression has a high-variance mixture of orientation loss and fixation at high migration. | Demonstrated for this parameterization | Endpoint distributions and loss/fixation metrics in `endpoint_summary.tsv` and `baseline_results_report.md` | Report distributions and event frequencies, not only means. |
| Lower constitutive-treatment burden can result from selective loss of highly loaded A haplotypes. | Supported by replicate-level association | `results/maintenance_baseline/analysis/baseline_results_report.md`; `endpoint_replicates.tsv`; `paired_replicate_differences.tsv` | This is evidence for selective truncation as a contributor, not proof that purifying selection is stronger. |
| The baseline demonstrates recombination-mediated purging. | Not demonstrated | Baseline starts with perfectly coupled within-orientation adaptive markers; m2/m3 and m5/m6 remain redundant. | The baseline callback is validated, but the baseline lacks variation that would make adaptive uncoupling informative. |
| The Arm B smoke test demonstrates that conditional recombination can create neutral recombinant phases. | Demonstrated in a short smoke test | `validation/mechanistic_smoke/final_smoke_report.md` and local smoke fixtures | This validates observable recombination and output accounting, not long-run purging. |
| Arm B will show lower-burden recombinant adaptive haplotypes. | Hypothesis under investigation | No Arm B production runs are included yet | Requires the HPCC smoke comparison and all 300 production tasks. |
| The load process is equilibrated by generation 10,000. | Rejected | `trajectory_summary.tsv` and baseline report | Trajectories are still changing between 8,000 and 10,000 generations. |

The repository should not describe neutral recombinant phases alone as evidence
of purging. Purging requires a reduction in burden among comparable surviving
adaptive haplotypes, supported by burden distributions, ancestry/background,
and genotype-state conditioning.

