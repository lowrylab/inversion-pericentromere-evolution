# References

1. Haller BC, Messer PW. SLiM 5 manual. Current manual and citation guidance:
   <https://messerlab.org/slim/>.
2. Haller BC. Eidos: A Simple Scripting Language. Eidos manual and license:
   <https://benhaller.com/slim/Eidos_Manual.pdf>.
3. Haller BC, Messer PW. SLiM 3: forward genetic simulations beyond the
   Wright–Fisher model. *Bioinformatics* (2019). DOI:
   <https://doi.org/10.1093/bioinformatics/bty661>.
4. Berdan EL et al. Deleterious mutation accumulation and the long-term fate
   of chromosomal inversions. *PLoS Genetics* (2021). DOI:
   <https://doi.org/10.1371/journal.pgen.1009411>.
5. StevisonLab. *Slim_ICE*: Modeling inversions with interchromosomal effect.
   <https://github.com/StevisonLab/Slim_ICE>.

The archived legacy ICE branch also names the following empirical or historical
sources. They are preserved here so that the archive's citations are not lost;
their full-genome parameterization is not the parameterization of the current
two-population models:

6. Wang W et al. (2023). Direct estimation of *de novo* mutation rates in
   *Drosophila melanogaster*. PMID: <https://pubmed.ncbi.nlm.nih.gov/37037625/>.
7. Loewe L, Charlesworth B. (2006). Inferring the distribution of mutational
   effects on fitness in *Drosophila*. *Biology Letters* 2:426–430.
8. Sturtevant AH, Beadle GW. (1936). The relations of inversions in the X
   chromosome of *Drosophila melanogaster* to crossing over and disjunction.
   *Genetics* 21:554–604. <https://doi.org/10.1093/genetics/21.5.554>.
9. Ramel C. (1968). The effect of the curly inversions on meiosis in
   *Drosophila melanogaster*. *Hereditas* 60:211–222.
10. Koury SA. (2023). Predicting recombination suppression outside chromosomal
    inversions in *Drosophila melanogaster* using crossover interference
    theory. *Heredity* 130:196–208. <https://doi.org/10.1038/s41437-023-00593-x>.
11. Grell RF. (1978). A comparison of heat and interchromosomal effects on
    recombination and interference in *Drosophila melanogaster*. *Genetics*
    89:65–77. <https://doi.org/10.1093/genetics/89.1.65>.

The current project uses these works for simulation framework, inversion/ICE
context, and biological motivation. It does not claim to implement the
canonical Slim_ICE or conventional inversion recipe: its A/B rule is an
intentional genotype-dependent suppression model.
