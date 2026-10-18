#!/bin/bash
#SBATCH --job-name=slim_mech_smoke
#SBATCH --array=0-5
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00
#SBATCH --output=slurm_logs/smoke_%A_%a.out
#SBATCH --error=slurm_logs/smoke_%A_%a.err

set -euo pipefail
PROJECT_ROOT="${PROJECT_ROOT:?Set PROJECT_ROOT to the HPCC project directory}"
PACKAGE_ROOT="${PACKAGE_ROOT:-$PROJECT_ROOT}"
SLIM_BIN="${SLIM_BIN:-slim}"
if [[ -n "${SLIM_MODULE:-}" ]] && command -v module >/dev/null 2>&1; then module load "$SLIM_MODULE"; fi
MODEL="$PACKAGE_ROOT/models/mechanistic_within_orientation_variation.slim"
SMOKE="$PACKAGE_ROOT/validation/mechanistic_smoke/hpcc_smoke"
mkdir -p "$SMOKE" "$PACKAGE_ROOT/slurm_logs"
mi=$((SLURM_ARRAY_TASK_ID / 2)); treatment=$((SLURM_ARRAY_TASK_ID % 2))
case "$mi" in 0) mig=0;; 1) mig=0.01;; 2) mig=0.05;; esac
if (( treatment == 0 )); then model=inversion; permanent=0; else model=permanent_suppression; permanent=1; fi
seed=$((2026092801 + mi * 50))
"$SLIM_BIN" -s "$seed" -d N=1000 -d GENS=1000 -d LOG_EVERY=1000 -d "MIG=$mig" -d CLEAN_INIT=T -d "PERMANENT_SUPPRESSION=$permanent" "$MODEL" > "$SMOKE/${model}_mig_${mig}.tsv" 2> "$SMOKE/${model}_mig_${mig}.stderr"
