#!/bin/bash
#SBATCH --job-name=slim_env_check
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:05:00
#SBATCH --output=slurm_logs/env_%j.out
#SBATCH --error=slurm_logs/env_%j.err

set -u
echo "hostname=$(hostname)"
date
command -v module >/dev/null 2>&1 && { module purge; module avail 2>&1 | grep -i slim || true; module spider slim 2>&1 || true; }
echo "PATH=$PATH"
echo "slim_path=$(command -v slim || true)"
if command -v slim >/dev/null 2>&1; then slim -v 2>&1 | head -n 2; fi
echo "cpu_count=$(getconf _NPROCESSORS_ONLN 2>/dev/null || true)"
free -h 2>/dev/null || true
