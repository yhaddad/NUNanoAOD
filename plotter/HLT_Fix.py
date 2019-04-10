import yaml
from ROOT import *
import ROOT
import sys
#from array import array

gROOT.SetBatch(1)

with open('ROOTfiles.yml', 'r') as f_yml:
    _dict_yml = yaml.load(f_yml)

with open('ROOTfiles_CtgryFltrd.yml', 'r') as f2_yml:
    _dict_yml_ctgry = yaml.load(f2_yml)

Dict = [
	{'dataset':'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8',				'name':'Other',			'Scale':1.0000362066412656*1.0/1000.0, 		'FillColor': 880+1, 		'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8',                   	'name':'Other',                 'Scale':1.0000377165908536*1.0/1000.0,          'FillColor': 880+1,               'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8',                   	'name':'Other',                 'Scale':1.0000360831761363*1.0/1000.0,          'FillColor': 880+1,               'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8',                   	'name':'Other',                 'Scale':1.000036739050646*1.0/1000.0,           'FillColor': 880+1,               'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8',                   	'name':'Other',                 'Scale':1.0000344760838633*1.0/1000.0,          'FillColor': 880+1,               'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8',                   		'name':'Other',                 'Scale':1.0000344984862481*1.0/1000.0,          'FillColor': 880+1,               'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8',                   		'name':'Other',                 'Scale':1.000033746620705*1.0/1000.0,           'FillColor': 880+1,               'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8',                   		'name':'Other',                 'Scale':1.0000342868480752*1.0/1000.0,          'FillColor': 880+1,               'LineColor':880+1 },
        {'dataset':'ZZTo2L2Nu_13TeV_powheg_pythia8',                   				'name':'ZZ',                    'Scale':1.6642683283450472,                     'FillColor': 800-2,               'LineColor':800-2 },
        {'dataset':'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8',                   		'name':'WZ',                    'Scale':0.11620249895326198*0.85,               'FillColor': 860-4,                'LineColor':860-4 },
        {'dataset':'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8',                   		'name':'WW',                    'Scale':0.09026903803982789,                    'FillColor': 840+2,                 'LineColor':840+2 },
        #{'dataset':'WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8',                 'name':'WW',                    'Scale':0.11620249895326198,                    'FillColor': 840+2,                 'LineColor':840+2 },
        {'dataset':'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8',                   			'name':'VVV',                   'Scale':67.8391334859334,                      	'FillColor': 900-5,                 'LineColor':900-5 },
        {'dataset':'WZZ_TuneCP5_13TeV-amcatnlo-pythia8',                   			'name':'VVV',                   'Scale':17.926871172229877,                     'FillColor': 900-5,                 'LineColor':900-5 },
        #{'dataset':'WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8',                   			'name':'VVV',                   'Scale':1.0000342868480752,                     'FillColor': 900-5,                 'LineColor':900-5 },
        #{'dataset':'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8',                   		'name':'TT',                    'Scale':0.013873208098316917,                   'FillColor': 920+1,                 'LineColor':920+1 },
        {'dataset':'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8',                   			'name':'TT',                    'Scale':1.9579072463512601,                     'FillColor': 920+1,                 'LineColor':920+1 },
        {'dataset':'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',                  		'name':'TT',                    'Scale':4.114175980028324,                      'FillColor': 920+1,                 'LineColor':920+1 },
        {'dataset':'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',                   'name':'TT',                    'Scale':2.9187223944620277,                     'FillColor': 920+1,                 'LineColor':920+1 },
        {'dataset':'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',                    'name':'TT',                    'Scale':1.4479458997439978,                     'FillColor': 920+1,                 'LineColor':920+1 },
        {'dataset':'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',             'name':'TT',                    'Scale':0.028592390600870286,                   'FillColor': 920+1,                 'LineColor':920+1 },
        {'dataset':'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',                 'name':'TT',                    'Scale':0.028646991701397357,                   'FillColor': 920+1,                 'LineColor':920+1 },
        {'dataset':'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',                  	'name':'TT',                    'Scale':0.013873005409467596,                   'FillColor': 920+1,                 'LineColor':920+1 },
        #{'dataset':'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',                   	'name':'DY',                    'Scale':0.00005603985310*5.0/6.0,               'FillColor': 900+1,                 'LineColor':900+1 },
        {'dataset':'DY1JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8',           'name':'DY',                    'Scale':0.00019966935814257948,                 'FillColor': 900+1,                 'LineColor':900+1 },
        {'dataset':'DY1JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',          'name':'DY',                    'Scale':0.016779882370808786,                   'FillColor': 900+1,                 'LineColor':900+1 },
        {'dataset':'DY1JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',          'name':'DY',                    'Scale':0.13838894560722576,                    'FillColor': 900+1,                 'LineColor':900+1 },
        {'dataset':'DY1JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',          'name':'DY',                    'Scale':1.1417575373019058,                     'FillColor': 900+1,                 'LineColor':900+1 },
        {'dataset':'DY2JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8',           'name':'DY',                    'Scale':0.0003776394424266632,                  'FillColor': 900+1,                 'LineColor':900+1 },
        {'dataset':'DY2JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',          'name':'DY',                    'Scale':0.014432142715805535,                   'FillColor': 900+1,                 'LineColor':900+1 },
        {'dataset':'DY2JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',          'name':'DY',                    'Scale':0.11950809213291834,                    'FillColor': 900+1,                 'LineColor':900+1 },
        {'dataset':'DY2JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',          'name':'DY',                    'Scale':1.0074427610853405,                     'FillColor': 900+1,                 'LineColor':900+1 },
        {'dataset':'ZZTo4L_13TeV_powheg_pythia8',                   				'name':'ZZ',                    'Scale':0.7548052739055428,                     'FillColor': 800-2,               'LineColor':800-2 }
	]

