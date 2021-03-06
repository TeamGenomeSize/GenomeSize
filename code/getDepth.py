#!/usr/bin/python3

import os
import sys
import math
import statistics
import time
from pathlib import Path

def usageExample():
    # example output directory
    # to only run the usage example use
    # python3 getDepth.py output_directory
    # make sure the pileup file exists in output_directory first
    # outdir = "/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/output/"
    outdir = sys.argv[1]

    pileup_file = "{}/pileup.out".format(outdir)
    out_file = "{}/depths.out".format(outdir)

    depths, all_depths = readPileup(pileup_file)

    mmDepth = modeOfModes(depths)
    modDepth = modeDepth(all_depths)
    medMedDepth = medMedian(depths)    
    
    f = open(out_file, "w")

    f.write("mmDepth {}\n".format(mmDepth))
    f.write("modeDepth {}\n".format(modDepth))
    f.write("medDepth {}\n".format(medMedDepth))
    
    f.close()

def getDepth(method: str, depths: list, all_depths:list, filter_len: str, od: str, name: str):
    output = od + "/" + name + "_" + str(filter_len) + "_" + method + ".txt"
    time_limit = 20700 # 5h 45m
    check_interval = 300 # check every 5m

    # if file has been made but it's empty wait
    if os.path.exists(output) and os.path.getsize(output) == 0:        
    
        # read file when it's no longer empty    
        if watchFile(output, time_limit, check_interval):
            with open(output) as f:
                depth = int(f.readline().strip())
                    
        # quit if it takes longer than 5h and 45m    
        else:
            print("File not found after waiting:", time_limit, " seconds!")
            exit(1)

    # file exists and isn't empty so just read it
    elif os.path.exists(output) and os.path.getsize(output) > 0:
        with open(output) as f:
            depth = int(f.readline().strip())
    else:
        Path(output).touch()

        if method == 'mmDepth':
            depth = modeOfModes(depths)    

        elif method == 'modeDepth':
            depth = modeDepth(all_depths)        

        elif method == 'medDepth':
            depth = medMedian(depths)   
        
        # then write depth to file for other processes to read
        with open(output, 'w') as f:
            f.write(str(int(depth)) + "\n")

    return depth


# Watches a file path to see if it 
# Adapted from https://stackoverflow.com/questions/25617706/listening-for-a-file-in-python
def watchFile( filename, time_limit=3600, check_interval=60 ):
    '''Return true if filename exists, if not keep checking once every check_interval seconds for time_limit seconds.
    time_limit defaults to 1 hour
    check_interval defaults to 1 minute
    '''

    now = time.time()
    last_time = now + time_limit

    while time.time() <= last_time:
        if os.path.getsize( filename ) > 0:
             return True
        else:
            # Wait for check interval seconds, then check again.
            time.sleep( check_interval )

    return False



# Input: pileup file
# Output: A list a lists [sco] where sco = [read depth of bases]
# Generates read depth from a pileup file
def readPileup(pileupFile):
    f = open(pileupFile, "r")
    depths = []
    all_depths =[]
    
    curr_gene = []
    index = 0
    
    for line in f:
        # vals[1] = position
        # vals[3] = depth at given base
        
        vals = line.split()
        if int(vals[1]) != index + 1 and index != 0:
            depths.append(curr_gene)
            curr_gene = []
        
        curr_gene.append(int(vals[3]))
        all_depths.append(int(vals[3]))
        
        index = int(vals[1])
    
    f.close()
    
    return depths, all_depths


# https://stackoverflow.com/questions/10797819/finding-the-mode-of-a-list/10797913
# creates a list of unique somethings
def mode(array):
    most = max(list(map(array.count, array)))
    return list(set(filter(lambda x: array.count(x) == most, array)))

# mode in a given SCO and then the mode of these modes
def modeOfModes(depths):
    modes = []
    for d in depths:
    #     modes += mode(d)
    # return max(mode(modes))
        modes.append(min(statistics.multimode(d)))
    return min(statistics.multimode(modes))

# median of medians
# used for comparison with mode of modes
# simply experimental
def medMedian(depths):
    medians = []
    for d in depths:
        medians.append(statistics.median(d))
    
    return statistics.median(medians)

# mode when looking at all sco residues
def modeDepth(depths):
    return statistics.mode(depths)
        
if __name__ == "__main__":
    usageExample()
