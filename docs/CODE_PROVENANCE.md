# Code provenance

## Current scientific model

The authoritative current models are the two files in `models/`. The corrected
maintenance model is the version used for the completed 700-run baseline.
Mechanistic Arm B is the same validated conditional/permanent callback logic
with neutral within-orientation markers and diagnostic phase records. Exact
SHA256 values are in `config/model_hashes.tsv`.

The defining recombination rule is the declared implementation choice for this
project: inversion A/A and B/B allow internal recombination, inversion A/B
suppresses all internal breakpoints, and the permanent comparator suppresses
internal breakpoints in every genotype. Similar heterokaryotype-suppression
assumptions occur in earlier inversion models; this repository does not claim
to have invented that assumption. The Arm B phase smoke test documents the
implemented behavior.

## Relationship to Slim_ICE and Berdan et al.

The local `slim-inversion-agent/Slim_ICE-main` material and the public
StevisonLab/Slim_ICE repository were used as conceptual and historical context
for inversion markers, model organization, and the distinction between simple
inversion suppression and genome-wide interchromosomal effects. The public
README describes a direct extension of Berdan et al. (2021) and its m1/m2/m3
model family. It identifies Laurie Stevison as the author of the SLiM models,
with computational work and summarized outputs, and credits collaboration
with Spencer Koury. Those contributions are acknowledged here rather than
collapsed into a generic statement of conceptual influence.

The local and current public repositories were compared at public commit
`73fdcba3fcb673ee85f70cec51aff770d308c382`. All 14 code/driver files checked
are byte-for-byte identical; the local README is an older version of the
public README. The hashes and comparison scope are recorded in
`archive/legacy_ice/FILE_HASH_COMPARISON.tsv`.

The source files themselves are not redistributed in this initial release.
The public GitHub repository has no machine-readable license file; its README
states MIT, while the associated Zenodo metadata reports CC-BY-4.0. The
conflict is a publication blocker for redistributing those files, so this
repository retains only the comparison, attribution, and upstream link under
`archive/legacy_ice/`. The original private working directory remains the
location of the archived source files.

The upstream README requests citation of Berdan et al. (2021), the empirical
parameter sources, and the Zenodo release `10.5281/zenodo.20170793`. Those
requirements are reflected in `docs/REFERENCES.md` and
`docs/CITATION_GUIDE.md`.

## Project-specific implementation

The two-population antagonistic-pleiotropy model, burden decomposition, paired
manifests, Arm B marker design, and current analyses were developed for this
project. The callback is an implementation of the declared conditional rule,
not a claim of a new recombination principle and not a canonical inversion
implementation copied from Slim_ICE. The archived templates and audit logs
show the development path and superseded alternatives.

