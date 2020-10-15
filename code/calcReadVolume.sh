#!/bin/bash

# Author: Sehhaj Grewal
# UNSW BINF6112 Team Genome Size
# Date: 8 October 2020


# TO DO
# stretch goal including fastq.gz files - create BAM file
# ERROR CHECKING MIN_READ_LENGTH FLAG/ BAM FILE
# test with diploiducus
# test with redbean.bams

# Full path to BAM file of mapped reads to determine total read length
# MIN_READ_LENGTH - cutoff for the min read length in calculation 5kb/10kb

BAM_FILE=$1
MIN_READ_LENGTH=$2

#samtools view includes supplementary reads
#samtools stats - raw reads

if [[ -z "${MIN_READ_LENGTH}" ]]
then
    samtools  stats ${BAM_FILE} | grep ^RL | cut -f 2- | awk '{total+=$1*$2} END{print total}'
    #samtools view $1 | awk '{sum+=length($10)} END{print "WITH CLIPPING read volume = ",sum}'
else
    samtools stats ${BAM_FILE} | grep ^RL | cut -f 2- | awk -v min="${MIN_READ_LENGTH}" '{if($1 >= min) total+=$1*$2 } END{print total}'
    #samtools view $1 | awk -v min="${MIN_READ_LENGTH}" '{if(length($10) >= min) sum+=length($10)} END{print "WITH CLIPPING read volume = ",sum}'
fi
