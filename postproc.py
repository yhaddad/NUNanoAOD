import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import PSet
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


isMC = True
era = "2017"
dataRun = ""

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

pre_selection = "Sum$(Electron_pt>20&&abs(Electron_eta)<2.5) + Sum$(Muon_pt>20&&abs(Muon_eta)<2.5)>=1"

lumiWeight  = 1.0
if isMC:
   import yaml
   if options.dataset == "X":
      options.dataset = inputFiles().value()[0]
      options.dataset = options.dataset.split('store/mc/RunIIFall17NanoAOD/')[1]
      options.dataset = options.dataset.split('/NANOAODSIM/')[0]
   catalog = None
   with open(options.catalog, 'r') as stream:
      try:
         catalog = yaml.load(stream)
      except yaml.YAMLError as exc:
         print(exc)
   for ds, m in catalog.items():
      if options.dataset == m.get("sample", ""):
         print m.get("sample", "")
         lumiWeight = 1000.0 * m.get("xsec") 
         lumiWeight *= m.get("br", 1.0) 
         lumiWeight *= m.get("kf",1.0) 
         lumiWeight = lumiWeight/float(m.get("nevents", 1))
         print "---------------------------"
         print "xsection   == ", m.get("xsec"), " [pb]"
         print "nevents    == ", m.get("nevents", 1)
         print "lumiWeight == ", lumiWeight
         break
    
   else:
      lumiWeight = 1.0
      print "---------------------------"
      print "lumiWeight == ", lumiWeight

modules_2017 = [
   GlobalWeightProducer(options.isMC, lumiWeight), 
   MonoZProducer(options.isMC, str(options.era))
]

if options.isMC:
   modules_2017.insert(0, puAutoWeight())
   modules_2017.insert(1, GenMonoZProducer())
   modules_2017.insert(2, btagSFProducer("2017", "deepcsv"))   
   modules_2017.insert(3, muonScaleRes2017())
   
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
   outputbranchsel="keep_and_drop.txt",
   modules=modules_2017,
   provenance=True,
   noOut=False,
   fwkJobReport=False,
   jsonInput=runsAndLumis()
)

p.run()
