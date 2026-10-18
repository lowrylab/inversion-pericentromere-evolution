#!/usr/bin/env python3
import csv, glob, os, re, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN_ROOT = ROOT / "results" / "mechanistic_arm_b"
OUT = RUN_ROOT / "analysis"
OUT.mkdir(exist_ok=True)

def parse(path):
    table=[]; geno=[]; loads=[]; header=None
    for line in open(path):
        p=line.rstrip("\n").split("\t")
        if p[0]=="generation": header=p
        elif p[0]=="GENOTYPE": geno.append(p)
        elif p[0]=="LOAD": loads.append(p)
        elif header and p[0].isdigit() and len(p)==len(header):
            d=dict(zip(header,p))
            for k,v in list(d.items()):
                if k=="generation": d[k]=int(v)
                elif k!="pop": d[k]=float(v)
            table.append(d)
    return table,geno,loads

def complete(table): return bool(table) and max(r["generation"] for r in table)==10000

files=[]
for model in ("inversion","permanent_suppression"):
    for path in sorted(glob.glob(str(RUN_ROOT/model/"mig_*_rep_*.tsv"))):
        m=re.search(r"mig_([^_]+)_rep_(\d+)\.tsv$",path)
        if m: files.append((model,float(m.group(1)),int(m.group(2)),Path(path)))

end=[]; traj=[]
for model,mig,rep,path in files:
    table,geno,loads=parse(path)
    if not complete(table): continue
    for r in table: traj.append({"model":model,"mig":mig,"rep":rep,**r})
    row={"model":model,"mig":mig,"rep":rep}
    for pop in ("p1","p2"):
        t=max((x for x in table if x["pop"]==pop),key=lambda x:x["generation"])
        for k,v in t.items():
            if k not in ("generation","pop"): row[f"{k}_{pop}"]=v
        g=max((x for x in geno if x[2]==pop),key=lambda x:int(x[1]))
        for key,idx in (("nAA",3),("nAB",4),("nBB",5),("a_chrom",6),("b_chrom",7),("A_in_AA",8),("A_in_AB",9),("B_in_BB",10),("B_in_AB",11)):
            row[f"{key}_{pop}"]=float(g[idx])
        for cl in ("A","B"):
            l=max((x for x in loads if x[2]==pop and x[3]==cl),key=lambda x:int(x[1]))
            for key,idx in (("n",4),("mean_count",5),("median_count",6),("q90_count",7),("total_count",8),("pop_count_contribution",9),("mean_weight",10),("median_weight",11),("q90_weight",12),("total_weight",13),("pop_weight_contribution",14)):
                row[f"{cl}_{key}_{pop}"]=float(l[idx])
    end.append(row)

def write(path, rows, fields):
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t"); w.writeheader(); w.writerows(rows)

fields=sorted({k for r in end for k in r}); write(OUT/"endpoint_replicates.tsv",end,fields)
def q(x,p):
    x=sorted(x); return x[int((len(x)-1)*p)] if x else float("nan")
def avg(x): return sum(x)/len(x) if x else float("nan")
def sd(x): return statistics.stdev(x) if len(x)>1 else 0.0

metrics=["A_freq_p1","A_freq_p2","A_mean_count_p1","A_mean_count_p2","A_total_count_p1","A_total_count_p2","B_mean_count_p1","B_mean_count_p2","A_recomb10_p1","A_recomb10_p2","A_recomb01_p1","A_recomb01_p2","B_recomb10_p1","B_recomb10_p2","B_recomb01_p1","B_recomb01_p2","LD_m2_m7_p1","LD_m2_m8_p1","LD_m5_m9_p1","LD_m5_m10_p1"]
sumrows=[]
for model in ("inversion","permanent_suppression"):
    for mig in sorted({r["mig"] for r in end if r["model"]==model}):
        sub=[r for r in end if r["model"]==model and r["mig"]==mig]
        for metric in metrics:
            if metric not in sub[0]: continue
            v=[r[metric] for r in sub]; sumrows.append({"model":model,"mig":mig,"metric":metric,"n":len(v),"mean":avg(v),"sd":sd(v),"q10":q(v,.1),"median":q(v,.5),"q90":q(v,.9)})
write(OUT/"endpoint_summary.tsv",sumrows,["model","mig","metric","n","mean","sd","q10","median","q90"])
write(OUT/"trajectory_records.tsv",traj,sorted({k for r in traj for k in r}))

bad=[]
for r in end:
    for pop in ("p1","p2"):
        for cl in ("A","B"):
            if abs(r[f"{cl}_total_count_{pop}"]-r[f"{cl}_mean_count_{pop}"]*r[f"{cl}_n_{pop}"])>.01: bad.append((r["model"],r["mig"],r["rep"],pop,cl,"count"))
with open(OUT/"qa.txt","w") as f:
    f.write(f"completed_endpoint_records={len(end)}\n")
    f.write(f"burden_decomposition_failures={len(bad)}\n")
    f.write("recombinant_phase_metrics=A_recomb10,A_recomb01,B_recomb10,B_recomb01\n")
    if bad: f.write("\n".join(map(str,bad))+"\n")
print(f"analyzed {len(end)} completed records; burden failures={len(bad)}")
