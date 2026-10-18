# Literature-Aligned Figure Outputs

This file documents the additional figure outputs added to align with inversion-modeling literature conventions.

## Figure 1: Final Frequency vs Migration (with uncertainty)

- Script: `scripts/plot_slim_summary.py`
- Inputs: `summary.tsv` from `scripts/summarize_slim_results.py`
- Output: `migration_outcomes.png/.svg`
- Uncertainty: 95% CI around mean final A-orientation frequency for each population.

## Figure 2: Time-Series Trajectories by Migration

- Script: `scripts/plot_trajectories_by_migration.py`
- Inputs: per-run TSVs in sweep directory
- Output: `migration_trajectories.png/.svg`
- Layout: faceted panels by migration value; each panel shows mean trajectory +/- 95% CI for p1 and p2.

## Figure 3: Migration-Selection Phase Map (m x s)

- Script: `scripts/plot_phase_map.py`
- Inputs: multiple `summary.tsv` files from runs across different `s` values
- Outputs:
  - `phase_map_delta.png/.svg` (final ΔA = p1 - p2)
  - `phase_map_class.png/.svg` (outcome class: Maintained / Mixed-Eroded / Reversed)
- Note: requires an `s`-grid run set; not generated from a single fixed-`s` sweep.

## Full Pipeline (Figures 1 + 2)

`scripts/run_full_pipeline.sh` now produces both endpoint and trajectory figures automatically.

Example:

```bash
cd <source slim-inversion-agent>
bash scripts/run_full_pipeline.sh \
  --migs "0,0.001,0.005,0.01,0.05,0.1,0.2,0.3" \
  --reps 20 \
  --outdir results/full_pipeline_mig_to_0.3
```

If running in a headless environment, backend defaults are already set in the pipeline:
- `MPLBACKEND=Agg`
- `MPLCONFIGDIR=/tmp/mplconfig`
