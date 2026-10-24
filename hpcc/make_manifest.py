#!/usr/bin/env python3
import csv
from pathlib import Path

root = Path(__file__).resolve().parents[1]
out = root / "config" / "mechanistic_arm_B_manifest.tsv"
migs = ["0", "0.01", "0.05"]
reps = 50
seed_base = 2026092800
rows = []
task = 0
for mi, mig in enumerate(migs):
    for model, flag in (("inversion", 0), ("permanent_suppression", 1)):
        for rep in range(1, reps + 1):
            seed = seed_base + mi * reps + rep
            rows.append({
                "task_id": task, "migration_index": mi, "mig": mig,
                "replicate": rep, "model": model, "permanent_suppression": flag,
                "seed": seed,
                "stdout": f"results/mechanistic_arm_b/{model}/mig_{mig}_rep_{rep}.tsv",
                "stderr": f"results/mechanistic_arm_b/{model}/mig_{mig}_rep_{rep}.stderr",
                "status": "PENDING",
            })
            task += 1
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
    w.writeheader(); w.writerows(rows)
print(f"wrote {len(rows)} tasks to {out}")
