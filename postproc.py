import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.monoZ.MonoZProducer import *
from PhysicsTools.NanoAODTools.postprocessing.monoZ.GenMonoZProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.mht import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
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
    "root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAOD/DYJetsToLL_M-50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/10000/08884C40-C7A4-E811-A882-3C4A92F7DE0E.root"
]

pre_selection = " || ".join([
    "(Sum$(Electron_pt > 20) >= 2)",
    "(Sum$(Muon_pt > 20) >= 2)",
    "(Sum$(Muon_pt > 20 && Muon_tightId) >= 1)"
])
pre_selection = " && ".join([pre_selection, "(Entry$ < 50000)"])
pre_selection = "(Entry$ < 1000)"
print("pre_selection : ", pre_selection)

modules_2017 = [
    puAutoWeight(),
    muonScaleRes2017(),
    btagSFProducer("2017", "deepcsv"),
    GenMonoZProducer(),
    MonoZProducer(options.isMC, str(options.era))
]

if options.doSyst:
    modules_2017.insert(
        0, jetmetUncertainties2017All()
    )
    modules_2017.insert(
        1, MonoZProducer(
        isMC=options.isMC, era=options.era,
        do_syst=options.doSyst, syst_var='jesTotalUp')
    )
    modules_2017.insert(
        2, MonoZProducer(
        isMC=options.isMC, era=options.era,
        do_syst=options.doSyst, syst_var='jesTotalDown')
    )

p = PostProcessor(
    ".", files, cut=pre_selection,
    branchsel="keep_and_drop.txt",
    outputbranchsel="keep_and_drop.txt",
    modules=modules_2017,
    provenance=True,
    noOut=False,
)

p.run()
