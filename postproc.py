import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
# import PSet
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.monoZ.MonoZProducer import *
from PhysicsTools.NanoAODTools.postprocessing.monoZ.GenMonoZProducer import *
from PhysicsTools.NanoAODTools.postprocessing.monoZ.GlobalWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.mht import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

import argparse


parser = argparse.ArgumentParser("")
parser.add_argument('-isMC'   , '--isMC'   , type=int, default=1     , help="")
parser.add_argument('-jobNum' , '--jobNum' , type=int, default=1     , help="")
parser.add_argument('-era'    , '--era'    , type=str, default="2017", help="")
parser.add_argument('-doSyst' , '--doSyst' , type=int, default=0     , help="")
parser.add_argument('-dataset', '--dataset', type=str, default="X"   , help="")
parser.add_argument('-catalog', '--catalog', type=str, default="configs/catalogue_2017.yaml", help="")
options  = parser.parse_args()
print "---------------------------"
print " -- options  = ", options 
print " -- is MC    = ", options.isMC
print " -- jobNum   = ", options.jobNum
print " -- era      = ", options.era
print " -- dataset  = ", options.dataset
print " -- catalog  = ", options.catalog
print "---------------------------"

lumiWeight  = 1.0
if options.isMC:
   from PhysicsTools.NanoAODTools.postprocessing.monoZ.catalog_2017 import catalog
   condtag_ = "NANOAODSIM"
   if options.dataset == "X":
      options.dataset = inputFiles().value()[0]
      options.dataset = options.dataset.split('store/mc/RunIIFall17NanoAOD/')[1]
      condtag_ = options.dataset.split('/')[2]
      options.dataset = options.dataset.split('/NANOAODSIM/')[0]
   for ds, m in catalog.items():
      if options.dataset == m.get("sample", "") and condtag_ in ds:
         # ----- 
         lumiWeight = 1000.0 * m.get("xsec")
         lumiWeight *= m.get("br", 1.0)
         lumiWeight *= m.get("kf", 1.0)
         lumiWeight = lumiWeight/float(m.get("nevents", 1))
         print "---------------------------"
         print "sample     == ", m.get("sample", "")
         print "dataset    == ", ds
         print "xsection   == ", m.get("xsec"), " [pb]"
         print "nevents    == ", m.get("nevents", 1)
         print "lumiWeight == ", lumiWeight
         break
   else:
      lumiWeight = 1.0
      print "---------------------------"
      print "lumiWeight == ", lumiWeight



HLT_paths = [
   # DiElectron (DoubelEG)
   "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL",
   "HLT_DoubleEle33_CaloIdL_MW",
   
   # DiMuon (DoubleMuon)
   "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",
   "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8",
   
   # MuonElectron
   "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
   "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
   "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
   "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
   "HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ",
   "HLT_Mu8_DiEle12_CaloIdL_TrackIdL",
   "HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ",
   
   # TriElectron
   "HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL",
   
   # TriMuon
   "HLT_TripleMu_10_5_5_DZ",
   "HLT_TripleMu_12_10_5",
   
   # SingleElectron
   "HLT_Ele35_WPTight_Gsf",
   "HLT_Ele38_WPTight_Gsf",
   "HLT_Ele40_WPTight_Gsf",
   
   # Single Mu
   "HLT_IsoMu27",

   # HLTs not in our original list
   "HLT_Ele115_CaloIdVT_GsfTrkIdT",
   "HLT_Ele27_WPTight_Gsf",
   "HLT_Ele32_WPTight_Gsf",
   "HLT_Ele32_WPTight_Gsf_L1DoubleEG",
   "HLT_Photon200",
   "HLT_IsoMu24",
   "HLT_IsoMu30",
   "HLT_Mu50",
   "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8",
   "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8",
   "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ",
   "HLT_DiEle27_WPTightCaloOnly_L1DoubleEG",
   "HLT_DoubleEle25_CaloIdL_MW",
   "HLT_DoublePhoton70",
   "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
   # These 2 triggers do not exist
   # "HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ",
   # "HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL",
   "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL"
] 

dic_HLT_NotIn = {
   "C": [
      "HLT_Ele32_WPTight_Gsf",
      "HLT_IsoMu30",
      "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8",
      "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8",
      "HLT_DoubleEle25_CaloIdL_MW"
   ],
   "B": [
      "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",
      "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
      "HLT_Ele115_CaloIdVT_GsfTrkIdT",
      "HLT_Ele32_WPTight_Gsf",
      "HLT_IsoMu30",
      "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8",
      "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8",
      "HLT_DiEle27_WPTightCaloOnly_L1DoubleEG",
      "HLT_DoubleEle25_CaloIdL_MW",
      "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
      "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL"
   ]
}

# This has only been tested on 2017 samples
if not options.isMC:
   letter = options.dataset.split('/')[2][7]
   if letter == 'B' or (letter == 'C' and options.dataset.split('/')[1] != 'MuonEG'):
      HLT_paths = [ HLT for HLT in HLT_paths if HLT not in dic_HLT_NotIn[letter] ]

pre_selection = "( ( Sum$(Electron_pt>20&&abs(Electron_eta)<2.5) + Sum$(Muon_pt>20&&abs(Muon_eta)<2.5) )>=1 )"
pre_selection = pre_selection + " && (" + "||".join(HLT_paths) + ")"

modules_2017 = [
   GlobalWeightProducer(options.isMC, lumiWeight), 
   MonoZProducer(options.isMC, str(options.era))
]

if options.isMC:
   modules_2017.insert(0, puAutoWeight())
   modules_2017.insert(1, GenMonoZProducer())
   #modules_2017.insert(2, btagSFProducer("2017", "deepcsv"))
   modules_2017.insert(2, muonScaleRes2017())

if options.doSyst:
   modules_2017.insert(
      0, jetmetUncertainties2017All()
   )
   modules_2017.insert(
      1, MonoZProducer(
         isMC=options.isMC, era=str(options.era),
         do_syst=options.doSyst, syst_var='jesTotalUp'
   )
   )
   modules_2017.insert(
      2, MonoZProducer(
      isMC=options.isMC, era=str(options.era),
         do_syst=options.doSyst, syst_var='jesTotalDown'
      )
   )

p = PostProcessor(
   ".", inputFiles(), 
   cut=pre_selection,
   branchsel="keep_and_drop.txt",
   outputbranchsel="keep_and_drop_post.txt",
   modules=modules_2017,
   provenance=True,
   noOut=False,
   fwkJobReport=True,
   jsonInput=runsAndLumis()
)

p.run()
