# Final smoke-test report

- Model: `models/mechanistic_within_orientation_variation.slim`
- Model SHA256: `71124f228b292f5324b054540e45d6cf07d15ce0c316909c68a543574783ca70`
- SLiM: 5.1
- N: 1000 per population
- GENS: 1000
- m: 0.01
- Seed: 20260928, matched between treatments

Initial phase records in both populations:

| orientation | 11 | 00 | 10 | 01 |
|---|---:|---:|---:|---:|
| A | 0.50 | 0.50 | 0.00 | 0.00 |
| B | 0.50 | 0.50 | 0.00 | 0.00 |

At generation 1000, inversion produced nonzero recombinant phases. The observed p1 values were A-10=0.652 and B-10=0.0405; p2 values were A-10=0.480 and B-10=0.000 in this replicate. Permanent suppression produced zero A and B recombinant phases in both populations.

Adaptive initialization was m2=m3=m5=m6=1.0 on the intended orientation classes. The source-defined fitness callbacks remain unchanged. LOAD checks passed to printed precision: total copy/effect burden equals the class mean times class count, and population contribution equals total/(2N).

The separate callback smoke test remains the direct validation that inversion A/A and B/B permit internal crossovers while A/B suppresses them; this mechanistic model uses the same callback logic exactly.
