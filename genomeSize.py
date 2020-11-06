# runs all python components
# reads intermediary files created by bash scripts

############
# UNTESTED #
############

import csv, re
from pathlib import Path
import argparse
from code.getDepth import readPileup, getDepth

############
# run with:
# python3 genomeSize.py -od ${od} -n ${name} -p ${pileup} -v ${volume} -m ${method}


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

args = parser.parse_args()


def main ():

    # test_flags()

    indel = bool(args.indel)

    # 1) get read volume
    volume = readVolume(args.volume_path)

    # 2) get read depth
    depths = readPileup(args.pileup_path)
    depth = getDepth(args.method, depths) 

    # 3) calculate genome size (takes the floor function)
    if indel:
        genome_size = volume / depth
        
        indel_ratio = args.volume_path.replace(".sam", "_indel_bias.txt")
        indel_bias = readVolume(indel_ratio)

        genome_size = genome_size / indel_bias
    else:
        genome_size = volume / depth

    createLog()
    generateLog(volume, depth, genome_size)


def createLog():
    log = Path(args.od + "/genomeSize_log.csv")
    if not log.is_file():
        with open(args.od+'/genomeSize_log.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Method", "Filter", "Indel Bias", "Read Clipping", "Volume", "Depth", "Genome Size"])

def generateLog(vol, depth, gs):
    with open(args.od+'/genomeSize_log.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([args.method, args.filter_len, args.indel, args.rc, vol, depth, gs])

def readVolume(readVolumeFile: str):
    read_volume = 0

    with open(readVolumeFile) as f:
        read_volume = f.readline().strip()
    
    return float(read_volume)



def test_flags():
    print(args.volume_path)
    print(args.od)
    print(args.name)
    print(args.pileup_path)
    print(args.method)
    print(args.indel)
    print(args.rc)
    print('------------')


if __name__ == "__main__":
    main()
