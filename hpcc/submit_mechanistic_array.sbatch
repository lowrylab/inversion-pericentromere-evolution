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
done_marker="$out.done"
if [[ -s "$out" && -s "$done_marker" ]] && grep -q $'^10000\tp1\t' "$out" && grep -q $'^LOAD\t10000\tp2\tB\t' "$out"; then
  echo "COMPLETE task=$TASK_ID output=$out"
  exit 0
fi

tmpout="$out.tmp.${SLURM_JOB_ID:-local}.${TASK_ID}"
tmperr="$err.tmp.${SLURM_JOB_ID:-local}.${TASK_ID}"
rm -f "$tmpout" "$tmperr"
trap 'rm -f "$tmpout" "$tmperr"' EXIT

echo "START task=$TASK_ID model=$model mig=$mig rep=$rep seed=$seed"
"$SLIM_BIN" -s "$seed" -d "MIG=$mig" -d CLEAN_INIT=T \
  -d "PERMANENT_SUPPRESSION=$permanent" "$MODEL" > "$tmpout" 2> "$tmperr"
if ! grep -q $'^10000\tp1\t' "$tmpout" || ! grep -q $'^LOAD\t10000\tp2\tB\t' "$tmpout"; then
  echo "INCOMPLETE task=$TASK_ID: expected terminal records were not found" >&2
  exit 3
fi
mv "$tmpout" "$out"
mv "$tmperr" "$err"
{
  echo "task_id=$task_id"
  echo "slurm_job_id=${SLURM_JOB_ID:-unknown}"
  echo "slurm_array_task_id=${SLURM_ARRAY_TASK_ID:-unknown}"
  echo "seed=$seed"
  echo "model=$model"
  echo "output_sha256=$(shasum -a 256 "$out" | awk '{print $1}')"
  echo "completion_time=$(date '+%Y-%m-%d %H:%M:%S %z')"
} > "$done_marker"
echo "END task=$TASK_ID model=$model mig=$mig rep=$rep seed=$seed"
