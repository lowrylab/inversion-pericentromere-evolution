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
README describes a direct extension of Berdan et al. (2021) and its m2/m3
model family.

Selected historical files and their SHA256 hashes are preserved under
`archive/legacy_ice/`; they are not current production models. Because the
local legacy snapshot does not contain a standalone license file and the
available remote inspection did not establish file-level authorship for every
copy, these files are retained for audit/provenance rather than presented as
new project code. Before redistributing the archive publicly, verify the
upstream license and retain any required notices.

## Project-specific implementation

The two-population antagonistic-pleiotropy model, burden decomposition, paired
manifests, Arm B marker design, and current analyses were developed for this
project. The callback is an implementation of the declared conditional rule,
not a claim of a new recombination principle and not a canonical inversion
implementation copied from Slim_ICE. The archived templates and audit logs
show the development path and superseded alternatives.

