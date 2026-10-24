# Scientific background

## Local adaptation and inversions

Inversions can preserve combinations of locally adaptive alleles by reducing
recombination between arrangements exposed to migration. The classic
two-population local-adaptation framework is Kirkpatrick and Barton (2006),
with later analysis by Charlesworth and Barton (2018). Those studies motivate
the divergent-selection and migration component of this project.

## Load, recombination, and genotype occupancy

Suppressed recombination can preserve adaptive combinations but can also link
beneficial alleles to deleterious mutations. Nickel and Foote (2026) review
this tension as a tradeoff between adaptive hitchhiking and deleterious-load
accumulation. Their conceptual contrast is especially relevant here:

1. arrangements maintained mostly in homokaryotypes may permit recombination
   and more effective purging within an arrangement;
2. arrangements maintained mostly in heterokaryotypes may experience stronger
   linkage and accumulation of deleterious variation.

Our comparison extends that question by holding selection, migration, mutation,
and map parameters fixed while comparing conditional suppression with a
constitutively suppressed comparator. The mechanistic Arm B experiment adds
neutral within-orientation phase variation so that permitted A/A and B/B
recombination can be observed directly.

Huang et al. (2022) provide empirical context: mutation-load patterns in
sunflower inversions vary with inversion heterozygosity and population
polymorphism, while the evidence for a simple universal overdominance pattern
is limited. This motivates separating genotype occupancy from burden among
surviving A and B chromosomes.

## Scope and limitation

The current deleterious-mutation dominance parameter is h=0.5. The present
experiments therefore do not directly test the strongly recessive-load regime
that can produce associative overdominance. They also do not reproduce all
mechanisms in the Nickel–Foote framework, including arbitrary dominance,
variable inversion histories, or detailed demographic and genomic structure.

The pericentromeric treatment is an idealized constitutively suppressed
interval. The inversion treatment is an idealized genotype-dependent rule:
internal recombination is allowed in A/A and B/B but completely suppressed in
A/B. These assumptions are the experimental contrast, not a claim that either
model is a complete physical description of an inversion or centromere.

## Future tests of the framework

The most informative follow-up experiments are a dominance grid including
recessive deleterious effects, a selection-by-migration grid, longer trajectory
runs, and tests with alternative initial orientation frequencies. Each should
retain the validated recombination callback and report burden conditional on
surviving haplotypes, genotype occupancy, and loss/fixation frequencies.

