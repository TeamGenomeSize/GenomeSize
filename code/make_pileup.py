#!/usr/bin/python3

import sys
import pysam

# if len(sys.argv) > 2:
#     print("Usage: python3 make_pileup.py FILE.bam [FILE.bed]")
#     sys.exit(1)

# filename = sys.argv[1]

zid = "z5207331"

try:
    # bamfile = "/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/e_coli/bam/e_coli.bam"
    bamfile = "/srv/scratch/{0}/e_coli.sort.bam".format(zid)
    
    samfile = pysam.AlignmentFile(bamfile, "rb", index_filename="/srv/scratch/{0}/e_coli.sort.bam.bai".format(zid))
    # samfile._hasIndex()
    
    # sort -n -k 2 e_coli_ss.bed > e_coli_sorted.bed
    f = open("/srv/scratch/{0}/e_coli_sorted.bed".format(zid), "r")
    outf = open("/srv/scratch/{0}/pysam.pileup.out".format(zid), "w")

    counts = []
    
    for line in f:
        if line[0] == "#":
            continue
          
        vals = line.split(" ")
        
        ncounts = []
        
        outf.write(line + "\n")
        
        for pileupcolumn in samfile.pileup(reference=vals[0], start=int(vals[1]), end=int(vals[2]),stepper='nofilter',max_depth=500000,truncate=False,min_base_quality=0):
            outf.write("coverage at base {} : {}\n".format(pileupcolumn.reference_pos, pileupcolumn.nsegments))
            # for pileupread in pileupcolumn.pileups:
            #     if not pileupread.is_del and not pileupread.is_refskip:
            #         # query position is None if is_del or is_refskip is set.
            #         outf.write('\tbase in read %s = %s' %
            #               (pileupread.alignment.query_name,
            #                pileupread.alignment.query_sequence[pileupread.query_position]))
                
        # counts.append(ncounts)
        
    samfile.close()
    f.close()
    outf.close()


except FileNotFoundError:
    print("file does not exist")
    sys.exit(1)