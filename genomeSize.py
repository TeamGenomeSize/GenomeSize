# runs all python components
# reads intermediary files created by bash scripts

############
# UNTESTED #
############


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
parser.add_argument('-i', action='store', type=bool, required=True, dest='indel')
# rd
parser.add_argument('-rc', action='store', type=bool, required=True, dest='rc')

args = parser.parse_args()


def main ():

    # test_flags()

    # 1) get read volume
    volume = readVolume(args.volume_path)

    # 2) get read depth
    depths = readPileup(args.pileup_path)
    depth = getDepth(args.method, depths) 

    # 3) calculate genome size (takes the floor function)
    genome_size = volume / depth

    # 4) print out into a parseable log file with list of assumptions (ALANA)

    # e.g. print('method =', args.method)
    
    #             method, filter, indel bias, 
    # volume              50000
    # depth
    # genome_size=1million
    # --------------------------
    #             method, filter, indel bias, 
    # volume      
    # depth
    # genome_size

    


def readVolume(readVolumeFile: str):
    f = open(readVolumeFile, "r")

    for line in f:
        read_volume = int(line)

    f.close()
    
    return read_volume



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