_ndatasets = len(Dict)

_datasets = [
   'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8',
   'GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8',
   'GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8',
   'GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8',
   'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8',
   'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8',
   'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8',
   'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8',
   'ZZTo2L2Nu_13TeV_powheg_pythia8',
   'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8',
   'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8',
   #'WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8',
   'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8',
   'WZZ_TuneCP5_13TeV-amcatnlo-pythia8',
   #'WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8',
   #'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',
   #'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8',
   'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8',
   'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',
   'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',
   'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',
   'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',
   'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',
   'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',
   #'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',
   'DY1JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8',
   'DY1JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',
   'DY1JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',
   'DY1JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',
   'DY2JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8',
   'DY2JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',
   'DY2JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',
   'DY2JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',
   'ZZTo4L_13TeV_powheg_pythia8']

#_ndatasets = len(_datasets)

_HLTs = [
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
   "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL"]

_nHLTs = len(_HLTs)

_PDs = [
#   'MuonEG',
   'SingleElectron',
   'SingleMuon',
   'DoubleMuon',
   'DoubleEG',
   'MuonEG']

_nPDs = len(_PDs)

#_nBins = [
#   #8,
#   30,
#   #14,
#   30,
#   32,
#   30]
_nBins = [
   #8,
   15,
   #14,
   #15,
   32]
_xLow = [
   #0,
   0,
   #0,
   #0,
   -3.2]

_xHi = [
   #8,
   300,
   #14,
  # 300,
   3.2]
   #300]

_variable = [
   #"ngood_jets",
   "Z_pt",
   #"ngood_jets",
   #"emulatedMET",
   "delta_phi_ZMet"]
   #"Z_mass"]
   #"met_pt"]
   #"sca_balance"]
   

_nVars = len(_variable)


