#!/usr/bin/python3

# import pandas as pd
import sys
import math
# import pysam

def usageExample():
    outdir = "/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/output/{}".format(sys.argv[1])

    pileup_file = "{}/pileup.out".format(outdir)
    out_file = "{}/depths.out".format(outdir)

    depths = readPileup(pileup_file)

    mmDepth = modeOfModes(depths)     # list
    maxDepth = maxMode(depths)         # list
    maxMedDepth = maxMedian(depths)    # int

    f = open(out_file, "w")

    f.write("mode of modes depth is {}\n".format(mmDepth))
    f.write("modal depth is {}\n".format(maxDepth))
    f.write("max median depth is {}\n".format(maxMedDepth))

    f.close()

def getDepth(method: str, depths: list):
    
    if method == 'mmDepth':
        depth = modeOfModes(depths)     # list

    elif method == 'maxDepth':
        depth = maxMode(depths)         # list

    elif method == 'maxMedDepth':
        depth = maxMedian(depths)    # int

    return depth

# Input: pileup file
# Output: A list a lists [sco] where sco = [read depth of bases]
# Generates read depth from a pileup file
def readPileup(pileupFile):
    f = open(pileupFile, "r")
    depths = []
    
    curr_gene = []
    index = 0
    
    for line in f:
        # vals[1] = index
        # vals[3] = depth at given base
        vals = line.split()
        if int(vals[1]) != index + 1 and index != 0:
            depths.append(curr_gene)
            curr_gene = []
                
        curr_gene.append(int(vals[3]))    
        
        index = int(vals[1])
    
    f.close()
    
    return depths


# https://stackoverflow.com/questions/10797819/finding-the-mode-of-a-list/10797913
# creates a list of unique somethings
def mode(array):
    most = max(list(map(array.count, array)))
    return list(set(filter(lambda x: array.count(x) == most, array)))


def modeOfModes(depths):
    modes = []
    for d in depths:
        modes += mode(d)
    return mode(modes)


def maxMode(depths):
    maxes = []
    for d in depths:
        maxes.append(max(d))
    
    return mode(maxes)
    
def maxMedian(depths):
    maxes = []
    for d in depths:
        maxes.append(max(d))
    
    return maxes[math.floor(len(maxes)/2)]
        
if __name__ == "__main__":
    usageExample()