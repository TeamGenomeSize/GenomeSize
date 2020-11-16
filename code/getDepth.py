#!/usr/bin/python3

# import pandas as pd
import sys
import math
# import pysam

def usageExample():
    # outdir = "/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/output/{}".format(sys.argv[1])
    outdir = "/srv/scratch/z5207331/{}".format(sys.argv[1])

    pileup_file = "{}/pileup.out".format(outdir)
    out_file = "{}/depths.out".format(outdir)

    depths = readPileup(pileup_file, out_file)
    print(depths)


# returns a dictionary with method as the key
# and value is the read depth
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
def readPileup(pileupFile, outFile):
    f = open(pileupFile, "r")
    
    depths = []                 # list of lists, each list is depths of one sco
    all_depths = []             # read depths of all sco base positions in one list
    mode_depths = []            # mode of each sco in one list
    # median_depths = []          # median depth of each sco in one list
    
    # # same as above but only bases that match the majority of the reads
    # depths_m = []                 
    # all_depths_m = []             
    # mode_depths_m = []            
    # median_depths_m = []
    
    curr_gene = []
    # curr_gene_m = []
    
    index = 0
    
    for line in f:
        # vals[1] = index
        # vals[3] = depth at given base
        # vals[5] = base at position
        vals = line.split()
        
        # moving on to next SCO
        if int(vals[1]) != index + 1 and index != 0:
            # add to list of all depths
            all_depths += curr_gene
            # all_depths_m += curr_gene_m
            
            # add to list of modes
            mode_depths.append(max(mode(curr_gene)))
            # mode_depths_m.append(max(mode(curr_gene_m)))
            
            # # add to list of medians
            # median_depths.append(sorted(curr_gene)[math.floor(len(curr_gene)/2)])
            # median_depths_m.append(sorted(curr_gene_m)[math.floor(len(curr_gene_m)/2)])
            
            depths.append(curr_gene)
            curr_gene = []
            # curr_gene_m = []
                
        curr_gene.append(int(vals[3]))
        
        # matches = count_match(vals[5])
        # curr_gene_m.append(matches)
        
        index = int(vals[1])
    
    f.close()
    
    final = {}
    
    final["modeOfModes"] = max(mode(mode_depths))
    # final["modeOfModesM"] = max(mode(mode_depths_m))
    
    # final["medOfMeds"] = sorted(median_depths)[math.floor(len(median_depths)/2)]
    # final["medOfMedsM"] = sorted(median_depths)[math.floor(len(median_depths_m)/2)]
    
    final["mode"] = max(mode(all_depths))
    # final["modeM"] = max(mode(all_depths_m))
    
    depthFile = open(outFile, "w+")        # need to rename file
    for key in final:
        depthFile.write("{} {}\r\n".format(key, final[key]))
    depthFile.close()
    
    return final

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


# can be deleted
# ====================================================================================

def modeOfModes(depths):
    modes = []
    for d in depths:
        modes += mode(d)
    return max(mode(modes))


def maxMode(depths):
    maxes = []
    for d in depths:
        maxes.append(max(d))
    
    return max(mode(maxes))
    
def maxMedian(depths):
    maxes = []
    for d in depths:
        maxes.append(max(d))
    
    return maxes[math.floor(len(maxes)/2)]
        
if __name__ == "__main__":
    usageExample()