_Stuff = [100,125,150,175,200,250,300,350,400,500,600]
_Stuff = [0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0]
#_cuts = "(lep_category==7 && Z_mass > 81 && Z_mass < 101  && Z_pt>60 && met_pt>40 && ngood_bjets==0 && delta_phi_ZMet > 2)"
#_cuts = "((lep_category==1 || lep_category==3) && Z_mass > 81 && Z_mass < 101  && Z_pt>60 && met_pt>40 && ngood_jets < 2 && ngood_bjets == 0)"   
#_cuts = "((lep_category==1 || lep_category==3) && Z_mass > 76 && Z_mass < 106 && Z_pt>60 && ngood_jets < 2 && ngood_bjets == 0 && delta_phi_ZMet > 2.8 && met_pt>100 && delta_R_ll < 1.8 && delta_phi_j_met > 0.5)" #&& vec_balance < 0.4)"# && delta_R_ll < 1.8 && delta_phi_j_met > 0.5)"
_cuts = "((lep_category==3) && Z_mass > 76 && Z_mass < 106 && Z_pt>60 && ngood_jets < 2 && ngood_bjets == 0 && met_pt>40)"# && abs(delta_phi_ZMet) > 2.8 && met_pt>100 && delta_R_ll < 1.8 && abs(delta_phi_j_met) > 0.5 )"#&& vec_balance > 0.4 && vec_balance < 1.6 )"
#_cuts = "((lep_category==1 || lep_category==3) && Z_mass > 76 && Z_mass < 106 && Z_pt>65 && met_pt<50)"
def test(_variable,_nBins,_xLow,_xHi):
   print _variable
   print _nBins
   print _xLow
   print _xHi
   prf = TProof.Open("lite://")
   hists = [None] * _ndatasets
   stk = ROOT.THStack("stk", ";;Events / Bin ")
   mc = TH1F('h', 'h', _nBins, _xLow, _xHi)
   for i in range(_ndatasets):
      #dataset = _datasets[i]
      dictionary = Dict[i]
      dataset = dictionary['dataset']
      name = dictionary['name']
      chain = TChain("Events") 
      for file in _dict_yml[dataset]['files']:
         chain.Add(file)
      chain.SetProof()
      #if dataset == 'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8': name = 'Other'
      #if dataset == 'GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8': name = 'Other'
      #if dataset == 'GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8': name = 'Other'
      #if dataset == 'GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8': name = 'Other'
      #if dataset == 'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8': name = 'Other'
      #if dataset == 'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8': name = 'Other'
      #if dataset == 'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8': name = 'Other'
      #if dataset == 'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8': name = 'Other'
      #if dataset == 'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8': name = 'TT'
      #if dataset == 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8': name = 'TT'
      #if dataset == 'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8': name = 'TT'
      #if dataset == 'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8': name = 'TT'
      #if dataset == 'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8': name = 'TT'
      #if dataset == 'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8': name = 'TT'
      #if dataset == 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8': name = 'TT'
      #if dataset == 'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8': name = 'TT'
      #if dataset == 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8': name = 'DY'
      #if dataset == 'DY1JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      #if dataset == 'DY1JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      #if dataset == 'DY1JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      #if dataset == 'DY1JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      #if dataset == 'DY2JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      #if dataset == 'DY2JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      #if dataset == 'DY2JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      #if dataset == 'DY2JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'    
      #if dataset == 'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8': name = 'WW'
      #if dataset == 'WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8': name = 'WW' 
      #if dataset == 'ZZTo2L2Nu_13TeV_powheg_pythia8': name = 'ZZ'
      #if dataset == 'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8': name = 'WZ'
      #if dataset == 'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8': name = 'VVV'
      #if dataset == 'WZZ_TuneCP5_13TeV-amcatnlo-pythia8': name = 'VVV'
      #if dataset == 'WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8': name = 'VVV'
      #if dataset == 'ZZTo4L_13TeV_powheg_pythia8': name = 'ZZ'
      hists[i] = TH1F(name, name,_nBins, _xLow, _xHi)
      chain.Project(name, _variable, "puWeight * weight * " + _cuts)
      #chain.Project(name, 'Z_mass', "puWeight * lumiWeight * (lep_category==2 && Z_pt>60 && met_pt>40 && ngood_jets<2 && ngood_bjets==0)")
      hists[i].SetName(name)
      chain.Reset()
      chain.Delete()
      hists[i].Scale(41.5)
      #scale_factor = dictionary['Scale']
      #hFillColor = dictionary['FillColor']
      #hLineColor = dictionary['LineColor']
      hists[i].Scale(dictionary['Scale'])
      #hFillColor = ROOT.TColor(dictionary['FillColor'])
      #hLineColor = ROOT.TColor(dictionary['LineColor'])
      #hists[i].SetFillColor(hFillColor)
      #hists[i].SetLineColor(hLineColor)
      hists[i].SetFillColor(dictionary['FillColor'])
      hists[i].SetLineColor(dictionary['LineColor'])
      #if dataset == 'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8': 
      #          hists[i].Scale(1.0/1000.0)
      #          hists[i].Scale(1.0000362066412656)
      #  	hists[i].SetFillColor(880+1)
      #if dataset == 'GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8': 
      #          hists[i].Scale(1.0/1000.0)
      #          hists[i].Scale(1.0000377165908536)
      #  	hists[i].SetFillColor(880+1)
      #if dataset == 'GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8': 
      #          hists[i].Scale(1.0/1000.0)
      #          hists[i].Scale(1.0000360831761363)
      #  	hists[i].SetFillColor(880+1)
      #if dataset == 'GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8': 
      #          hists[i].Scale(1.0/1000.0)
      #          hists[i].Scale(1.000036739050646)
      #  	hists[i].SetFillColor(880+1)
      #if dataset == 'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8': 
      #          hists[i].Scale(1.0/1000.0)
      #          hists[i].Scale(1.0000344760838633)
      #  	hists[i].SetFillColor(880+1)
      #if dataset == 'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8': 
      #          hists[i].Scale(1.0/1000.0)
      #          hists[i].Scale(1.0000344984862481)
      #  	hists[i].SetFillColor(880+1)
      #if dataset == 'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8': 
      #          hists[i].Scale(1.0/1000.0)
      #          hists[i].Scale(1.000033746620705)
      #  	hists[i].SetFillColor(880+1)
      #if dataset == 'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8': 
      #          hists[i].Scale(1.0/1000.0)
      #          hists[i].Scale(1.0000342868480752)
      #  	hists[i].SetFillColor(880+1)

