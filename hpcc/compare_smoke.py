#!/usr/bin/env python3
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
local = root / "validation" / "local_smoke"
hpcc = root / "validation" / "hpcc_smoke"
names = ["inversion_mig_0.tsv", "permanent_suppression_mig_0.tsv",
         "inversion_mig_0.01.tsv", "permanent_suppression_mig_0.01.tsv",
         "inversion_mig_0.05.tsv", "permanent_suppression_mig_0.05.tsv"]
for name in names:
    a = local / name; b = hpcc / name
    if not a.exists() or not b.exists():
        print(name, "MISSING"); continue
    ha = hashlib.sha256(a.read_bytes()).hexdigest(); hb = hashlib.sha256(b.read_bytes()).hexdigest()
    print(name, "IDENTICAL" if ha == hb else "DIFFERENT", ha, hb)
