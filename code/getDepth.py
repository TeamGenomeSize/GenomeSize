#!/usr/bin/python3

# import pandas as pd
import sys
import math
# import pysam

def usageExample():
    # outdir = "/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/output/{}".format(sys.argv[1])
    outdir = "srv/scratch/z5207331/{}".format(sys.argv[1])

    pileup_file = "{}/pileup.out".format(outdir)
    out_file = "{}/depths.out".format(outdir)

    depths = readPileup(pileup_file)

    mmDepth = modeOfModes(depths)     # list
    modDepth = modeDepth(depths)         # list
    medMedDepth = medMedian(depths)    # int
    
    # matching that could make it slow
    # mmDepth2 = modeOfModes(depths_match)     # list
    # modDepth2 = modeDepth(depths_match)         # list
    # medMedDepth2 = medMedian(depths_match)    # int

    f = open(out_file, "w")

    f.write("mmDepth {}\n".format(mmDepth))
    f.write("modeDepth {}\n".format(modDepth))
    f.write("medDepth {}\n".format(medMedDepth))
    
    # f.write("========================== without mismatches ==========================\n")
    
    # f.write("mode of modes depth is {}\n".format(mmDepth2))
    # f.write("modal depth is {}\n".format(modDepth2))
    # f.write("median of median depth is {}\n".format(medMedDepth2))

    f.close()

def getDepth(method: str, depths: list):
    
    if method == 'mmDepth':
        depth = modeOfModes(depths)     # list

    elif method == 'modeDepth':
        depth = modeDepth(depths)         # list

    elif method == 'medDepth':
        depth = medMedian(depths)    # int

    return depth

# Input: pileup file
# Output: A list a lists [sco] where sco = [read depth of bases]
# Generates read depth from a pileup file
def readPileup(pileupFile):
    f = open(pileupFile, "r")
    depths = []
    # depths_no_mismatch = []
    
    curr_gene = []
    # curr_gene_no_mismatch = []
    index = 0
    
    for line in f:
        # vals[1] = position
        # vals[3] = depth at given base
        # vals[5] = base read at position
        
        vals = line.split()
        if int(vals[1]) != index + 1 and index != 0:
            depths.append(curr_gene)
            # depths_no_mismatch.append(curr_gene_no_mismatch)
            curr_gene = []
            # curr_gene_no_mismatch = []
        
        curr_gene.append(int(vals[3]))
        # matches = count_match(vals[5])
        # curr_gene_no_mismatch.append(matches)
        
        index = int(vals[1])
    
    f.close()
    
    return depths

def count_match(string):
    bases = {"a": 0, "c": 0, "g":0, "t":0}
    for i in string.lower():
        if i in bases:
            bases[i] += 1
    
    return max(bases.values())

# https://stackoverflow.com/questions/10797819/finding-the-mode-of-a-list/10797913
# creates a list of unique somethings
def mode(array):
    most = max(list(map(array.count, array)))
    return list(set(filter(lambda x: array.count(x) == most, array)))


def modeOfModes(depths):
    modes = []
    for d in depths:
        modes += mode(d)
    return max(mode(modes))

    
# now its median of medians
def medMedian(depths):
    maxes = []
    for d in depths:
        s = sorted(d)
        maxes.append(s[math.floor(len(s)/2)])
    
    return maxes[math.floor(len(maxes)/2)]
    
def modeDepth(depths):
    allDepths = []
    for d in depths:
        allDepths += d
        
    return max(mode(allDepths))
        
if __name__ == "__main__":
    usageExample()