#!/usr/bin/python3


import sys, re
import csv
from pathlib import Path

samtools_view_output = sys.argv[1]
# print(samtools_view_output)

f = open(samtools_view_output, "r")

counter_dict = {"total_deleted_bases" : 0, "total_inserted_bases" : 0, "total_deletion_regions" : 0, "total_insertion_regions" : 0, "total_soft_clipping_bases" : 0, "total_soft_clipped_regions" : 0, "total_hard_clipping_bases" : 0, "total_hard_clipped_regions" : 0, "total_matched_bases" : 0, "total_matched_regions" : 0}

#binary variable that turns on/off at the start/end of the cigar string in the samtools view output
#cigar_binary = 0

for line in f:
    line_outputs = re.split("\t", line)
    #print(line_outputs)  #counts indel regions
    counter_dict["total_insertion_regions"] += line_outputs[5].count("I")
    counter_dict["total_deletion_regions"] += line_outputs[5].count("D")
    counter_dict["total_soft_clipped_regions"] += line_outputs[5].count("S")
    counter_dict["total_hard_clipped_regions"] += line_outputs[5].count("H")
    counter_dict["total_matched_regions"] += line_outputs[5].count("M")
        
    #count inserted bases
    cigar_indels = re.findall("[0-9]+[I]", line_outputs[5])
    for gap in cigar_indels:
        x = re.split("\D", gap)
        counter_dict["total_inserted_bases"] += int(x[0])

    #count deleted bases
    cigar_indels = re.findall("[0-9]+[D]", line_outputs[5])
    for gap in cigar_indels:
        x = re.split("\D", gap)
        counter_dict["total_deleted_bases"] += int(x[0])
       
    #count soft clipped bases
    cigar_clippings = re.findall("[0-9]+[S]", line_outputs[5])
    for gap in cigar_clippings:
        x = re.split("\D", gap)
        counter_dict["total_soft_clipping_bases"] += int(x[0])

    #count hard clipped bases
    cigar_clippings = re.findall("[0-9]+[H]", line_outputs[5])
    for gap in cigar_clippings:
        x = re.split("\D", gap)
        counter_dict["total_hard_clipping_bases"] += int(x[0])

    #count matches
    cigar_clippings = re.findall("[0-9]+[M]", line_outputs[5])
    for gap in cigar_clippings:
        x = re.split("\D", gap)
        counter_dict["total_matched_bases"] += int(x[0])        

#print(counter_dict)

indel_ratio_dict = {"indel_regions" : 0, "indel_bases" : 0}
# indel_ratio_dict["indel_regions"] = (counter_dict["total_matched_regions"] + counter_dict["total_insertion_regions"])/(counter_dict["total_matched_regions"] + counter_dict["total_deletion_regions"])
indel_ratio_dict["indel_bases"] = (counter_dict["total_matched_bases"] + counter_dict["total_inserted_bases"])/(counter_dict["total_matched_bases"]+counter_dict["total_deleted_bases"])
#print(indel_dict["indel_regions"])

# indel ratio
if indel_ratio_dict["indel_bases"] == 0:
    print("Error: ratio is 0")
else:
    print(indel_ratio_dict["indel_bases"])



