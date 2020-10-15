#!/usr/bin/python3

import pandas as pd
import sys
# import pysam


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
    
    f.close()
    
    return depths


# https://stackoverflow.com/questions/10797819/finding-the-mode-of-a-list/10797913
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
        


zid = "z5207331"

pileup_file = "/srv/scratch/{0}/pileup.out".format(zid)
out_file = "/srv/scratch/{0}/depths.out".format(zid)

depths = read_pileup(pileup_file)

print(depths)

mmdepth = mode_of_modes(depths)
maxdepth = max_mode(depths)

print(mmdepth)
print(maxdepth)

# f = open(out_file, "w")

# f.write(mmdepth + "\n")
# f.write(maxdepth + "\n")

# f.close()