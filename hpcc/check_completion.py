#!/usr/bin/env python3
import csv
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = root / "config" / "mechanistic_arm_B_manifest.tsv"
rows = list(csv.DictReader(manifest.open(), delimiter="\t"))
completed = failed = incomplete = 0
for r in rows:
    out = root / r["stdout"]
    err = root / r["stderr"]
    marker = root / (r["stdout"] + ".done")
    text = out.read_text(errors="ignore") if out.exists() else ""
    ok = marker.exists() and "\n10000\tp1\t" in text and "\nLOAD\t10000\tp2\tB\t" in text
    if ok:
        status = "COMPLETE"; completed += 1
    elif err.exists() and any(x in err.read_text(errors="ignore").lower() for x in ("error", "fatal", "segmentation")):
        status = "FAILED"; failed += 1
    else:
        status = "INCOMPLETE"; incomplete += 1
    r["status"] = status
final_manifest = root / "results" / "mechanistic_arm_b" / "final_manifest.tsv"
final_manifest.parent.mkdir(parents=True, exist_ok=True)
with final_manifest.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
    w.writeheader(); w.writerows(rows)
with (final_manifest.with_suffix(".metadata.txt")).open("w") as f:
    f.write(f"check_time_utc={datetime.now(timezone.utc).isoformat()}\n")
    f.write(f"completed={completed}\nfailed={failed}\nincomplete={incomplete}\ntotal={len(rows)}\n")
print(f"completed={completed} failed={failed} incomplete={incomplete} total={len(rows)} final_manifest={final_manifest}")
if failed or incomplete:
    raise SystemExit(1)
