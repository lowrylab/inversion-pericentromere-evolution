#!/usr/bin/env python3
import csv
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = root / "config" / "mechanistic_arm_B_manifest.tsv"
rows = list(csv.DictReader(manifest.open(), delimiter="\t"))
completed = failed = incomplete = 0
for r in rows:
    out = root / r["stdout"]
    err = root / r["stderr"]
    text = out.read_text(errors="ignore") if out.exists() else ""
    ok = "\n10000\tp1\t" in text and "\nLOAD\t10000\tp2\tB\t" in text
    if ok:
        status = "COMPLETE"; completed += 1
    elif err.exists() and any(x in err.read_text(errors="ignore").lower() for x in ("error", "fatal", "segmentation")):
        status = "FAILED"; failed += 1
    else:
        status = "INCOMPLETE"; incomplete += 1
    r["status"] = status
with manifest.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
    w.writeheader(); w.writerows(rows)
print(f"completed={completed} failed={failed} incomplete={incomplete} total={len(rows)}")
if failed or incomplete:
    raise SystemExit(1)