#####################################
      #if dataset == 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8': 
      #          hists[i].Scale(0.013873208098316917)
      #  	hists[i].SetFillColor(920+1)
      #     	hists[i].SetLineColor(920+1)
      #if dataset == 'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8': 
      #          hists[i].Scale(1.9579072463512601)
      #  	hists[i].SetFillColor(920+1)
      #          hists[i].SetLineColor(920+1)
      #if dataset == 'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8': 
      #          hists[i].Scale(4.114175980028324)
      #  	hists[i].SetFillColor(920+1)
      #          hists[i].SetLineColor(920+1)
      #if dataset == 'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8': 
      #          hists[i].Scale(2.9187223944620277)
      #  	hists[i].SetFillColor(920+1)
      #          hists[i].SetLineColor(920+1)
      #if dataset == 'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8': 
      #          hists[i].Scale(1.4479458997439978)
      #  	hists[i].SetFillColor(920+1)
      #          hists[i].SetLineColor(920+1)
      #if dataset == 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8': 
      #          hists[i].Scale(0.028592390600870286)
      #  	hists[i].SetFillColor(920+1)
      #          hists[i].SetLineColor(920+1)
      #if dataset == 'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8': 
      #          hists[i].Scale(0.028646991701397357)
      #  	hists[i].SetFillColor(920+1)
      #          hists[i].SetLineColor(920+1)
      #if dataset == 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8': 
      #          hists[i].Scale(0.013873208098316917)
      #  	hists[i].SetFillColor(920+1)
      #          hists[i].SetLineColor(920+1)
      #if dataset == 'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8':
      #   #hists[i].Scale(687.1/66761812)
      #   #hists[i].Scale(87.3/66761.812)
      #          hists[i].Scale(0.013873005409467596)
      #   	hists[i].SetFillColor(920+1)
      #if dataset == 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8':
      #   	#hists[i].Scale(41.5*6529000/207497932)
      #          hists[i].Scale(0.00005603985310)
      #          hists[i].Scale(5.0/6.0)
      #   	hists[i].SetFillColor(900+1)
      #if dataset == 'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8': 
      #          hists[i].Scale(0.09026903803982789)
      #  	hists[i].SetFillColor(840+2)
      #if dataset == 'WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8': 
      #          hists[i].Scale(0.11620249895326198)
      #  	hists[i].SetFillColor(840+2)
      #if dataset == 'ZZTo2L2Nu_13TeV_powheg_pythia8': 
      #          hists[i].Scale(1.6642683283450472)
      #  	hists[i].SetFillColor(800-2)
      #if dataset == 'ZZTo4L_13TeV_powheg_pythia8': 
      #          hists[i].Scale(0.7548052739055428)
      #  	hists[i].SetFillColor(800-2)
      #if dataset == 'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8': 
      #  	#hists[i].Scale(1.109)
      #          hists[i].Scale(0.11620249895326198)
      #          hists[i].Scale(0.85)
      #  	hists[i].SetFillColor(860-4)
      #if dataset == 'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8': 
      #  	hists[i].Scale(67.8391334859334)
      #  	hists[i].SetFillColor(900-5)
      #if dataset == 'WZZ_TuneCP5_13TeV-amcatnlo-pythia8': 
      #          hists[i].Scale(17.926871172229877)
      #  	hists[i].SetFillColor(900-5)
      #if dataset == 'WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8': 
      #          hists[i].Scale(1.0000342868480752)
      #  	hists[i].SetFillColor(900-5)
      #if dataset == 'DY1JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8': 
      #  hists[i].SetFillColor(900+1)
      #  hists[i].SetLineColor(900+1)
      #  #hists[i].Scale(1.0/1.2)
      #  hists[i].Scale(0.00019966935814257948)
      #if dataset == 'DY1JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8': 
      #  hists[i].SetFillColor(900+1)
      #  hists[i].SetLineColor(900+1)
      #  #hists[i].Scale(1.0/1.2)
      #  hists[i].Scale(0.016779882370808786)
      #if dataset == 'DY1JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8': 
      #  hists[i].SetFillColor(900+1)
      #  hists[i].SetLineColor(900+1)
      #  #hists[i].Scale(1.0/1.2)
      #  hists[i].Scale(0.13838894560722576)
      #if dataset == 'DY1JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8': 
      #  hists[i].SetFillColor(900+1)
      #  hists[i].SetLineColor(900+1)
      #  #hists[i].Scale(1.0//1.2)
      #  hists[i].Scale(1.1417575373019058)
      #if dataset == 'DY2JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8': 
      #  hists[i].SetFillColor(900+1)
      #  hists[i].SetLineColor(900+1)
      #  #hists[i].Scale(1.0//1.2)
      #  hists[i].Scale(0.0003776394424266632)
      #if dataset == 'DY2JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8': 
      #  hists[i].SetFillColor(900+1)
      #  hists[i].SetLineColor(900+1)
      #  #hists[i].Scale(1.0//1.2)
      #  hists[i].Scale(0.014432142715805535)
      #if dataset == 'DY2JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8': 
      #  hists[i].SetFillColor(900+1)
      #  hists[i].SetLineColor(900+1)
      #  #hists[i].Scale(1.0//1.2)
      #  hists[i].Scale(0.11950809213291834)
      #if dataset == 'DY2JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8': 
      #  hists[i].SetFillColor(900+1)
      #  hists[i].SetLineColor(900+1)
      #  #hists[i].Scale(1.0//1.2)
      #  hists[i].Scale(1.0074427610853405)
      stk.Add(hists[i])
      mc.Add(hists[i])

   Other.SetFillColor(880+1)
   TT.SetFillColor(920+1)
   WW.SetFillColor(840+2)
   ZZ.SetFillColor(800-2)
   WZ.SetFillColor(860-4)
   DY.SetFillColor(900+1)
   VVV.SetFillColor(900-5)

   leg  = TLegend(.7,.7,.9,.9, "", "fNDC")
   leg.AddEntry(Other, "Other","F")
   leg.AddEntry(ZZ,"ZZ","F")
   leg.AddEntry(WZ, "WZ","F")
   leg.AddEntry(WW,"WW","F")
   leg.AddEntry(TT,"TT","F")
   leg.AddEntry(VVV,"VVV","F")
   leg.AddEntry(DY,"DY","F")


   dathists = [None] * _nPDs
   dat = TH1F('data', 'data',_nBins, _xLow, _xHi)
   for j in range(_nPDs):
      pd = _PDs[j]
      chain = TChain("Events")
      for file in _dict_yml_ctgry[pd]['files']:
         chain.Add(file)
      chain.SetProof()
      hist_name = pd.split('_')[0]
      dathists[j] = TH1F('data', 'data',_nBins, _xLow, _xHi)
      if pd == 'SingleElectron':
	HLT_Cuts = ''
      if pd == 'SingleMuon':
	HLT_Cuts = ' HLT_Ele35_WPTight_Gsf==0 && HLT_Ele38_WPTight_Gsf==0 && HLT_Ele40_WPTight_Gsf==0 &&'
      if pd == 'DoubleEG':
        HLT_Cuts = ' HLT_Ele35_WPTight_Gsf==0 && HLT_Ele38_WPTight_Gsf==0 && HLT_Ele40_WPTight_Gsf==0 && HLT_IsoMu27==0 &&'
      if pd == 'DoubleMuon':
        HLT_Cuts = ' HLT_Ele35_WPTight_Gsf==0 && HLT_Ele38_WPTight_Gsf==0 && HLT_Ele40_WPTight_Gsf==0 && HLT_IsoMu27==0 && HLT_DoubleEle33_CaloIdL_MW==0 && HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL==0 &&'
      if pd == 'MuonEG':
        HLT_Cuts = ' HLT_Ele35_WPTight_Gsf==0 && HLT_Ele38_WPTight_Gsf==0 && HLT_Ele40_WPTight_Gsf==0 && HLT_IsoMu27==0 && HLT_DoubleEle33_CaloIdL_MW==0 && HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL==0 && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8==0 && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8==0 &&'
        #HLT_Cuts = '&& HLT_Ele35_WPTight_Gsf==false && HLT_IsoMu27==false && HLT_DoubleEle33_CaloIdL_MW==false && HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL==false && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8==false && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8==false'
      #chain.Project('data', _variable, _cuts + HLT_Cuts)
      chain.Project('data', _variable, HLT_Cuts + _cuts)
      #chain.Project('data', 'Z_mass', "(lep_category==2  && Z_pt>60 && met_pt>40 && ngood_jets<2 && ngood_bjets==0)")
      dathists[j].SetName(hist_name)
      chain.Reset()
      chain.Delete()
      dat.Add(dathists[j])   
   
   cOutput = TCanvas("cOutput", "cOutput", 600, 800)
   cOutput.SetFillStyle(4000)
   gStyle.SetOptStat(0)
   p1 = TPad("p1", "p1", 0, 0.25, 1, 1)
   p1.SetLogy()
   p1.SetBottomMargin(0)  # joins upper and lower plot
   p1.Draw()
   p1.cd()

   stk.SetMinimum(1.0)
   #stk.SetMaximum(520)
   stk.SetTitle(_variable +" ; Z_{p_{T}} [GeV];Events / Bin")
   stk.Draw("hist")
   dat.SetMarkerStyle(20)
   dat.SetMarkerColor(kBlack)
   dat.SetMarkerSize(0.5)
   dat.Draw("Esame")
   #leg  = TLegend(.7,.7,.9,.9, "", "fNDC")
   #leg.AddEntry(ZZ,"ZZ","F")
   #leg.AddEntry(WZ, "WZ","F")
   #leg.AddEntry(WW,"WW","F")
   #leg.AddEntry(TT,"TT","F")
   #leg.AddEntry(VVV,"VVV","F")
   #leg.AddEntry(DY,"DY","F")
   leg.Draw("same")
   pad = cOutput.cd()
   l = pad.GetLeftMargin()
   t = pad.GetTopMargin()
   r = pad.GetRightMargin()
   b = pad.GetBottomMargin()
   lab1 = TLatex()
   lab1.SetTextSize(0.03)
   lab1.SetTextAlign(11)
   lab1.SetTextFont(42)
   cmsTag = '#bf{CMS} Work in Progress'
   lab1.DrawLatexNDC(l+0.01, 1-t+0.029, cmsTag)
   lab2 = TLatex()
   lab2.SetTextSize(0.03)
   lab2.SetTextAlign(11)
   lab2.SetTextFont(42)
   cmsTag = 'll ch., 41.5 fb^{-1} (13 TeV)'
   lab1.DrawLatexNDC(l+0.5, 1-t+0.029, cmsTag)

   cOutput.cd()
   p2 = TPad("p2", "p2", 0, 0.05, 1, 0.25)
   p2.SetTopMargin(0)  # joins upper and lower plot
   p2.SetBottomMargin(0.2)
   p2.SetGridx()
   p2.Draw()
   p2.cd()

   #Ratio Parameters
   mc.Divide(dat)
   mc.SetTitle("")
   mc.SetMaximum(2.0)
   mc.SetMinimum(0.0)
   mc.SetStats(0)
   mc.SetMarkerColor(kBlue)
   mc.SetMarkerStyle(20)

   #Adjust y-axis settings
   y = mc.GetYaxis()
   y.SetTitle("#frac{#Sigma MC}{Data}")
   y.SetNdivisions(505)
   y.SetTitleSize(15)
   y.SetTitleFont(43)
   y.SetTitleOffset(1.75)
   y.SetLabelFont(43)
   y.SetLabelSize(15)
 
   # Adjust x-axis settings
   x = mc.GetXaxis()
   x.SetTitle(_variable)
   x.SetTitleSize(15)
   x.SetTitleFont(43)
   x.SetTitleOffset(4.2)
   x.SetLabelFont(43)
   x.SetLabelSize(15)

   #Add a line at 1 for the ratio plot
   ll = TLine(_xLow, 1., _xHi, 1.)
   ll.SetLineWidth(2)
   ll.SetLineStyle(7)
   ll.SetLineColor(kBlack)
   
   mc.Draw("P")
   ll.Draw("same")

   cOutput.SaveAs(_variable + ".pdf")

   dat.Delete()
   stk.Delete()
   mc.Delete()
   prf.Close()
   prf.Delete()
   return ()

def ratioplot():

   for var in range( _nVars):
	test(_variable[var],_nBins[var],_xLow[var],_xHi[var])

if __name__ == "__main__":
   ratioplot()
