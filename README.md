# GenomeSize

---

Chelsea's dump to be incorporated later

## Soft Clipping
Samtools mpileup does not explicitly state how it handles soft clipping in any official documentation, as such our understanding of this behaviour and how we subsequently interpreted a soft clipping bias was constructed through examination of the source code and the ![help](https://github.com/samtools/hts-specs/issues/80) of various other users ![asking](http://seqanswers.com/forums/showthread.php?t=31770) adjacent ![questions](https://bioinformatics.stackexchange.com/questions/157/are-soft-clipped-bases-used-for-variant-calling-in-samtools-bcftools). Soft clipped residues are included in the sequences of reads in BAM files, thereby contributing to read volume if the flag is switched on. Conversely as soft clipped residues are not part of alignments, they have no influence on read depth.





## Hard Clipping

## Insertion-Deletion Bias

