#!/bin/bash
#SBATCH --job-name=slim_mech_armB
#SBATCH --array=0-299%50
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=2-00:00:00
#SBATCH --output=slurm_logs/%A_%a.out
#SBATCH --error=slurm_logs/%A_%a.err

set -euo pipefail

# Set PROJECT_ROOT to the HPCC copy of the project before submission.
PROJECT_ROOT="${PROJECT_ROOT:?Set PROJECT_ROOT to the HPCC project directory}"
PACKAGE_ROOT="${PACKAGE_ROOT:-$PROJECT_ROOT}"
SLIM_BIN="${SLIM_BIN:-slim}"
if [[ -n "${SLIM_MODULE:-}" ]] && command -v module >/dev/null 2>&1; then module load "$SLIM_MODULE"; fi
MANIFEST="$PACKAGE_ROOT/config/mechanistic_arm_B_manifest.tsv"
MODEL="$PACKAGE_ROOT/models/mechanistic_within_orientation_variation.slim"
TASK_ID="${SLURM_ARRAY_TASK_ID:?SLURM_ARRAY_TASK_ID is required}"

mkdir -p "$PACKAGE_ROOT/results/mechanistic_arm_b/inversion" "$PACKAGE_ROOT/results/mechanistic_arm_b/permanent_suppression" "$PACKAGE_ROOT/slurm_logs"

row="$(awk -v id="$TASK_ID" 'NR > 1 && $1 == id {print}' "$MANIFEST")"
if [[ -z "$row" ]]; then echo "No manifest row for task $TASK_ID" >&2; exit 2; fi
IFS=$'\t' read -r task_id migration_index mig replicate model permanent seed stdout stderr status <<< "$row"

out="$PACKAGE_ROOT/$stdout"
err="$PACKAGE_ROOT/$stderr"
mkdir -p "$(dirname "$out")"
if [[ -s "$out" ]] && grep -q $'^10000\tp1\t' "$out" && grep -q $'^LOAD\t10000\tp2\tB\t' "$out"; then
  echo "COMPLETE task=$TASK_ID output=$out"
  exit 0
fi
rm -f "$out" "$err"

echo "START task=$TASK_ID model=$model mig=$mig rep=$rep seed=$seed"
"$SLIM_BIN" -s "$seed" -d "MIG=$mig" -d CLEAN_INIT=T \
  -d "PERMANENT_SUPPRESSION=$permanent" "$MODEL" > "$out" 2> "$err"
echo "END task=$TASK_ID model=$model mig=$mig rep=$rep seed=$seed"
