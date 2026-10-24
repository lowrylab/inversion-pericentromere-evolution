# Genotype-dependent recombination suppression and linked selection

This repository contains the reproducible SLiM implementation and compact
results for a two-population comparison of a genotype-dependent inversion
model with a constitutively suppressed pericentromeric comparator.

## Biological question

The model asks whether conditional linkage can maintain locally adaptive
haplotypes under migration while still permitting recombination-mediated
release from linked deleterious burden in homozygotes.

The inversion model is deliberately non-canonical:

* A/A: internal recombination is allowed.
* A/B: every internal breakpoint is removed; recombination is completely
  suppressed.
* B/B: internal recombination is allowed.

The pericentromeric comparator removes all internal breakpoints in A/A, A/B,
and B/B. It therefore represents constitutive suppression, not a canonical
SLiM inversion implementation. The adaptive loci are m2/m3 on the A class
and m5/m6 on the B class. The mechanistic arm adds neutral linked markers
m7/m8 and m9/m10 to create within-orientation variation without changing
fitness.

The pericentromeric treatment is an idealized constitutively suppressed
interval, not a detailed physical model of centromere biology. The
genotype-dependent rule is an intentional model specification; it should not
be described as the canonical SLiM inversion recipe.

## Model and experiments

The two populations exchange migrants and experience reciprocal antagonistic
selection. Both orientations begin at frequency 0.5 in each population. The
completed maintenance baseline contains 7 migration values, 50 matched
replicates per value, and two suppression treatments: 700 runs total. Its
compact endpoint and trajectory outputs are in `results/maintenance_baseline/`.

Mechanistic Arm B uses the same N, selection, mutation model, DFE, map, focal
interval, and validated recombination callback. It is prepared for 300 paired
HPCC tasks at m = 0, 0.01, and 0.05. The local production smoke gate passed;
the six-task MSU smoke array and 300-task production array remain pending
until an MSU HPCC login/module environment is available.

The baseline supports orientation-maintenance and selective-loss conclusions,
but its adaptive markers are perfectly coupled within orientation. The
mechanistic arm is intended to test actual recombination-mediated uncoupling.
Neither 10,000 generations nor the baseline load trajectories should be
described as an established equilibrium.

The current deleterious mutation dominance parameter is h=0.5. This project
therefore does not directly test the strongly recessive-load conditions under
which associative overdominance may arise. See
`docs/SCIENTIFIC_BACKGROUND.md` for the conceptual comparison and future
experiments.

## Repository map

* `models/`: exact validated production models.
* `scripts/`: baseline and Arm B analysis entry points.
* `hpcc/`: self-contained SLURM scripts, manifest generation, completion
  checking, and local-versus-HPCC smoke comparison.
* `config/`: model hashes, parameter records, and task-manifest metadata.
* `results/`: compact derived tables, provenance, and smoke outputs; large raw
  production outputs are intentionally excluded.
* `figures/`: figures generated from the included compact baseline tables.
* `docs/`: reproducibility, provenance, references, audit, and AI disclosure.
* `archive/`: selected historical audits and legacy ICE materials, clearly
  separated from the current model.

## Citation and reuse

If you use code, simulation models, analytical workflows, or other materials
from this repository in a scientific publication, please cite this repository
and any associated research publication.

This repository builds upon previous theoretical and computational work,
including StevisonLab/Slim_ICE and Berdan et al. (2021). Researchers using
these materials should also cite the relevant original sources identified in
`docs/REFERENCES.md` and `docs/CODE_PROVENANCE.md`.

We encourage researchers who adapt or extend these models to acknowledge the
original computational contributions and clearly document their modifications.

This scholarly request for citation is distinct from the legal permissions of
the MIT license. See `docs/CITATION_GUIDE.md`.

## Reproduction

Run commands from the repository root. The baseline model requires SLiM 5.1
and the baseline runner can be inspected or run with:

```sh
./scripts/run_paired_baseline.sh
python3 scripts/analyze_baseline.py
Rscript scripts/make_baseline_figures.R
```

The Arm B manifest is `results/mechanistic_arm_b/mechanistic_arm_B_manifest.tsv`.
On MSU HPCC, copy the repository to a project/scratch location, load SLiM in
the job environment, run the six-task smoke array, compare it with the
included local smoke files, and only then submit the production array. See
`docs/REPRODUCIBILITY.md` and `hpcc/README.md` for the exact sequence.

## Current findings and limits

The corrected baseline shows more stable maintenance of the locally favored
orientation under conditional suppression, whereas constitutive suppression
has a high-variance mixture of orientation loss and fixation at higher
migration. The lower mean burden in the constitutive treatment is partly
explained by selective loss of highly loaded A haplotypes. The baseline does
not demonstrate adaptive-marker uncoupling because it starts with perfectly
coupled within-orientation adaptive markers. Arm B addresses that limitation
with neutral within-orientation phase variation.

## Provenance and disclosure

David B. Lowry directed the scientific questions, model assumptions,
interpretation, and final decisions. ChatGPT assisted with experimental
planning, scientific reasoning, and review. Codex assisted with model
implementation, validation, computational execution, and reproducibility
auditing. AI tools are not authors. See `docs/CODE_PROVENANCE.md`,
`docs/REFERENCES.md`, and `docs/AI_DISCLOSURE.md`.

