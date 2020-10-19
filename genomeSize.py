# runs all python components
# reads intermediary files created by bash scripts

############
# UNTESTED #
############


import argparse
import code.getDepth import readPileup
from code.calcGenomeSize import *


#############
# VARIABLES #
#############


parser = argparse.ArgumentParser(description='Calculate genome size given a set of combinations.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--method', metavar='method' dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))


def main ():

    # 1) get read volume
    volume = readVolume()

    # 2) get read depth
    depths = readPileup()
    depth = maxMedian(method, depths)    # int

    # 3) calculate genome size
    genome_size = calcGenomeSize()

    # 4) print out into a parseable log file

    


def readVolume(readVolumeFile: str):
    f = open(readVolumeFile, "r")

    for line in f:
        read_volume = int(line)

    f.close()
    
    return read_volume



if __name__ == "__main__":
    main()
