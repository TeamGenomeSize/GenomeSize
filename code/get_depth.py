#!/usr/bin/python3

# import pandas as pd
import sys
# import pysam

def main ():
    zid = "z5207331" # CHANGE THIS TO YOUR zID WHEN RUNNING

    pileup_file = "/srv/scratch/{0}/pileup.out".format(zid)
    out_file = "/srv/scratch/{0}/depths.out".format(zid)

    depths = read_pileup(pileup_file)

    mmdepth = mode_of_modes(depths)
    maxdepth = max_mode(depths)

    f = open(out_file, "w")

    f.write("mode of modes depth is {}\n".format(mmdepth))
    f.write("modal depth is {}\n".format(maxdepth))

    f.close()

# Input: pileup file
# Output: A list a lists [sco] where sco = [read depth of bases]
# Generates read depth from a pileup file
def read_pileup(pileup_file):
    f = open(pileup_file, "r")
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


def mode_of_modes(depths):
    modes = []
    for d in depths:
        modes += mode(d)
    return mode(modes)


def max_mode(depths):
    maxes = []
    for d in depths:
        maxes.append(max(d))
    
    return mode(maxes)
        
if __name__ == "__main__":
    main()