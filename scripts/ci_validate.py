#!/usr/bin/env python3
"""Fast repository checks; intentionally does not run population simulations."""
import csv
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_HASHES = {
    "models/two_pop_conditional_suppression_diagnostics.slim":
        "f49e03a9d63ef8ac10697aded0a8916eb0bdc735b9bf75d0a597d5f30f3aa9df",
    "models/mechanistic_within_orientation_variation.slim":
        "71124f228b292f5324b054540e45d6cf07d15ce0c316909c68a543574783ca70",
}


def check_hashes():
    for rel, expected in EXPECTED_HASHES.items():
        got = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        assert got == expected, f"hash mismatch: {rel}: {got}"


def check_manifest():
    path = ROOT / "config/mechanistic_arm_B_manifest.tsv"
    rows = list(csv.DictReader(path.open(), delimiter="\t"))
    assert len(rows) == 300
    assert len({r["task_id"] for r in rows}) == 300
    for mi, mig in enumerate(("0", "0.01", "0.05")):
        inv = [r for r in rows if r["migration_index"] == str(mi) and r["model"] == "inversion"]
        per = [r for r in rows if r["migration_index"] == str(mi) and r["model"] == "permanent_suppression"]
        assert len(inv) == len(per) == 50
        assert {r["seed"] for r in inv} == {r["seed"] for r in per}


def check_burden_identities():
    path = ROOT / "results/maintenance_baseline/analysis/endpoint_replicates.tsv"
    rows = list(csv.DictReader(path.open(), delimiter="\t"))
    assert len(rows) == 700
    for row in rows:
        for cls in ("A", "B"):
            for pop in ("p1", "p2"):
                total = float(row[f"{cls}_total_count_{pop}"])
                mean = float(row[f"{cls}_mean_count_{pop}"])
                n = float(row[f"{cls}_n_{pop}"])
                contribution = float(row[f"{cls}_pop_count_contribution_{pop}"])
                # Means are printed to three decimals; at n=2000 this can
                # create up to roughly one copy of rounding discrepancy.
                assert abs(total - mean * n) <= 1.1
                assert abs(contribution - total / 2000.0) < 0.01


def check_smoke_fixtures():
    files = sorted((ROOT / "validation/mechanistic_smoke/local_smoke").glob("*.tsv"))
    assert len(files) == 6
    for path in files:
        text = path.read_text()
        assert "PHASE_INIT\t" in text
        assert "ADAPTIVE_INIT\t" in text
        assert "LOAD\t" in text
    permanent = [p for p in files if p.name.startswith("permanent_suppression")]
    for path in permanent:
        lines = path.read_text().splitlines()
        header = next(x.split("\t") for x in lines if x.startswith("generation\t"))
        endpoints = [dict(zip(header, x.split("\t"))) for x in lines if x.startswith("1000\t")]
        assert endpoints
        assert all(float(r[k]) == 0 for r in endpoints
                   for k in ("A_recomb10", "A_recomb01", "B_recomb10", "B_recomb01"))


def check_local_links():
    for path in [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]:
        for target in re.findall(r"\]\(([^)#]+)", path.read_text()):
            if target.startswith(("http://", "https://", "codex:")):
                continue
            assert (path.parent / target).exists(), f"missing link target {target} in {path}"


if __name__ == "__main__":
    check_hashes()
    check_manifest()
    check_burden_identities()
    check_smoke_fixtures()
    check_local_links()
    print("repository validation passed")

