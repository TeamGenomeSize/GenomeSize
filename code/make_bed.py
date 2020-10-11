#!/usr/bin/python3

import sys

if len(sys.argv) != 1:
    print("Usage: python3 make_bed.py BUSCOFILE.tsv")
    sys.exit(1)

filename = sys.argv[1]

try:
    f = open(filename, "r")
    outf = open("ecoli.bed", "w")


    f.close()



except FileNotFoundError:
    print("\"" + sys.argv[1] "\"" + " does not exist")
    sys.exit(1)