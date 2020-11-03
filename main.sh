#!/bin/sh

# Author: Chelsea Liang

# This main script launches the investigation of each viable combination of assumptions
	# you may exit the shell when following is printed to the terminal:
	# "Completed error checking inputs, pipeline will complete in background"
# run with:
# mkdir -p ${OD} 
# ./main.sh -od ${od} -nm ${NAME} -wd ${WD} -b ${bam} -sco ${sco} &
# disown -h %1

# NAME=e_coli
# od=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/output/chelsea_test
# bam=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/${NAME}/bam/${NAME}.bam
# sco=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/${NAME}/busco3/run_${NAME}/full_table_${NAME}.tsv
# WD=$(pwd)

# setting default flags
CALC_SCO=false
FILTER_LEN=5000


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
# - ${OD}, path of the working/output directory of script
# - ${NAME}, rootname for files created by pipeline
# - #{wd}, path to top level of code i.e. same level as this main.sh script

# Optional:
# - ${REF_GENOME}, path to reference genome
# - ${SCO}, path to tsv of BUSCO single copy ortholog output
# - ${BAM}, path to bam file of mapped reads


##                                                                              ##
# getopts handling adapted from:                                                 #
# https://stackoverflow.com/questions/18414054/reading-optarg-for-optional-flags #
##                                                                              ##

function print_usage {
  echo "banana"
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
      "-nm"|"--name"                    ) NAME="$1"; shift;;
      "-wd"|"--working_dir"             ) WD="$1"; shift;;
      *                                 ) echo "ERROR: Invalid option: \""$opt"\"" >&2
      exit 1;;
    esac
  done
fi



# ERROR HANDLING OF MISSING MANDATORY ARGUMENTS
# TODO
if [[ "$OD" == "" || "$NAME" == "" || "$WD" == "" ]]; then
  echo "ERROR: Option -od, -nm, -wd require arguments." >&2
  exit 1
fi


# have bam, have sco, have ref FAIL, wait for input of which one to do
if [[ "$BAM" != ""  && "$SCO" != "" && "$REF_GENOME" != "" ]]; then
  echo "Press 1: Run from BAM and SCO (fast)"
  echo "Press 2: Run from reference genome (slow)"
  read -n 1 -p "Input Selection:" input
  if [[ $input == "2" ]]; then
    $CALC_SCO=true
  elif [[ $input == "1" ]]; then
    $CALC_SCO=false
  else
    echo "ERROR: You have entered an invalid selection, please rerun correctly"
    exit 1
  fi
fi

# have bam, no sco, have ref FAIL, wait for input to do busco/mmseq or include sco
if [[ "$BAM" != ""  && "$SCO" == "" && "$REF_GENOME" != "" ]]; then
  echo "Press 1: Program will exit and please run again providing BAM"
  echo "Press 2: Run from reference genome (slow)"
  read -n 1 -p "Input Selection:" input
  if [[ $input == "1" ]]; then
    exit 1
  elif [[ $input == "2" ]]; then
    $CALC_SCO=true
  else
    echo "ERROR: You have entered an invalid selection, please rerun correctly"
    exit 1
  fi
fi

# have bam, no sco, no ref FAIL, missing sco
if [[ "$BAM" != ""  && "$SCO" == "" && "$REF_GENOME" == "" ]]; then
  echo "ERROR: Missing single copy ortholog .tsv (-sco)"
  exit 1
fi

# no bam, have sco, no ref FAIL, missing BAM
if [[ "$BAM" == ""  && "$SCO" != "" && "$REF_GENOME" == "" ]]; then
  echo "ERROR: Missing .bam (-bam)"
  exit 1
fi

# no bam, no sco, no ref FAIL, missing stuff
if [[ "$BAM" == ""  && "$SCO" == "" && "$REF_GENOME" == "" ]]; then
  echo "Either provide a reference genome (slow) OR provide a bam and corresponding sco file (fast)"
  exit 1
fi

if [[ "$BAM" != ""  && "$SCO" != "" && "$REF_GENOME" == "" ]]; then
  continue
elif [[ "$BAM" == ""  && "$SCO" == "" && "$REF_GENOME" != "" ]]; then
  continue
else
  echo "Either provide a reference genome (slow) OR provide a bam and corresponding sco file (fast)"
  exit 1
fi


LOG=${OD}/pipeline_log.txt
echo "Error handling of arguments complete, you may now close the terminal"
echo "---"
echo "Make sure to check pipeline_log.txt before using results in \
case the script terminated unexpectedly."

exec 3>&1 1>>${LOG} 2>&1 	# handles printing of messages to log and terminal

echo "===========================================================" >> ${LOG}
echo [$(date)] "PID: $$" >> ${LOG}
echo "===========================================================" >> ${LOG}

# Print current envrionment variables
echo "BAM =${BAM}"
echo "OUTPUT_DIRECTORY = ${OD}"
echo "SCO = ${SCO}"
echo "NAME = ${NAME}"
echo "REF_GENOME = ${REF_GENOME}"

echo "===========================================================" >> ${LOG}

# # Running BUSCO or MMSeq2 would happen up here (Epic Story 4)
# # TODO


# Compute array of assumptions to try
python3 ${WD}/code/assumptions.py ${WD}/assumptions.txt


echo "===========================================================" >> ${LOG}

# Run the different combinations of variable (python generated)
for assumptions in ${WD}/assumptions.txt; do

  # run run.pbs, launching parralel jobs
  echo "qsub v bam=${BAM},wd=${WD},od=${OD},sco=${SCO},name=${NAME},filter_len=${FILTER_LEN},method=${METHOD},assumptions=${assumptions} run.pbs"
  qsub -v bam=${BAM},wd=${WD},od=${OD},sco=${SCO},name=${NAME},filter_len=${FILTER_LEN},method=${METHOD},assumptions=${assumptions} run.pbs > ${JOBID}
  echo $JOBID

done


## DELETE AND TIDY FILES



## PRINTS DURATION OF SCRIPT
echo "$((${SECONDS} / 3600)) hours, $(((${SECONDS} / 60) % 60)) minutes and $((${SECONDS} % 60)) seconds elapsed" >> ${LOG}
echo [$(date)] "COMPLETED PIPELINE for: ${NAME}" >> ${LOG}
echo "===========================================================" >> ${LOG}


