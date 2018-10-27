import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.monoZ.JetProducer import *
from PhysicsTools.NanoAODTools.postprocessing.monoZ.MonoZProducer import *

from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.mht import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetSysColl import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
# from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
import argparse


isMC = True
era = "2017"
dataRun = ""

parser = argparse.ArgumentParser("")
parser.add_argument('-isMC', '--isMC', type=int, default=1, help="")
parser.add_argument('-jobNum', '--jobNum', type=int, default=1, help="")
parser.add_argument('-era', '--era', type=str, default="2017", help="")
parser.add_argument('-doSyst', '--doSyst', type=int, default=0, help="")
parser.add_argument('-dataRun', '--dataRun', type=str, default="X", help="")

options  = parser.parse_args()
print(" -- options = ", options)
isMC = options.isMC
era = options.era
dataRun = options.dataRun

print("isMC = ", isMC, "era = ", era, "dataRun = ", dataRun)

files = [
    #"root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAOD/DYJetsToLL_M-50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/08884C40-C7A4-E811-A882-3C4A92F7DE0E.root"
    "root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAOD/ZZTo4L_13TeV_powheg_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/00000/04664F82-5F43-E811-808C-0025905A48C0.root"
    #"root://cms-xrd-global.cern.ch//store/data/Run2017B/DoubleMuon/NANOAOD/31Mar2018-v1/110000/9EB58CB8-1C47-E811-9382-FA163E67A014.root"
    #"root://cms-xrd-global.cern.ch//store/data/Run2017B/SingleMuon/NANOAOD/31Mar2018-v1/20000/BA1FD7CE-E546-E811-8F21-0025905B861C.root"
]

pre_selection = " || ".join([
    "Sum$(Electron_pt>20&&abs(Electron_eta)<2.5) + Sum$(Muon_pt>20&&abs(Muon_eta)<2.5)>=1"
])

pre_selection = " && ".join([pre_selection, "(Entry$ < 20000)"])
#pre_selection = "(Entry$ < 2000)"
print("pre_selection : ", pre_selection)

#modules_2017 = [
#    jetmetUncertainties2017All(),
#    JetProducer(systvals=['jesTotalUp', 'jesTotalUp'], jetSelection= lambda j : j.pt > 30),
#]
modules_2017 = [
    #puAutoWeight(),
    #muonScaleRes2017(),
    #btagSFProducer("2017", "deepcsv"),
    MonoZProducer(options.isMC, str(options.era))
]


p = PostProcessor(
    ".", files, cut=pre_selection,
    #branchsel="keep_and_drop.txt",
    #outputbranchsel="keep_and_drop.txt",
    modules=modules_2017,
    provenance=True,
    noOut=False,
    fwkJobReport=True,
    # jsonInput=runsAndLumis()
)

p.run()
