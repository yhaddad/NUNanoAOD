#!/bin/bash

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
python condor_WSProducer.py --jobNum=$1 --isMC=0 --era=2016 --infile=$2
echo "----- transfer output to eos :"
xrdcp -s -f tree_$1.root root://eoscms.cern.ch//store/group/phys_exotica/monoZ/Exorcism2016_WS_MT/DoubleEG_Run2016C-Nano1June2019-v1/
echo "----- directory after running :"
ls -lR .
echo " ------ THE END (everyone dies !) ----- "
