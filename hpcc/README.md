# MSU HPCC execution

The SLURM scripts in this directory are designed for one CPU core per task.
They do not assume a particular MSU module name: set `SLIM_MODULE` after
checking the current module tree with `check_hpcc_environment.sbatch`, or set
`SLIM_BIN` to the site-provided SLiM 5.1 executable.

From the repository root on the cluster:

```sh
export PROJECT_ROOT="$PWD"
sbatch --export=ALL,PROJECT_ROOT="$PROJECT_ROOT" hpcc/check_hpcc_environment.sbatch
sbatch --export=ALL,PROJECT_ROOT="$PROJECT_ROOT",SLIM_MODULE="<site module>" hpcc/submit_hpcc_smoke.sbatch
```

The smoke array is six tasks: matched inversion/permanent-suppression pairs at
m=0, 0.01, and 0.05. After completion, place the six outputs in
`validation/mechanistic_smoke/hpcc_smoke/` and run:

```sh
python3 hpcc/compare_smoke.py
```

Only after the comparison is identical (or a documented, diagnosed runtime
difference is resolved) should the production array be submitted:

```sh
sbatch --export=ALL,PROJECT_ROOT="$PROJECT_ROOT",SLIM_MODULE="<site module>" hpcc/submit_mechanistic_array.sbatch
```

The production request is one core, 4 GB, two days, and concurrency 50 as a
provisional starting point. These values must be replaced or confirmed using
the six-task `sacct` elapsed-time, MaxRSS, CPU-time, and failure summary.
Record the final command, job IDs, module/version output, manifest checksum,
and accounting summary with the completed result directory.

