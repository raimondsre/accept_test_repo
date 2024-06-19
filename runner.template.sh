#!/bin/bash
#PBS -A @account
#PBS -l walltime=24:00:00,feature=largescratch
#PBS -q batch
#PBS -l nodes=1:ppn=1,pmem=4g
#PBS -j oe
base_dir=@base_dir
log_dir="${base_dir}/work"
entrypoint=@entrypoint

module load singularity/3.11.4
nextflow -log $log_dir run $entrypoint -w $base_dir