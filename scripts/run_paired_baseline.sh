#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODEL="$ROOT/models/two_pop_conditional_suppression_diagnostics.slim"
OUT="$ROOT/results/maintenance_baseline"
MIGS="0,0.001,0.005,0.01,0.02,0.03,0.05"
REPS=50
SEED_BASE=926000
SLIM_BIN="${SLIM_BIN:-slim}"

mkdir -p "$OUT/inversion" "$OUT/permanent_suppression"
cp "$MODEL" "$OUT/model_snapshot.slim"
cp "$0" "$OUT/runner_snapshot.sh"

MODEL_SHA="$(shasum -a 256 "$MODEL" | awk '{print $1}')"
SLIM_VERSION="$($SLIM_BIN -v 2>&1 | sed -n '1p')"
{
  echo "run_start_local: $(date '+%Y-%m-%d %H:%M:%S %z')"
  echo "runner: $ROOT/scripts/run_paired_baseline.sh"
  echo "slim_bin: $SLIM_BIN"
  echo "slim_version: $SLIM_VERSION"
  echo "model: $MODEL"
  echo "model_sha256: $MODEL_SHA"
  echo "migs: $MIGS"
  echo "reps_per_model_per_migration: $REPS"
  echo "seed_base: $SEED_BASE"
  echo "shared_seed_formula: seed = SEED_BASE + migration_index * REPS + replicate"
  echo "GENS=10000 LOG_EVERY=200 N=1000 S=0.05 INV_INIT=0.5 MU_DEL=2e-7 S_DEL_MEAN=-0.05 H_DEL=0.5 INV_MAP_CM=30"
} > "$OUT/run_manifest.txt"
printf 'model\tmig\trep\tseed\tstdout\tstderr\tcommand\n' > "$OUT/run_parameters.tsv"

IFS=',' read -r -a mig_array <<< "$MIGS"
MAX_PARALLEL="${MAX_PARALLEL:-8}"

is_complete() {
  local f="$1"
  [[ -s "$f" ]] && grep -q $'^10000\tp1\t' "$f" && grep -q $'^10000\tp2\t' "$f" && grep -q $'^LOAD\t10000\tp1\tA\t' "$f" && grep -q $'^LOAD\t10000\tp2\tB\t' "$f"
}

run_pair() {
  local mi="$1" mig="$2" rep="$3" seed="$4"
  for spec in inversion permanent_suppression; do
    local flag=0
    if [[ "$spec" == "permanent_suppression" ]]; then flag=1; fi
    local dir="$OUT/$spec"
    local stdout="$dir/mig_${mig}_rep_${rep}.tsv"
    local stderr="$dir/mig_${mig}_rep_${rep}.stderr"
    if is_complete "$stdout"; then
      echo "Skipping complete $spec MIG=$mig rep=$rep seed=$seed"
      continue
    fi
    rm -f "$stdout" "$stderr"
    echo "Running $spec MIG=$mig rep=$rep seed=$seed"
    "$SLIM_BIN" -s "$seed" -d "MIG=$mig" -d CLEAN_INIT=T -d "PERMANENT_SUPPRESSION=$flag" "$MODEL" > "$stdout" 2> "$stderr"
  done
}

active=0
for mi in "${!mig_array[@]}"; do
  mig="${mig_array[$mi]}"
  for ((rep=1; rep<=REPS; rep++)); do
    seed=$((SEED_BASE + mi * REPS + rep))
    for spec in inversion permanent_suppression; do
      flag=0; if [[ "$spec" == "permanent_suppression" ]]; then flag=1; fi
      dir="$OUT/$spec"; stdout="$dir/mig_${mig}_rep_${rep}.tsv"; stderr="$dir/mig_${mig}_rep_${rep}.stderr"
      cmd="$SLIM_BIN -s $seed -d MIG=$mig -d CLEAN_INIT=T -d PERMANENT_SUPPRESSION=$flag $MODEL"
      printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$spec" "$mig" "$rep" "$seed" "$stdout" "$stderr" "$cmd" >> "$OUT/run_parameters.tsv"
    done
    run_pair "$mi" "$mig" "$rep" "$seed" &
    active=$((active + 1))
    if (( active >= MAX_PARALLEL )); then
      wait
      active=0
    fi
  done
done
wait

end_time="$(date '+%Y-%m-%d %H:%M:%S %z')"
echo "run_end_local: $end_time" >> "$OUT/run_manifest.txt"
{
  echo "completion_time: $end_time"
  echo "completed_pairs:"
  for mi in "${!mig_array[@]}"; do
    mig="${mig_array[$mi]}"
    for ((rep=1; rep<=REPS; rep++)); do
      seed=$((SEED_BASE + mi * REPS + rep))
      if is_complete "$OUT/inversion/mig_${mig}_rep_${rep}.tsv" && is_complete "$OUT/permanent_suppression/mig_${mig}_rep_${rep}.tsv"; then
        echo "  MIG=$mig rep=$rep seed=$seed"
      fi
    done
  done
  echo "failed_or_incomplete_pairs:"
  for mi in "${!mig_array[@]}"; do
    mig="${mig_array[$mi]}"
    for ((rep=1; rep<=REPS; rep++)); do
      seed=$((SEED_BASE + mi * REPS + rep))
      if ! is_complete "$OUT/inversion/mig_${mig}_rep_${rep}.tsv" || ! is_complete "$OUT/permanent_suppression/mig_${mig}_rep_${rep}.tsv"; then
        echo "  MIG=$mig rep=$rep seed=$seed"
      fi
    done
  done
} >> "$OUT/run_manifest.txt"
