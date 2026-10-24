# HPCC guide

The repository is prepared for MSU HPCC but has not yet been executed there.
Run `hpcc/check_hpcc_environment.sbatch` to identify the current SLiM 5.1
module or executable. Then run the six-task smoke array and compare outputs
with `validation/mechanistic_smoke/local_smoke/` before production.

The production script uses one CPU per task and a concurrency cap of 50. It
does not overwrite a task with a valid output and completion marker. Each task
writes to a temporary file, validates the expected terminal records, atomically
renames the result, and writes a `.done` marker containing task and SLURM
metadata. `hpcc/check_completion.py` writes a final status manifest only after
checking both output content and completion markers.

Resource requests remain provisional until the smoke array is benchmarked with
`sacct`. Record the SLURM job ID, array range, concurrency, module/version,
manifest checksum, MaxRSS, elapsed time, CPU time, and failures in the final
results directory.

