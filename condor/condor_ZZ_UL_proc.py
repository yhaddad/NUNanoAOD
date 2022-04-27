import os, sys, re
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
# import PSet
import yaml
#Import the NanoAOD-tools that we will need
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetSysColl import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.muonScaleResProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lepSFProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
#Import the MonoZ analysis tools
from PhysicsTools.MonoZ.ZZProducer import *
from PhysicsTools.MonoZ.VBSProducer import *
from PhysicsTools.MonoZ.GenWeightProducer import *
from PhysicsTools.MonoZ.EWProducer import *
from PhysicsTools.MonoZ.PhiXYCorrection import *
from PhysicsTools.MonoZ.BtagEventWeightProducer import *
from PhysicsTools.MonoZ.TriggerSFProducer import *
from PhysicsTools.MonoZ.GenMonoZProducer import *
import argparse


def inputfile(nanofile):
   tested   = False
   forceaaa = False
   pfn=os.popen("edmFileUtil -d %s"%(nanofile)).read()
   pfn=re.sub("\n","",pfn)
   print nanofile," -> ",pfn
   if (os.getenv("GLIDECLIENT_Group","") != "overflow" and
       os.getenv("GLIDECLIENT_Group","") != "overflow_conservative" and not
       forceaaa ):
      if not tested:
         print "Testing file open"
         testfile=ROOT.TFile.Open(pfn)
         if testfile and testfile.IsOpen() :
            print "Test OK"
            nanofile=pfn
            testfile.Close()
         else:
            if "root://cms-xrd-global.cern.ch/" not in nanofile:
               nanofile = "root://cms-xrd-global.cern.ch/" + nanofile
            forceaaa=True
      else:
         nanofile = pfn
   else: 
      if "root://cms-xrd-global.cern.ch/" not in nanofile: 
         nanofile = "root://cms-xrd-global.cern.ch/" + nanofile
   return nanofile


parser = argparse.ArgumentParser("")
parser.add_argument('-isMC'   , '--isMC'   , type=int, default=1     , help="")
parser.add_argument('-isUL'   , '--isUL'   , type=int, default=1     , help="")
parser.add_argument('-jobNum' , '--jobNum' , type=int, default=1     , help="")
parser.add_argument('-era'    , '--era'    , type=str, default="2018", help="")
parser.add_argument('-doSyst' , '--doSyst' , type=int, default=1     , help="")
parser.add_argument('-infile' , '--infile' , type=str, default=None  , help="")
parser.add_argument('-dataset', '--dataset', type=str, default="X"   , help="")
parser.add_argument('-nevt'   , '--nevt'   , type=str, default=-1    , help="")
parser.add_argument('-json'   , '--json'   , type=str, default=None  , help="")
options  = parser.parse_args()
options.infile = inputfile(options.infile)


if options.isMC:
   condtag_ = "NANOAODSIM"
   if options.dataset == "X":
      options.dataset = options.infile
      options.dataset = options.dataset.split('/store')[1].split("/")
      condtag_ = options.dataset[5]
      options.dataset = options.dataset[3]
   print "[check] condtag_ == ", condtag_
   print "[check] dataset  == ", options.dataset
else:
   if options.dataset == "X":
      options.dataset = options.infile
      options.dataset = options.dataset.split('/store')[1].split("/")
      condtag_ = options.dataset[2]
      options.dataset = options.dataset[3]
   else:
      options.dataset = options.dataset.split("/")
      condtag_ = options.dataset[2]
      options.dataset = options.dataset[1]


# Use EE noise mitigation for 2017
metBranchName = "METFixEE2017" if options.era=="2017" else "MET"

# pre selections before analyzer
pre_selection  = "((Sum$(Electron_pt>20 & &abs(Electron_eta)<2.5) + Sum$(Muon_pt>20 && abs(Muon_eta)<2.5) )>=2)"
pre_selection += " && Flag_METFilters"
if float(options.nevt) > 0:
   print " passing this cut and : ", options.nevt
   pre_selection += ' && (Entry$ < {})'.format(options.nevt)

print "---------------------------"
print " -- options   = ", options
print " -- is MC     = ", options.isMC
print " -- is UL     = ", options.isUL
print " -- jobNum    = ", options.jobNum
print " -- era       = ", options.era
print " -- in file   = ", options.infile
print " -- dataset   = ", options.dataset
print " -- candtag   = ", condtag_
print " -- METname   = ", metBranchName
print "---------------------------"

# HLTs for all 3 years
with open("HLT_Run2_UL.yaml", 'r') as f_yml:
   dict_HLT = yaml.load(f_yml, Loader=yaml.FullLoader)

# module list for PostProcessor
modules_era = []
modules_era.append(GenWeightProducer(isMC=options.isMC, dopdf=True ) )

