# Development history

The project began in the broader `slim-inversion-agent` workspace, which also
contains exploratory templates, an older full-genome ICE branch, analysis
scripts, and earlier result directories. The corrected maintenance baseline
and mechanistic Arm B work were consolidated into this repository without
modifying those original directories.

The principal scientific decisions were:

1. preserve the deliberate genotype-dependent callback;
2. use an idealized constitutive comparator rather than a detailed centromere
   model;
3. retain the 700-run perfectly coupled baseline as the orientation-maintenance
   reference;
4. add neutral within-orientation phase variation for the mechanistic test;
5. distinguish recombination-mediated burden change from selective loss of
   heavily loaded orientation haplotypes;
6. avoid equilibrium claims at 10,000 generations.

Audit notes and superseded material are under `archive/`.

