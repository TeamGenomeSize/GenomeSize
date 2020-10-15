#!/bin/bash

# Author: Sehhaj Grewal
# UNSW BINF6112 Team Genome Size
# Date: 8 October 2020


# TO DO
# stretch goal including fastq.gz files - create BAM file
#  ERROR CHECKING MIN_READ_LENGTH FLAG/ BAM FILE

# try with samtools view
# test with diploiducus
# test with redbean.bam

# Full path to BAM file of mapped reads to determine total read length
# MIN_READ_LENGTH - cutoff for the min read length in calculation 5kb/10kb

BAM_FILE=$1
MIN_READ_LENGTH=$2
echo "MIN_READ_LENGTH $2"

# if min_read_length is a number then samtools grep/cut/remove

#echo "All reads"
#all=$(samtools  stats $1 | grep ^RL | cut -f 2- | awk '{sum+=$2} {total+=$1*$2} END{print "sum=",sum} END{print "total=",total}')

#echo "Only reads above 5kb"
#5kb=$(samtools  stats $1 | grep ^RL | cut -f 2- | awk '{if($1 >= 5000) sum+=$2} {if($1 >= 5000) total+=$1*$2 } END{print "sum=",sum} END{print "total=",total}')

#echo "Only reads above 10kb"
#10kb=$(samtools  stats $1 | grep ^RL | cut -f 2- | awk '{if($1 >= 5000) sum+=$2} {if($1 >= 5000) {if($1 >= 10000) total+=$1*$2} END{print "sum=",sum} END{print "total=",total}')

# samtools stats ignores clipping
# if [[ -z "${MIN_READ_LENGTH}" ]]
# then
#     samtools  stats $1 | grep ^RL | cut -f 2- | awk '{sum+=$2} {total+=$1*$2} END{print "1. number of reads =",sum} END{print "WITHOUT CLIPPING read volume=",total}'
#     samtools view $1 | awk '{sum+=length($10)} END{print "WITH CLIPPING read volume = ",sum}'
# else
#     samtools stats $1 | grep ^RL | cut -f 2- | awk -v min="${MIN_READ_LENGTH}" '{if($1 >= min) sum+=$2} {if($1 >= min) total+=$1*$2 } END{print "1. number of reads =",sum} END{print "read volume=",total}'
#     samtools view $1 | awk -v min="${MIN_READ_LENGTH}" '{if(length($10) >= min) sum+=length($10)} END{print "WITH CLIPPING read volume = ",sum}'
# fi

if [[ -z "${MIN_READ_LENGTH}" ]]
then
    samtools  stats $1 | grep ^RL | cut -f 2- | awk '{total+=$1*$2} END{print "WITHOUT CLIPPING read volume=",total}'
    samtools view $1 | awk '{sum+=length($10)} END{print "WITH CLIPPING read volume = ",sum}'
else
    samtools stats $1 | grep ^RL | cut -f 2- | awk -v min="${MIN_READ_LENGTH}" '{if($1 >= min) total+=$1*$2 } END{print "WITHOUT CLIPPING read volume=",total}'
    samtools view $1 | awk -v min="${MIN_READ_LENGTH}" '{if(length($10) >= min) sum+=length($10)} END{print "WITH CLIPPING read volume = ",sum}'
fi


#echo "${all}"
#echo "MIN_READ_LENGTH ${5kb}"
#echo "MIN_READ_LENGTH ${10kb}"