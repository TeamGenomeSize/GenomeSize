#!/usr/bin/python3

import sys

methods = ['medDepth', 'mmDepth']
indel = ['true', 'false']
r_clipping = ['true', 'false']


f = open(sys.argv[1], 'w')
counter = 0

for method in methods:
    for status in indel:
        for setting in r_clipping:
            f.write("{}={},{}={},{}={}\n".format(
                'method',method,'indel',status,'r_clipping',setting
            ))
            counter = counter + 1
print("[assumptions.py] Number of assumption combinations = {}".format(counter))

f.close()