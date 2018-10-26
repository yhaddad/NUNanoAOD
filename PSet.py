#this fake PSET is needed for local test and for crab to figure the output filename
#you do not need to edit it unless you want to do a local test using a different input file than
#the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
	"/store/mc/RunIIFall17NanoAOD/ZZTo2L2Nu_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/100000/44870790-23A3-E811-A058-AC1F6B23C594.root"
    	#'root://cms-xrd-global.cern.ch://store/mc/RunIIFall17NanoAOD/ZZTo2L2Nu_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/D6F99CDC-D6A4-E811-A6E9-0CC47A166D66.root'
    	#"root://cms-xrd-global.cern.ch://store/data/Run2017B/DoubleEG/NANOAOD/31Mar2018-v1/110000/D6344F49-2147-E811-9289-FA163E65694B.root"
	#'../../NanoAOD/test/lzma.root' ##you can change only this line
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)

