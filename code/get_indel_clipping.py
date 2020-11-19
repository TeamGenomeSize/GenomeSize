#!/usr/bin/python3


import sys, re
import csv
from pathlib import Path

samtools_view_output = sys.argv[1]
# print(samtools_view_output)

f = open(samtools_view_output, "r")

total = {"deletions" : 0, "insertions" : 0, "soft_clipping" : 0, "hard_clipping" : 0, "match" : 0, "equal" : 0, "mismatch" : 0}

#binary variable that turns on/off at the start/end of the cigar string in the samtools view output
#cigar_binary = 0

# M I = X
for line in f:
    #line_outputs = re.split("\t", line)

    cigar_indels = re.findall("[0-9]+[=]", line)
    for gap in cigar_indels:
        x = re.split("\D", gap)
        total["equal"] += int(x[0])


    cigar_indels = re.findall("[0-9]+[X]", line)
    for gap in cigar_indels:
        x = re.split("\D", gap)
        total["mismatch"] += int(x[0])

    #count inserted bases
    cigar_indels = re.findall("[0-9]+[I]", line)
    for gap in cigar_indels:
        x = re.split("\D", gap)
        total["insertions"] += int(x[0])

    #count deleted bases
    cigar_indels = re.findall("[0-9]+[D]", line)
    for gap in cigar_indels:
        x = re.split("\D", gap)
        total["deletions"] += int(x[0])
       
    #count soft clipped bases
    cigar_clippings = re.findall("[0-9]+[S]", line)
    for gap in cigar_clippings:
        x = re.split("\D", gap)
        total["soft_clipping"] += int(x[0])

    #count hard clipped bases
    cigar_clippings = re.findall("[0-9]+[H]", line)
    for gap in cigar_clippings:
        x = re.split("\D", gap)
        total["hard_clipping"] += int(x[0])

    #count matches
    cigar_clippings = re.findall("[0-9]+[M]", line)
    for gap in cigar_clippings:
        x = re.split("\D", gap)
        total["match"] += int(x[0])        

print(total)
#print(counter_dict)

#indel_ratio_dict = {"indel_regions" : 0, "indel_bases" : 0}

#indel_ratio_dict["indel_bases"] = (total["match"] + total["insertions"])/(total["match"]+total["deletions"])

indel_ratio = (total["match"] + total["insertions"])/(total["match"]+total["deletions"])

# indel ratio
if indel_ratio == 0:
    print("Error: ratio is 0")
else:
    #print(indel_ratio_dict["indel_bases"])
    print((indel_ratio))
    print(total["soft_clipping"])


