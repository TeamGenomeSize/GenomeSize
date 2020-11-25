#!/usr/bin/python3

import sys

# This will generate assumptions.txt
# e.g. modify this to add more depth options when a method is implemented
methods = ['medDepth', 'mmDepth', 'modeDepth']
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