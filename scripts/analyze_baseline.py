#!/usr/bin/env python3
import csv
import glob
import math
import os
import re
from collections import defaultdict


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN_ROOT = os.path.join(ROOT, "results", "maintenance_baseline")
OUT = os.path.join(RUN_ROOT, "analysis")


def q(values, p):
    values = sorted(values)
    if not values:
        return float("nan")
    x = (len(values) - 1) * p
    lo = int(math.floor(x))
    hi = int(math.ceil(x))
    if lo == hi:
        return values[lo]
    return values[lo] + (values[hi] - values[lo]) * (x - lo)


def mean(values):
    return sum(values) / len(values) if values else float("nan")


def sd(values):
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / (len(values) - 1))


def parse_file(path):
    table = []
    genotype = []
    loads = []
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            if line.startswith("generation\t"):
                header = line.split("\t")
                continue
            if line.startswith("GENOTYPE\t"):
                p = line.split("\t")
                genotype.append({
                    "generation": int(p[1]), "pop": p[2], "nAA": int(p[3]), "nAB": int(p[4]),
                    "nBB": int(p[5]), "a_chrom": int(p[6]), "b_chrom": int(p[7]),
                    "A_in_AA": float(p[8]), "A_in_AB": float(p[9]),
                    "B_in_BB": float(p[10]), "B_in_AB": float(p[11]),
                })
                continue
            if line.startswith("LOAD\t"):
                p = line.split("\t")
                loads.append({
                    "generation": int(p[1]), "pop": p[2], "class": p[3], "n": int(p[4]),
                    "mean_count": float(p[5]), "median_count": float(p[6]), "q90_count": float(p[7]),
                    "total_count": float(p[8]), "pop_count_contribution": float(p[9]),
                    "mean_weight": float(p[10]), "median_weight": float(p[11]), "q90_weight": float(p[12]),
                    "total_weight": float(p[13]), "pop_weight_contribution": float(p[14]),
                })
                continue
            if "header" not in locals() or not line[0].isdigit():
                continue
            p = line.split("\t")
            if len(p) == len(header):
                row = dict(zip(header, p))
                if row.get("pop") in ("p1", "p2"):
                    row["generation"] = int(row["generation"])
                    for k, v in list(row.items()):
                        if k not in ("pop", "generation"):
                            row[k] = float(v)
                    table.append(row)
    return table, genotype, loads


def records():
    out = []
    trajectories = []
    for model in ("inversion", "permanent_suppression"):
        pattern = os.path.join(RUN_ROOT, model, "mig_*_rep_*.tsv")
        for path in sorted(glob.glob(pattern)):
            m = re.search(r"mig_([^_]+)_rep_(\d+)\.tsv$", os.path.basename(path))
            if not m:
                continue
            mig = float(m.group(1)); rep = int(m.group(2))
            table, genotype, loads = parse_file(path)
            if not table:
                continue
            endpoint = {}
            for pop in ("p1", "p2"):
                rows = [r for r in table if r["pop"] == pop]
                row = max(rows, key=lambda r: r["generation"])
                for k, v in row.items():
                    if k not in ("generation", "pop"):
                        endpoint[f"{k}_{pop}"] = v
            for pop in ("p1", "p2"):
                gl = [r for r in genotype if r["pop"] == pop]
                ll = [r for r in loads if r["pop"] == pop]
                g = max(gl, key=lambda r: r["generation"])
                for cls in ("A", "B"):
                    l = max([r for r in ll if r["class"] == cls], key=lambda r: r["generation"])
                    for k, v in l.items():
                        if k not in ("generation", "pop", "class"):
                            endpoint[f"{cls}_{k}_{pop}"] = v
                for k, v in g.items():
                    if k not in ("generation", "pop"):
                        endpoint[f"{k}_{pop}"] = v
            row = {"model": model, "mig": mig, "rep": rep}
            row.update(endpoint)
            row["A_loss_p1"] = int(endpoint["A_freq_p1"] <= 0.05)
            row["A_fix_p1"] = int(endpoint["A_freq_p1"] >= 0.95)
            row["A_loss_p2"] = int(endpoint["A_freq_p2"] <= 0.05)
            row["A_fix_p2"] = int(endpoint["A_freq_p2"] >= 0.95)
            row["divergent"] = int(endpoint["A_freq_p1"] >= 0.75 and endpoint["A_freq_p2"] <= 0.25)
            out.append(row)
            for r in table:
                trajectories.append({"model": model, "mig": mig, "rep": rep, **r})
            for r in genotype:
                trajectories.append({"model": model, "mig": mig, "rep": rep, "kind": "GENOTYPE", **r})
            for r in loads:
                trajectories.append({"model": model, "mig": mig, "rep": rep, "kind": "LOAD", **r})
    return out, trajectories


