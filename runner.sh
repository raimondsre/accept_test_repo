#!/bin/bash
#PBS -A bmc_klovins
#PBS -l walltime=24:00:00,feature=largescratch
#PBS -q batch
#PBS -l nodes=1:ppn=1,pmem=4g
#PBS -j oe

module load singularity/3.11.4

nextflow -log /home_beegfs/bioms02/calculator_experiments/nextflow-sample/work run /home_beegfs/bioms02/calculator_experiments/nextflow-sample/main.nf -w /home_beegfs/bioms02/calculator_experiments/nextflow-sample