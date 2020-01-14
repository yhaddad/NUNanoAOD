#!/bin/bash

export X509_USER_PROXY=/afs/cern.ch/user/c/cfreer/x509up_u85831
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc630

cd /afs/cern.ch/work/c/cfreer/MonoZ_2019/MT_plots/CMSSW_10_6_4/src/
eval `scramv1 runtime -sh`
echo
echo $_CONDOR_SCRATCH_DIR
cd   $_CONDOR_SCRATCH_DIR
echo
echo "... start job at" `date "+%Y-%m-%d %H:%M:%S"`
echo "----- directory before running:"
ls -lR .
echo "----- CMSSW BASE, python path, pwd:"
echo "+ CMSSW_BASE  = $CMSSW_BASE"
echo "+ PYTHON_PATH = $PYTHON_PATH"
echo "+ PWD         = $PWD"
echo "----- Found Proxy in: $X509_USER_PROXY"
python condor_Run2_proc.py --jobNum=$1 --isMC=1 --era=2018 --infile=$2
echo "----- transfert output to eos :"
xrdcp -s -f tree_$1.root root://eoscms.cern.ch//store/group/phys_exotica/monoZ/ADD_Truncation_v2_2018/ADDMonoZ_MD_1_d_3/
echo "----- directory after running :"
ls -lR .
echo " ------ THE END (everyone dies !) ----- "
