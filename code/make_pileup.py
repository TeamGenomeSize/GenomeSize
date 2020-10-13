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
    bamfile = "/srv/scratch/{0}/e_coli.bam".format(zid)
    
    samfile = pysam.AlignmentFile(bamfile, "rb")
    samfile._hasIndex()
    f = open("/srv/scratch/{0}/e_coli_ss.bed".format(zid), "r")
    outf = open("/srv/scratch/{0}/pileup.out".format(zid), "w")

    counts = []
    
    for line in f:
        if line[0] == "#":
            continue
          
        vals = line.split(" ")
        
        ncounts = []
        
        for pileupcolumn in samfile.pileup(vals[0], int(vals[1]), int(vals[2])):
            ncounts.append(pileupcolumn.n)
        
        counts.append(ncounts)
        outf.write(vals[0] + str(ncounts))
        
    samfile.close()
    f.close()
    outf.close()
    
    # error
    # [E::idx_find_and_load] Could not retrieve index file for '/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/e_coli/bam/e_coli.bam'
    # Traceback (most recent call last):
    #   File "code/make_pileup.py", line 31, in <module>
    #     for pileupcolumn in samfile.pileup(vals[0], int(vals[1]), int(vals[2])):
    #   File "pysam/libcalignmentfile.pyx", line 1331, in pysam.libcalignmentfile.AlignmentFile.pileup
    # ValueError: no index available for pileup

    # copied from pysam documentation
    
    # for pileupcolumn in samfile.pileup("chr1", 100, 120):
    # print("\ncoverage at base %s = %s" %
    #        (pileupcolumn.pos, pileupcolumn.n))
    # for pileupread in pileupcolumn.pileups:
    #     if not pileupread.is_del and not pileupread.is_refskip:
    #         # query position is None if is_del or is_refskip is set.
    #         print ('\tbase in read %s = %s' %
    #               (pileupread.alignment.query_name,
    #                pileupread.alignment.query_sequence[pileupread.query_position]))
    # samfile.close()
    


except FileNotFoundError:
    print("file does not exist")
    sys.exit(1)