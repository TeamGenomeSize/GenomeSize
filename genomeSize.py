# runs all python components
# reads intermediary files created by bash scripts

############
# UNTESTED #
############

import csv, re
from pathlib import Path
import argparse
from code.getDepth import readPileup, getDepth

#############
# VARIABLES #
#############


parser = argparse.ArgumentParser(description='Calculate genome size given a set of combinations.')
# v
parser.add_argument('-v', action='store', type=str, required=True, dest='volume_path')
# od
parser.add_argument('-od', action='store', type=str, required=True, dest='od')
# n
parser.add_argument('-n', action='store', type=str, required=True, dest='name')
# p
parser.add_argument('-p', action='store', type=str, required=True, dest='pileup_path')
# m
parser.add_argument('-m', action='store', type=str, required=True, dest='method')
# i
parser.add_argument('-i', action='store', type=str, required=True, dest='indel')
# rc
parser.add_argument('-rc', action='store', type=str, required=True, dest='rc')
# fl
parser.add_argument('-fl', action='store', type=int, required=True, dest='filter_len')
# pid
parser.add_argument('-pid', action='store', type=str, required=True, dest='pid')


args = parser.parse_args()


def main ():
    
    # 1) get read volume
    volume = readInput(args.volume_path)

    # 1.1) adjust by indel bias
    indel_bias = 1
    if args.indel == "true":
        indel_ratio_path = args.volume_path.replace("_read_volume.txt", "_indel_bias.txt")
        indel_bias = readInput(indel_ratio_path)
    
    adjusted_volume = round(volume / indel_bias, 2)

    # 1.2) adjust by clipping bias
    clipping_bias = 1
    if args.rc == "true":
        clipping_bias_path = args.volume_path.replace("_read_volume.txt", "_clipping_bias.txt")
        clipping_amount = readInput(clipping_bias_path)
        clipping_bias = round(adjusted_volume / (adjusted_volume + clipping_amount), 2)
    
    adjusted_volume = round(adjusted_volume / clipping_bias, 2)

    # 2) get read depth
    depths, all_depths = readPileup(args.pileup_path)
    depth = getDepth(args.method, depths, all_depths, args.filter_len, args.od, args.name) 

    # 3) calculate genome size
    genome_size = round( adjusted_volume / depth, 2)

    # 4) print out into a parseable log file with list of assumptions (ALANA)
    createLog()
    generateLog(volume, depth, genome_size, indel_bias, clipping_bias)
    

    # test_flags(indel_bias)


def createLog():
    log = Path(args.od + "/" + args.name + "_genomeSize_log.csv")
    if not log.is_file():
        with open(args.od + "/" + args.name + "_genomeSize_log.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["PID","Filter", "Method", "Indel On", "Indel Bias" ,"Read Clipping On", "Clipping Bias", "Volume", "Depth", "Genome Size"])

def generateLog(vol, depth, gs, indel_bias, clipping_bias):
    with open(args.od + "/" + args.name + "_genomeSize_log.csv", 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([args.pid, args.filter_len, args.method, args.indel, indel_bias, args.rc, clipping_bias , vol, depth, gs])

def readInput(readInputFile: str):
    read_volume = 0

    with open(readInputFile) as f:
        try:
            read_volume = float(f.readline().strip())
        except:
            print(f.readline().strip())
    
    read_volume = round(read_volume,4)
    return read_volume



def test_flags(indel_bias):
    print(args.volume_path)
    print(args.od)
    print(args.name)
    print(args.pileup_path)
    print(args.method)
    print(args.indel)
    print(args.rc)
    print("indel_bias = " + str(indel_bias))
    print('------------')


if __name__ == "__main__":
    main()
