#!/usr/bin/python3


import sys, re

samtools_view_output = "output.txt"

f = open(samtools_view_output, "r")

counter_dict = {"total_deleted_bases" : 0, "total_inserted_bases" : 0, "total_deletion_regions" : 0, "total_insertion_regions" : 0, "total_soft_clipping_bases" : 0, "total_soft_clipped_regions" : 0, "total_hard_clipping_bases" : 0, "total_hard_clipped_regions" : 0, "total_matched_bases" : 0, "total_matched_regions" : 0}

#binary variable that turns on/off at the start/end of the cigar string in the samtools view output
cigar_binary = 0

for line in f:

    if cigar_binary == 1:
        #counts indel regions
        counter_dict["total_insertion_regions"] += line.count("I")
        counter_dict["total_deletion_regions"] += line.count("D")
        counter_dict["total_soft_clipped_regions"] += line.count("S")
        counter_dict["total_hard_clipped_regions"] += line.count("H")
        counter_dict["total_matched_regions"] += line.count("M")        
        
        #count inserted bases
        cigar_indels = re.findall("[0-9]+[I]", line)
        for gap in cigar_indels:
            x = re.split("\D", gap)
            counter_dict["total_inserted_bases"] += int(x[0])

        #count deleted bases
        cigar_indels = re.findall("[0-9]+[D]", line)
        for gap in cigar_indels:
            x = re.split("\D", gap)
            counter_dict["total_deleted_bases"] += int(x[0])
       
        #count soft clipped bases
        cigar_clippings = re.findall("[0-9]+[S]", line)
        for gap in cigar_clippings:
            x = re.split("\D", gap)
            counter_dict["total_soft_clipping_bases"] += int(x[0])
 
        #count hard clipped bases
        cigar_clippings = re.findall("[0-9]+[H]", line)
        for gap in cigar_clippings:
            x = re.split("\D", gap)
            counter_dict["total_hard_clipping_bases"] += int(x[0])

        #count matches
        cigar_clippings = re.findall("[0-9]+[M]", line)
        for gap in cigar_clippings:
            x = re.split("\D", gap)
            counter_dict["total_matched_bases"] += int(x[0])        
    
    if line.count("unitig"):
        cigar_binary = 1
    
    if line.count("*"):
        cigar_binary == 0


#print(counter_dict)

indel_dict = {"indel_regions" : 0, "indel_bases" : 0}
indel_dict["indel_regions"] = (counter_dict["total_matched_regions"] + counter_dict["total_insertion_regions"])/(counter_dict["total_matched_regions"] + counter_dict["total_deletion_regions"])
indel_dict["indel_bases"] = (counter_dict["total_matched_bases"] + counter_dict["total_inserted_bases"])/(counter_dict["total_matched_bases"]+counter_dict["total_deleted_bases"])
#print(indel_dict)
#print(indel_dict["indel_regions"])

# indel ratio
print(indel_dict["indel_bases"])