def write_tsv(path, rows, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def summarize(rows):
    fields = sorted({k for r in rows for k in r})
    write_tsv(os.path.join(OUT, "endpoint_replicates.tsv"), rows, fields)
    metrics = [
        "A_freq_p1", "A_freq_p2", "A_mean_count_p1", "A_mean_count_p2",
        "A_median_count_p1", "A_median_count_p2", "A_q90_count_p1", "A_q90_count_p2",
        "A_pop_count_contribution_p1", "A_pop_count_contribution_p2",
        "A_mean_weight_p1", "A_mean_weight_p2", "A_pop_weight_contribution_p1", "A_pop_weight_contribution_p2",
        "pop_region_copy_burden_p1", "pop_region_copy_burden_p2",
        "pop_region_weighted_burden_p1", "pop_region_weighted_burden_p2",
        "A_in_AA_p1", "A_in_AB_p1", "A_in_AA_p2", "A_in_AB_p2",
    ]
    summary = []
    for model in ("inversion", "permanent_suppression"):
        for mig in sorted({r["mig"] for r in rows if r["model"] == model}):
            sub = [r for r in rows if r["model"] == model and r["mig"] == mig]
            for metric in metrics:
                vals = [r[metric] for r in sub]
                summary.append({"model": model, "mig": mig, "metric": metric, "n": len(vals),
                                "mean": mean(vals), "sd": sd(vals), "q10": q(vals, .1),
                                "median": q(vals, .5), "q90": q(vals, .9)})
            for metric in ("A_loss_p1", "A_fix_p1", "A_loss_p2", "A_fix_p2", "divergent"):
                vals = [r[metric] for r in sub]
                summary.append({"model": model, "mig": mig, "metric": metric, "n": len(vals),
                                "mean": mean(vals), "sd": sd(vals), "q10": q(vals, .1),
                                "median": q(vals, .5), "q90": q(vals, .9)})
    write_tsv(os.path.join(OUT, "endpoint_summary.tsv"), summary,
              ["model", "mig", "metric", "n", "mean", "sd", "q10", "median", "q90"])

    paired = []
    keys = {(r["mig"], r["rep"]) for r in rows}
    for mig, rep in sorted(keys):
        inv = next((r for r in rows if r["model"] == "inversion" and r["mig"] == mig and r["rep"] == rep), None)
        peri = next((r for r in rows if r["model"] == "permanent_suppression" and r["mig"] == mig and r["rep"] == rep), None)
        if inv is None or peri is None:
            continue
        for metric in ("A_freq_p1", "A_freq_p2", "A_pop_count_contribution_p1", "A_pop_count_contribution_p2",
                       "A_mean_count_p1", "A_mean_count_p2", "pop_region_copy_burden_p1", "pop_region_copy_burden_p2"):
            paired.append({"mig": mig, "rep": rep, "metric": metric,
                           "inversion": inv[metric], "permanent_suppression": peri[metric],
                           "difference_inv_minus_permanent": inv[metric] - peri[metric]})
    write_tsv(os.path.join(OUT, "paired_replicate_differences.tsv"), paired,
              ["mig", "rep", "metric", "inversion", "permanent_suppression", "difference_inv_minus_permanent"])


def trajectory_summary(trajectories):
    rows = []
    for model in ("inversion", "permanent_suppression"):
        for mig in (0.0, 0.01, 0.05):
            sub = [r for r in trajectories if r["model"] == model and r["mig"] == mig and "A_freq" in r]
            for gen in sorted({r["generation"] for r in sub}):
                for pop in ("p1", "p2"):
                    vals = [r["A_freq"] for r in sub if r["generation"] == gen and r["pop"] == pop]
                    if vals:
                        rows.append({"model": model, "mig": mig, "generation": gen, "pop": pop,
                                     "metric": "A_freq", "n": len(vals), "mean": mean(vals),
                                     "q10": q(vals,.1), "median": q(vals,.5), "q90": q(vals,.9)})
            load = [r for r in trajectories if r["model"] == model and r["mig"] == mig and r.get("kind") == "LOAD" and r["class"] == "A"]
            for gen in sorted({r["generation"] for r in load}):
                for pop in ("p1", "p2"):
                    vals = [r["mean_count"] for r in load if r["generation"] == gen and r["pop"] == pop]
                    if vals:
                        rows.append({"model": model, "mig": mig, "generation": gen, "pop": pop,
                                     "metric": "A_mean_count", "n": len(vals), "mean": mean(vals),
                                     "q10": q(vals,.1), "median": q(vals,.5), "q90": q(vals,.9)})
    write_tsv(os.path.join(OUT, "trajectory_summary.tsv"), rows,
              ["model", "mig", "generation", "pop", "metric", "n", "mean", "q10", "median", "q90"])


def plots(rows, trajectories):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return
    os.makedirs(OUT, exist_ok=True)
    for mig in sorted({r["mig"] for r in rows}):
        fig, ax = plt.subplots(figsize=(8, 5))
        for model, color, marker in (("inversion", "#1f77b4", "o"), ("permanent_suppression", "#d62728", "s")):
            for pop, ls in (("p1", "-"), ("p2", "--")):
                vals = [r[f"A_freq_{pop}"] for r in rows if r["model"] == model and r["mig"] == mig]
                xs = [i for i in range(len(vals))]
                ax.scatter(xs, vals, color=color, marker=marker, alpha=.45, s=18, label=f"{model} {pop}")
        ax.set_title(f"Endpoint A frequency distribution, MIG={mig:g}")
        ax.set_xlabel("Replicate index"); ax.set_ylabel("A frequency"); ax.set_ylim(0, 1); ax.grid(alpha=.25)
        ax.legend(frameon=False, ncol=2)
        fig.tight_layout(); fig.savefig(os.path.join(OUT, f"endpoint_distribution_mig_{mig:g}.png"), dpi=180); plt.close(fig)


def main():
    rows, trajectories = records()
    if not rows:
        raise SystemExit("No completed raw records found")
    summarize(rows)
    trajectory_summary(trajectories)
    plots(rows, trajectories)
    print(f"Analyzed {len(rows)} replicate-model records")


if __name__ == "__main__":
    main()
