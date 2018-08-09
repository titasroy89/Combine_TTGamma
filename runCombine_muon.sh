#!/bin/bash

job=$1
#extraOptions=$2

if [ -z ${_CONDOR_SCRATCH_DIR} ] ; then 
	echo "Running Interactively" ; 
else
	echo "Running In Batch"
	cd ${_CONDOR_SCRATCH_DIR}
	echo ${_CONDOR_SCRATCH_DIR}
	echo "xrdcp root://cmseos.fnal.gov//store/user/"${USER}"/CombineBuild_CMSSW_8_1_0.tgz ."
	xrdcp root://cmseos.fnal.gov//store/user/${USER}/CombineBuild_CMSSW_8_1_0.tgz .
	echo "tar -xvf CombineBuild_CMSSW_8_1_0.tgz"
	tar -xzf CombineBuild_CMSSW_8_1_0.tgz
	rm CombineBuild_CMSSW_8_1_0.tgz
	cd CMSSW_8_1_0/src/
	source /cvmfs/cms.cern.ch/cmsset_default.sh
    scram b ProjectRename
	eval `scramv1 runtime -sh`
	cd ../../
fi

python runImpactToys.py -d datacard_muons -t 10 
echo "python runImpactToys.py -d datacard_muons -t 10"
echo "rm higgs*"
rm higgs*

#echo "mkdir Job_$job"
mkdir Job_$job

mv impacts_* Job_$job/.

tar -zcf Job_$job.tgz Job_$job

echo "xrdcp -r -f Job_$job.tgz root://cmseos.fnal.gov//store/user/troy2012/muons/."
xrdcp -r -f Job_$job.tgz root://cmseos.fnal.gov//store/user/troy2012/muons/.

#rm impacts_*
rm Job_$job.tgz
#echo "rm combine_logger.out"
rm combine_logger.out


