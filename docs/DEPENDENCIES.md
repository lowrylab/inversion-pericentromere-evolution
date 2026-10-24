# Dependencies

## Required for repository checks

- Python 3.9 or newer, using only the standard library for validation and
  compact-table analysis.
- Git.

## Required for baseline simulation and figures

- SLiM 5.1, including the `slim` executable.
- R and the base graphics package for `scripts/make_baseline_figures.R`.

## Optional

- SLURM and the site-specific SLiM 5.1 module on MSU HPCC.
- `sacct` for resource accounting after HPCC jobs.

GitHub Actions intentionally runs syntax, manifest, hash, burden-accounting,
documentation-link, and smoke-fixture checks only. It does not run expensive
population simulations and reports SLiM-dependent execution as a separate
local/HPCC responsibility.

