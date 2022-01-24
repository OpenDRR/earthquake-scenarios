#!/bin/bash
# ==========================================================================
# Script for running scenario calculations in the National Canada Risk Model
# ==========================================================================
usage() {
echo "Script for running scenario calculations in OpenQuake, using Canadian data. 
You need to have created the hazard, damage, and risk files already, as well as 
functions called therein. Written by Tiegan E. Hobbs, last major update on 10 Dec 2020.


USAGE: run_OQStandard.sh NAME [-h -d -r -[b/o] -[s] -[l]]
    where NAME is the coding for the model run.
    No flags defaults to a full suite of calculations for all retrofits, assuming building level exposure files.
    Optional flags to run a subset of the calculations:
        -h [h]azard
        -d [d]amage and consequence
        -r [r]isk
        -b [b]aseline condition
        -o baseline + [o]ne extra retrofit (level r1)
        -t run retrofit level [t]wo (r2)
	    -s ini files call a site level exposure file, else default is building level
        -l run using personal laptop (not AWS)
    EXAMPLE 1: run_OQStandard.sh AFM7p3_GSM
    EXAMPLE 2: run_OQStandard.sh AFM7p3_GSM -d -b

"
}

#if [[ $LAPTOP != 'True' ]]; then
### SETUP AWS KILL 
#shut_down_ec2_instance() {
#    echo "Shutting down EC2 instance"
#    sudo shutdown
#    }
#
#trap "shut_down_ec2_instance" ERR
#fi

#    INITIALIZATION
#Set below flags to 0 to skip those elements of run, and to 1 to include. For retrofits, set flag to 0 for baseline, 1 for baseline plus one level of retrofit, and 2 for baseline plus two levels of retrofit.
HAZFLAG="0"; DMGFLAG="0"; RSKFLAG="0"; RETROFLAG="2"; EXPO='b'
if [ $# -eq "0" ]; then
    usage
    exit 0
else
    echo "------------------------------------------------"
    echo "CHECKING FILES AND CONFIGURATION"
    echo "------------------------------------------------"
    NAME=$1; shift
    if [ $# -eq "0" ]; then
        echo "Running the full suite."
        HAZFLAG="1"; DMGFLAG="1"; RSKFLAG="1"; RETROFLAG="2"
    else
        echo "Reading specifications from flags."
        while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
            -d )
                DMGFLAG="1"
                ;;
            -h )
                HAZFLAG="1"
                ;;
            -r )
                RSKFLAG="1"
                ;;
            -b )
                RETROFLAG="0"
                ;;
            -o )
                RETROFLAG="1"
                ;;
            -t )
                RETROFLAG="2"
                ;;
            -s ) 
		        EXPO='s'
		        ;;
            -l )
                LAPTOP='True'
                ;;
        esac; shift; done
    fi
fi

