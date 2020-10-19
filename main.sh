#!/bin/sh

# Author: Chelsea Liang

# This main script launches the investigation of each viable combination of assumptions
	# you may exit the shell when following is printed to the terminal:
	# "Completed error checking inputs, pipeline will complete in background"
# run with:
# mkdir -p ${output_dir} 
# ./main.sh -od ${output_dir} -b ${bam} -sco ${sco} &
# disown -h %1

# output_dir =
# bam =
# sco =
# summary_path =

############
# UNTESTED #
############

## LOGS AND ERRORS
SECONDS=0					# records time taken by whole pipeline
set -e						# if any error occurs, exit 1


###############
## Variables ##
###############

# Mandatory:
# - ${bam}, path to bam file of mapped reads
# - ${od}, path of the working/output directory of script
# - ${sco}, path to tsv of BUSCO single copy ortholog output

# Optional:
# - ${rf}, path to reference genome
# - ${fl}, filter_len: reads below this threshold not included in read volume calculation
# - ${dm}, mode to calculuate read depth

##                                                                              ##
# getopts handling adapted from:                                                 #
# https://stackoverflow.com/questions/18414054/reading-optarg-for-optional-flags #
##                                                                              ##

function print_usage {
  echo "TODO"
}


if [[ "$1" =~ ^((-{1,2})([Hh]$|[Hh][Ee][Ll][Pp])|)$ ]]; then
    print_usage; exit 1
else
  while [[ $# -gt 0 ]]; do
    opt="$1"
    shift;
    current_arg="$1"
    if [[ "$current_arg" =~ ^-{1,2}.* ]]; then
      echo "WARNING: You may have left an argument blank. Double check your command." 
    fi
    case "$opt" in
      "-od"|"--output_dir"              ) OD="$1"; shift;;
      "-b"|"--bam"                      ) BAM="$1"; shift;;
      "-sco"|"--single_copy_orthologs"  ) SCO="$1"; shift;;
      "-rf"|"--reference_genome"        ) REF_GENOME="$1"; shift;;
      "-fl"|"--filter_len"              ) FILTER_LEN="$1"; shift;;
      "-dm"|"--depth_method"            ) METHOD="$1"; shift;;
      *                                 ) echo "ERROR: Invalid option: \""$opt"\"" >&2
      exit 1;;
    esac
  done
fi

# setting default flags
METHOD=mode_of_modes            # mode of modes, maximum of modes, median
CALC_SCO=false
WD=$(pwd)

# ERROR HANDLING OF MISSING MANDATORY ARGUMENTS
# TODO
if [[ "$OD" == "" ]]; then
  echo "ERROR: Option -od require arguments." >&2
  exit 1
fi

if [[ "$BAM" == "" ]]; then
  echo "TODO" >&2

  if [[ "$SCO" == "" ]]; then
    echo "TODO" >&2

    if [[ "$REF_GENOME" == "" ]]; then
      echo "Either provide a reference genome or provide a bam and corresponding sco file" >&2
    fi

  fi

  exit 1
fi


echo "Error handling of arguments complete, you may now close the terminal"
echo "---"
echo "Make sure to check pipeline_log.txt before using results in \
case the script terminated unexpectedly."

log=${output_dir}/pipeline_log.txt
exec 3>&1 1>>${log} 2>&1 	# handles printing of messages to log and terminal

echo "===========================================================" >> ${log}
echo [$(date)] "PID: $$" >> ${log}
echo "===========================================================" >> ${log}

# Print current envrionment variables
# TODO


# Running BUSCO or MMSeq2 would happen up here (Epic Story 4)
# TODO


# Compute array of assumptions to try
# TODO


# Run the different combinations of variable (python generated)
# for each assumptions in python output 

  # run run.pbs, launching parralel jobs
  qsub run.pbs \
  -v OD=${OD} BAM=${BAM} SCO=${SCO} assumptions=${assumptions}





## DELETE AND TIDY FILES



## PRINTS DURATION OF SCRIPT
duration=${SECONDS}
echo "$((${duration} / 3600)) hours, $(((${duration} / 60) % 60)) minutes and $((${duration} % 60)) seconds elapsed" >> ${log}
echo [$(date)] "COMPLETED PIPELINE for: " >> ${log}
echo "${experiment_name}" >> ${log}
echo "===========================================================" >> ${log}






















## PROGRAM PATHS -- PLEASE CHANGE THESE PATHS TO THE ACTUAL PROGRAM PATHS ON YOUR SYSTEM

## ERROR HANDLING INPUTS

