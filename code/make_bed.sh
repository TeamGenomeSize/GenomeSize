#!/bin/sh

#PBS -l select=1:ncpus=1:mem=4gb
#PBS -l walltime=1:00:00
#PBS -M z5207331@unsw.edu.au
#PBS -m ae
#PBS -j oe
#PBS -o /home/z5207331/GenomeSize/make_bed_log

cd /home/z5207331/GenomeSize

# python3 make_bed.py /srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/e_coli/busco3/run_e_coli/full_table_e_coli.tsv

egrep -v "^#" /srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/e_coli/busco3/run_e_coli/full_table_e_coli.tsv | \
cut -f1,4,5 > /home/z5207331/GenomeSize/e_coli.bed

module load samtools

samtools mpileup -I /home/z5207331/GenomeSize/e_coli.bed -b /srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/e_coli/bam/e_coli.bam -o /home/z5207331/GenomeSize/e_coli.pileup