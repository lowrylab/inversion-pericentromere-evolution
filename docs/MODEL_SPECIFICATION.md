# Model specification

## Shared architecture

The production models use two populations of N=1000, reciprocal divergent
selection at adaptive loci m2/m3 and m5/m6, migration, a 2 Mb chromosome, a
300–700 kb focal interval, a 30 cM focal map length, mutation rate 2e-7 for
deleterious mutations, gamma-shaped deleterious effects with mean -0.05 and
shape 0.2, and h=0.5. The initial A frequency is 0.5 in both populations.

The focal interval is 0.4 Mb of a 2 Mb chromosome, so its physical reference
fraction is 0.2. Fixed deleterious substitutions are included in the burden
metrics through the model's `FIXED` accounting.

## Recombination treatments

The inversion callback removes all internal focal-region breakpoints only for
A/B individuals. A/A and B/B individuals retain normal internal recombination.
The permanent-suppression comparator removes internal focal-region breakpoints
for all three genotype classes. This is an intentional idealized comparison;
the inversion model is not the canonical SLiM inversion implementation.

## Model versions

The exact files and SHA256 values are recorded in `config/model_hashes.tsv`.
The completed maintenance baseline uses the conditional-suppression model.
Mechanistic Arm B adds neutral within-orientation markers and diagnostic phase
records without changing the validated recombination rule or fitness model.

