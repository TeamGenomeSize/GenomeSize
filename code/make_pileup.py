#!/usr/bin/python3

import sys
import pysam

# if len(sys.argv) > 2:
#     print("Usage: python3 make_pileup.py FILE.bam [FILE.bed]")
#     sys.exit(1)

# filename = sys.argv[1]



try:
    bamfile = "/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/e_coli/bam/e_coli.bam"
    samfile = pysam.AlignmentFile(bamfile, "rb")
    
    f = open("/home/z5207331/GenomeSize/e_coli_ss.bed", "r")
    outf = open("/home/z5207331/GenomeSize/pileup.out", "w")
    
    counts = {}
    
    for line in f:
        if line[0] == "#":
            continue
          
        vals = line.split(" ")
        
        ncounts = []
        
        for pileupcolumn in samfile.pileup(vals[0], int(vals[1]), int(vals[2])):
            ncounts.append(pileupcolumn.n)
        
        counts[vals[0]] = ncounts
        outf.write(vals[0] + str(ncounts))
        
    samfile.close()
    f.close()
    outf.close()

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
    
    


    # f.close()



except FileNotFoundError:
    print("file does not exist")
    sys.exit(1)