#!/bin/sh

# Author: Chelsea Liang

# This main script launches the investigation of each viable combination of assumptions
	# you may exit the shell when following is printed to the terminal:
	# "Completed error checking inputs, pipeline will complete in background"
# run with:
# mkdir -p ${od}; ./main.sh -od ${od} -nm ${name} -wd ${wd} -b ${bam} -sco ${sco} -t ${threads} &
# disown -h %1

# CHELSEA
# name=e_coli
# od=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/output/test_e_coli
# bam=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/e_coli/bam/e_coli.bam
# sco=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/e_coli/busco3/run_e_coli/full_table_e_coli.tsv
# wd=$(pwd)
# threads=2

# name=s_cerevisiae
# od=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/output/s_cerevisiae
# bam=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/s_cerevisiae/bam/s_cerevisiae.bam
# sco=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/s_cerevisiae/busco3/run_s_cerevisiae/full_table_s_cerevisiae.tsv
# wd=$(pwd)
# threads=2

# name=c_elegans
# od=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/output/c_elegans
# bam=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/c_elegans/bam/c_elegans.bam
# sco=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/c_elegans/busco3/run_c_elegans/full_table_c_elegans.tsv
# wd=$(pwd)
# threads=4

# name=m_musculus
# od=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/output/m_musculus
# bam=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/m_musculus/bam/m_musculus.bam
# sco=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/m_musculus/busco3/run_m_musculus/full_table_m_musculus.tsv
# wd=$(pwd)
# threads=4

# name=d_melanogaster
# od=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/output/d_melanogaster
# bam=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/d_melanogaster/bam/d_melanogaster.bam
# sco=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/d_melanogaster/busco3/run_d_melanogaster/full_table_d_melanogaster.tsv
# wd=$(pwd)
# threads=4

# name=a_thaliana
# od=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/output/a_thaliana
# bam=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/a_thaliana/bam/a_thaliana.bam
# sco=/srv/scratch/z3452659/BINF6112-Sep20/TeamGenomeSize/data/2020-09-22.ReferenceGenomes/a_thaliana/busco3/run_a_thaliana/full_table_a_thaliana.tsv
# wd=$(pwd)
# threads=4




# setting default flags
CALC_SCO=false
FILTER_LEN=5000
THREADS=2


## LOGS AND ERRORS
set -e						# if any error occurs, exit 1


###############
## Variables ##
###############

# Mandatory:
# - ${OD}, path of the working/output directory of script
# - ${NAME}, rootname for files created by pipeline
# - #{WD}, path to top level of code i.e. same level as this main.sh script

# Optional:
# - ${REF_GENOME}, path to reference genome
# - ${SCO}, path to tsv of BUSCO single copy ortholog output
# - ${BAM}, path to bam file of mapped reads
# - ${THREADS}, number of threads to run samtools computations


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
      "-t"|"--threads"                  ) THREADS="$1"; shift;;
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
touch ${LOG}

# exec 3>&1 1>>${LOG} 2>&1 	# handles printing of messages to log and terminal


{
echo "===========================================================" 
echo [$(date)] "PID: $$" 
echo "===========================================================" 

# Print current envrionment variables
echo "BAM =${BAM}"
echo "OUTPUT_DIRECTORY = ${OD}"
echo "SCO = ${SCO}"
echo "NAME = ${NAME}"
echo "REF_GENOME = ${REF_GENOME}"

echo "===========================================================" 

# Running BUSCO or MMSeq2 would happen up here (Epic Story 4)
# TODO


echo "===========================================================" 

echo "[Compute all intermediary files]"
PRELIM_PROCESS_ID=$(qsub \
-o ${OD} \
-l select=${THREADS}:ncpus=1:mem=4gb \
-v bam=${BAM},wd=${WD},od=${OD},sco=${SCO},name=${NAME},filter_len=${FILTER_LEN} \
${WD}/code/run_samtools.pbs | cut -d'.' -f1)
echo "PRELIM_PROCESS_ID is ${PRELIM_PROCESS_ID}"

echo "===========================================================" 

echo "[Compute array of assumptions to try]"
python3 ${WD}/code/assumptions.py ${WD}/assumptions.txt

echo "===========================================================" 

echo "[Run run.pbs, launching parralel genome calculations]"
while read ASSUMPTIONS; do
  METHOD=$( echo ${ASSUMPTIONS} | cut -d',' -f1 | cut -d'=' -f2 )
  INDEL=$( echo ${ASSUMPTIONS} | cut -d',' -f2 | cut -d'=' -f2 )
  R_CLIPPING=$( echo ${ASSUMPTIONS} | cut -d',' -f3 | cut -d'=' -f2 )

  JOBID=$(qsub \
  -o ${OD} \
  -W depend=afterok:${PRELIM_PROCESS_ID} \
  -v WD=${WD},OD=${OD},NAME=${NAME},METHOD=${METHOD},INDEL=${INDEL},R_CLIPPING=${R_CLIPPING},FILTER_LEN=${FILTER_LEN} \
  ${WD}/run.pbs)
  echo "qsub jobid is ${JOBID}"
done < ${WD}/assumptions.txt

echo "===========================================================" 
echo "[Delete and tidy files]"

chmod -R 775 ${OD}

echo "===========================================================" 
echo [$(date)] "ALL JOBS LAUNCHED for: ${NAME}" 
echo "Make sure to check pipeline_log.txt which has a record of"
echo "this command line output. Check the qsub logs before using"
echo "results in case the script terminated unexpectedly."
echo "===========================================================" 
} | tee -a ${LOG}