#source ~/.profile
mkdir -p ./temp/
rm -f ./temp/*
OUTDIR="outputs"
mkdir -p ./${OUTDIR}/
echo "Outputs will be placed in '${OUTDIR}'"
JOBDIR="initializations"
#JOBDIR="job-files"

if [[ $LAPTOP == 'True' ]]; then
    SCRIPTS_LOC="/Users/thobbs/Documents/GitHub/earthquake-scenarios/scripts/"
    CONSQ_LOC=${SCRIPTS_LOC}"consequences-v3.10.0_Laptop.py"
else
    SCRIPTS_LOC="/mnt/storage/earthquake-scenarios/scripts/"
    CONSQ_LOC=${SCRIPTS_LOC}"consequences-v3.10.0.py"
fi
AVGHAZLOC=${SCRIPTS_LOC}"weightHAZ.py"
AVG_LOC=${SCRIPTS_LOC}"weightedAverage.py"

if [[ $HAZFLAG == "1" ]]; then 
    echo "Preparing to run a hazard calculation."
    if [ ! -f ${JOBDIR}/s_Hazard_${NAME}.ini ]; then
      echo "Hazard file doesn't exist: ${JOBDIR}/s_Hazard_${NAME}.ini - EXITING"
      exit 0
    fi
fi
if [[ $DMGFLAG == "1" ]]; then 
    echo "Preparing to run a damage and consequence calculation."
    if [ ! -f ${JOBDIR}/s_Damage_${NAME}_b0_${EXPO}.ini ]; then #-o ! -f ${JOBDIR}/s_Damage_${NAME}_r1.ini -o ! -f ${JOBDIR}/s_Damage_${NAME}_r2.ini ]; then
      echo "Baseline damage file does not exist: ${JOBDIR}/s_Damage_${NAME}_b0_${EXPO}.ini - EXITING"
      exit 0
    fi
    expoSuffix=$EXPO
fi
if [[ $RSKFLAG == "1" ]]; then 
    echo "Preparing to run a risk calculation."
    if [ ! -f ${JOBDIR}/s_Risk_${NAME}_b0_${EXPO}.ini ]; then #-o ! -f ${JOBDIR}/s_Risk_${NAME}_r1.ini -o ! -f ${JOBDIR}/s_Risk_${NAME}_r2.ini ]; then
      echo "Baseline risk file does not exist: ${JOBDIR}/s_Risk_${NAME}_b0_${EXPO}.ini - EXITING"
      exit 0
    fi
    expoSuffix=$EXPO #`ls ${JOBDIR}/s_Risk_${NAME}_b0_?.ini | awk -F'(.ini|_)' '{print $(NF-1)}'`
    echo $expoSuffix
fi
if [[ $RETROFLAG == "2" ]]; then
    declare -a arr=("r2") #RETROFITS
    echo "Running only r2 retrofit."
elif [[ $RETROFLAG == "1" ]]; then
    declare -a arr=("b0" "r1")
    echo "Running baseline plus r1 retrofit."
else
    declare -a arr=("b0") 
    echo "Running baseline only."
fi
echo "All initialization files exist - You're ready to go."


#TESTFLAG=`ps aux | grep -v grep | grep "oq-webui" | wc | awk '$1=="1" {print "TRUE"}'`
#if [ "${TESTFLAG}" = "TRUE" ]; then
#echo "Webui running."
#else
#echo "Please run the following in another terminal:"
#echo "    oq webui start"
#exit 0
#fi


if [[ $HAZFLAG == "1" ]]; then
    echo "------------------------------------------------"
    echo "RUNNING HAZARD CALCULATION"
    echo "------------------------------------------------"
    oq engine --run ${JOBDIR}/s_Hazard_${NAME}.ini &> ./${OUTDIR}/s_Hazard_${NAME}.log;
    oq export gmf_data -1 -e csv -d temp
    CALCID=`basename temp/*gmf* .csv | awk -F'_' '{print $NF}'`
    python3 $AVGHAZLOC $NAME $CALCID
    SMSFILE="${OUTDIR}/s_sitemesh_${NAME}_${CALCID}.csv"
    mv temp/*sitemesh* ${SMSFILE}
    rm -f temp/sigma_epsilon_* temp/*gmf*.csv temp/realizations_${CALCID}.csv
fi


if [[ $DMGFLAG == "1" ]]; then
    echo "------------------------------------------------"
    echo "RUNNING DAMAGE & CONSEQUENCE CALCULATIONS"
    echo "------------------------------------------------"
    if [[ $RETROFLAG == "1" ]]; then 
        # RUN TWO CALCS WITH SHARED HAZ CALC
        oq engine --run ${JOBDIR}/s_Damage_${NAME}_${arr[0]}_${expoSuffix}.ini ${JOBDIR}/s_Damage_${NAME}_${arr[1]}_${expoSuffix}.ini &> ./${OUTDIR}/s_Damage_${NAME}_b0r1_${expoSuffix}.log;
        
        # EXPORT BASELINE, WHICH IS SECOND TO LAST CALC
        oq export damages-rlzs -2 -e csv -d temp
        oq export realizations -2 -e csv -d temp
        CALCID=` ls -t temp/avg_damages-rlz-???_* | head -1 | awk -F'[_.]' '{print $(NF-1)}'`
        python3 $AVG_LOC $NAME ${arr[0]} $CALCID $expoSuffix damage
        python3 $CONSQ_LOC -2
        declare -a files=(`ls consequences-rlz-???_-2.csv`) #conseq script doesn't know real calc id, so need to replace the "-2"
        for file in $files; do mv $file "temp/"`basename $file "-2.csv"`${CALCID}".csv"; done
        python3 $AVG_LOC $NAME ${arr[0]} $CALCID $expoSuffix consequence
        rm -f temp/consequences-rlz-???_${CALCID}.csv temp/realizations_${CALCID}.csv temp/avg_damages-rlz-???_${CALCID}.csv #clear temp dir
        
        # EXPORT RETROFIT 1, LAST CALC
        oq export damages-rlzs -1 -e csv -d temp
        oq export realizations -1 -e csv -d temp
        CALCID=` ls -t temp/avg_damages-rlz-???_* | head -1 | awk -F'[_.]' '{print $(NF-1)}'`
        python3 $AVG_LOC $NAME ${arr[1]} $CALCID $expoSuffix damage
        python3 $CONSQ_LOC -1
        mv consequences-rlz-???_${CALCID}.csv temp/
        python3 $AVG_LOC $NAME ${arr[1]} $CALCID $expoSuffix consequence
        rm -f temp/consequences-rlz-???_${CALCID}.csv temp/realizations_${CALCID}.csv temp/avg_damages-rlz-???_${CALCID}.csv #clear temp dir
        
    else
        # RUN A SINGLE CALC
        oq engine --run ${JOBDIR}/s_Damage_${NAME}_${arr[0]}_${expoSuffix}.ini > ./${OUTDIR}/s_Damage_${NAME}_${arr[0]}_${expoSuffix}.log
        oq export damages-rlzs -1 -e csv -d temp
        oq export realizations -1 -e csv -d temp
        CALCID=` ls -t temp/avg_damages-rlz-???_* | head -1 | awk -F'[_.]' '{print $(NF-1)}'`
        python3 $AVG_LOC $NAME ${arr[0]} $CALCID $expoSuffix damage
        python3 $CONSQ_LOC -1
        mv consequences-rlz-???_${CALCID}.csv temp/
        python3 $AVG_LOC $NAME ${arr[0]} $CALCID $expoSuffix consequence
        rm -f temp/consequences-rlz-???_${CALCID}.csv temp/realizations_${CALCID}.csv temp/avg_damages-rlz-???_${CALCID}.csv #clear temp dir
    fi
fi


if [[ $RSKFLAG == "1" ]]; then
    echo "------------------------------------------------"
    echo "RUNNING RISK CALCULATION"
    echo "------------------------------------------------"
    if [[ $RETROFLAG == "1" ]]; then
        # RUN TWO CALCS WITH SHARED HAZ CALC
        oq engine --run ${JOBDIR}/s_Risk_${NAME}_${arr[0]}_${expoSuffix}.ini ${JOBDIR}/s_Risk_${NAME}_${arr[1]}_${expoSuffix}.ini &> ./${OUTDIR}/s_Risk_${NAME}_b0r1_${expoSuffix}.log;
        
        # EXPORT BASELINE, WHICH IS SECOND TO LAST CALC
        oq export avg_losses-rlzs -2 -e csv -d temp;
        CALCID=`ls -t temp/avg_losses* | head -1 | awk -F'[_.]' '{print $(NF-1)}'`
        #Run weighted average script, save only that
        python3 $AVG_LOC $NAME ${arr[0]} $CALCID $expoSuffix loss
        rm -f temp/avg_losses-rlz-???_${CALCID}.csv temp/realizations_${CALCID}.csv
        
        # EXPORT RETROFIT 1, LAST CALC
        oq export avg_losses-rlzs -1 -e csv -d temp;
        CALCID=`ls -t temp/avg_losses* | head -1 | awk -F'[_.]' '{print $(NF-1)}'`
        #Run weighted average script, save only that
        python3 $AVG_LOC $NAME ${arr[1]} $CALCID $expoSuffix loss
        rm -f temp/avg_losses-rlz-???_${CALCID}.csv temp/realizations_${CALCID}.csv
    else
        # RUN A SINGLE CALC
        oq engine --run ${JOBDIR}/s_Risk_${NAME}_${arr[0]}_${expoSuffix}.ini &> ./${OUTDIR}/s_Risk_${NAME}_${arr[0]}_${expoSuffix}.log;
        oq export avg_losses-rlzs -1 -e csv -d temp;
        CALCID=`ls -t temp/avg_losses* | head -1 | awk -F'[_.]' '{print $(NF-1)}'`
        #Run weighted average script, save only that
        python3 $AVG_LOC $NAME ${arr[0]} $CALCID $expoSuffix loss
        rm -f temp/avg_losses-rlz-???_${CALCID}.csv temp/realizations_${CALCID}.csv
    fi
fi

#if [[ $LAPTOP != 'True' ]]; then
### AWS KILL
#shut_down_ec2_instance
#fi


exit 0

# =================================================================
# Spit out the 4D's
# =================================================================
DOLLARS=`awk -F',' 'dollars=$22+$24+$28 {sum += dollars} END {printf "%f",sum}' ${RISKFILE}`
DEATH=`awk -F',' '{sum += $26} END {printf "%f",sum}' ${RISKFILE}`
REDTAG=`awk -F',' 'dmg=$28+$30 {sum =+ dmg} END {printf "%f",sum}' ${DMGFILE}`
DOWNTIME=`awk -F',' '{sum += $12} END {printf "%f",sum/NR}' ${CONSFILE}`
echo 'Dollars = $'"${DOLLARS}"
echo "Deaths = ${DEATH}"
echo "Damage = ${REDTAG} red tagged buildings"
echo "Downtime = ${DOWNTIME} days, on average"