if options.isMC:
   jmeCorrections = createJMECorrector(isMC=True, dataYear='UL'*options.isUL + options.era, jesUncert="Total", metBranchName=metBranchName)
   if options.era=="2016":
      modules_era.append(puAutoWeight_2016())
      modules_era.append(PrefCorr())
      modules_era.append(muonScaleRes2016())
      modules_era.append(lepSF_2016())
      modules_era.append(btagSFProducer("UL2016", algo="deepjet", selectedWPs=['L']))
      modules_era.append(BtagEventWeight_2016())
   elif options.era=="2017":
      modules_era.append(puAutoWeight_2017())
      modules_era.append(PrefCorr())
      modules_era.append(muonScaleRes2017())
      modules_era.append(lepSF_2017())
      modules_era.append(btagSFProducer("UL2017", algo="deepjet", selectedWPs=['L']))
      modules_era.append(BtagEventWeight_2017())
   elif options.era=="2018":
      modules_era.append(puAutoWeight_2018())
      modules_era.append(muonScaleRes2018())
      modules_era.append(lepSF_2018())
      modules_era.append(btagSFProducer("UL2018", algo="deepjet", selectedWPs=['L']))
      modules_era.append(BtagEventWeight_2018())

   # WZ or ZZ sample for ewk corrections and ADD for EFT weights
   if "ZZTo" in options.dataset and "GluGluToContin" not in options.dataset and "ZZJJ" not in options.dataset:
      modules_era.append(EWProducer(1, True))
   if "WZTo" in options.dataset:
      modules_era.append(EWProducer(2, False))

   modules_era.append(jmeCorrections())
   modules_era.append(PhiXYCorrection(era=options.era, isMC=options.isMC, isUL=options.isUL, sys='', metBranchName=metBranchName))
   modules_era.append(GenMonoZProducer())
   modules_era.append(ZZProducer(isMC=options.isMC, era=str(options.era), do_syst=1, syst_var=''))
   modules_era.append(VBSProducer(isMC=options.isMC, era=str(options.era), do_syst=1, syst_var=''))
   modules_era.append(TriggerSFProducer(era=options.era, verbose=False, doSysVar=True))

   # for shift-based systematics
   for sys in ["ElectronEn", "MuonEn", "jesTotal", "jer"]:
      if options.doSyst != 1:
         continue
      for var in ["Up", "Down"]:
         if "jesTotal" in sys or "jer" in sys: 
            modules_era.append(PhiXYCorrection(era=options.era, isMC=options.isMC, isUL=options.isUL, sys=sys+var, metBranchName=metBranchName))
         modules_era.append(ZZProducer(options.isMC, str(options.era), do_syst=1, syst_var=sys+var))
         modules_era.append(VBSProducer(isMC=options.isMC, era=str(options.era), do_syst=1, syst_var=sys+var))

   # not applying HLT to MC
   # hlt_ls = [_hlt for _hlt_ls in dict_HLT[options.era].values() for _hlt in _hlt_ls]
   # pre_selection = pre_selection + " && (" + ' || '.join(hlt_ls) + ")"

else: 
   # Data
   ds_names = {'2016' : ['MuonEG', 'DoubleEG', 'DoubleMuon', 'SingleElectron', 'SingleMuon'], 
               '2017' : ['MuonEG', 'DoubleEG', 'DoubleMuon', 'SingleElectron', 'SingleMuon'], 
               '2018' : ['MuonEG', 'DoubleMuon', 'SingleMuon', 'EGamma']}

   # use HLT to remove duplicated events
   dict_combHLT = {}
   hlt_passed_list = []
   for _ds in ds_names[options.era]:
      # combined HLT for a single dataset
      hlt_this_list = dict_HLT[options.era][_ds]
      hlt_this_str = '(' + ' || '.join(hlt_this_list) + ')'

      if dict_combHLT:
         # remove events from previous datasets
         hlt_passed_str = '(' + ' || '.join(hlt_passed_list) + ')'
         str_combHLT = ' && !'.join([hlt_this_str, hlt_passed_str])
         dict_combHLT[_ds] = str_combHLT
      else:
         # 1st dataset
         str_combHLT = hlt_this_str
         dict_combHLT[_ds] = str_combHLT

      # list of HLTs of previous datasets
      hlt_passed_list.extend(hlt_this_list)

   pre_selection = pre_selection + " && (" + dict_combHLT[options.dataset] + ")"

   # JSON input
   json_inputs = {
      '2016': 'Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt',
      '2017': 'Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt',
      '2018': 'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt',
   }
   options.json = json_inputs[options.era]
   print " -- JSON used is : ", options.json

   # modules for data
   runPeriod = condtag_.split(options.era)[1][:1]
   jmeCorrections = createJMECorrector(isMC=False, 
                                       dataYear='UL'*options.isUL + options.era, 
                                       runPeriod=runPeriod, 
                                       jesUncert="Total", 
                                       metBranchName=metBranchName)
   modules_era.append(jmeCorrections())
   modules_era.append(PhiXYCorrection(era=options.era, isMC=options.isMC, isUL=options.isUL, sys='', metBranchName=metBranchName))
   modules_era.append(ZZProducer  (isMC=options.isMC, era=str(options.era), do_syst=1, syst_var=''))
   modules_era.append(VBSProducer(isMC=options.isMC, era=str(options.era), do_syst=1, syst_var=''))


for i in modules_era:
   print "modules : ", i

print "Selection : ", pre_selection

p = PostProcessor(".", [options.infile], 
                  cut=pre_selection, 
                  branchsel="keep_and_drop.txt", 
                  outputbranchsel="keep_and_drop.txt", 
                  haddFileName="tree_%s.root" % str(options.jobNum), 
                  modules=modules_era, 
                  provenance=True, 
                  noOut=False, 
                  fwkJobReport=True, 
                  jsonInput=options.json )
p.run()
