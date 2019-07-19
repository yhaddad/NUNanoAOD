#import yaml
#from MonoZNanoAOD.plotter.oyaml import oyaml as yaml
import oyaml as yaml
#from ruamel.yaml import YAML
import uproot
from ROOT import *
import ROOT
import sys
import numpy as np
import array as ar
#from collections import OrderedDict
#from array import array

gROOT.SetBatch(1)

import argparse

parser = argparse.ArgumentParser("")
parser.add_argument('-era'    , '--era'    , type=str, default="2018", help="")
parser.add_argument('-doSyst' , '--doSyst' , type=int, default=1     , help="")

options  = parser.parse_args()

lumi = {
        "2016" : 35.9,
        "2017" : 41.5,
        "2018" : 60.0
}
xsections = {}
dataset_info = {}
if options.era == "2018":
	with open('LionKing2018_ROOTfiles.yml', 'r') as f_yml:
    		_dict_yml = yaml.load(f_yml)
	with open("xsections_{}.yaml".format(2018), 'r') as stream:
    		xsections = yaml.safe_load(stream)
        with open("datasets_{}.yaml".format(2018), 'r') as dset:
                dataset_info = yaml.load(dset)
elif options.era == "2017":
        with open('LionKing2017_ROOTfiles.yml', 'r') as f_yml:
                _dict_yml = yaml.load(f_yml)
        with open("xsections_{}.yaml".format(2017), 'r') as stream:
                xsections = yaml.safe_load(stream)
        with open("datasets_{}.yaml".format(2017), 'r') as dset:
                dataset_info = yaml.safe_load(dset)
elif options.era == "2016":
        with open('LionKing2016_ROOTfiles.yml', 'r') as f_yml:
                _dict_yml = yaml.load(f_yml)
        with open("xsections_{}.yaml".format(2016), 'r') as stream:
                xsections = yaml.safe_load(stream)
        with open("datasets_{}.yaml".format(2016), 'r') as dset:
                dataset_info = yaml.safe_load(dset)
else:
	print "no valid era selected. Please run python era_plotter.py --era=201X"
Var_Dict = [
        #{'variable':'delta_phi_ZMet',        	'nBins':32,             'xLow':-3.2,            'xHi':3.2,	'title':'#Delta #phi(Z,p_{T}^{miss})'},
        #{'variable':'Z_mass',        		'nBins':30,             'xLow':0,               'xHi':300,	'title':'M_{ll} [GeV]'},
        #{'variable':'sca_balance',   		'nBins':10,             'xLow':0,               'xHi':5,	'title':'|p_{T}^{miss}|/|p_{T}^{ll}|'},
        #{'variable':'emulatedMET',         	'nBins':10,             'xLow':0,               'xHi':600,	'title':'Emulated p_{T}^{miss} [GeV]'},
        #{'variable':'Z_pt',         		'nBins':15,             'xLow':0,		'xHi':500,	'title':'p_{T}^{ll} [GeV]'},
        #{'variable':'ngood_jets',              'nBins':15,             'xLow':0,               'xHi':15,	'title':'# jets'},
        #{'variable':'PV_npvs',                 'nBins':100,            'xLow':0,               'xHi':100,	'title':'# vtx'}
        #{'variable':'delta_R_ll',               'nBins':15,             'xLow':0,               'xHi':5,	'title':'#Delta R_{ll}'}
        #{'variable':'delta_phi_j_met',               'nBins':32,             'xLow':-3.2,               'xHi':3.2,        'title':'#Delta#phi(Jet,p_{T}^{miss})'},
        #{'variable':'met_phi',               'nBins':32,             'xLow':-3.2,               'xHi':3.2,        'title':'p_{T}^{miss} #phi'}
        #{'variable':'met_pt',                  'nBins':10,             'xLow':50,               'xHi':100,	'title':'p_{T}^{miss} [GeV]'}
        {'variable':'met_pt',              'nBins':10,             'xAxis':ar.array('d', [50,55,60,65,70,75,80,85,90,95,100]),     'title':'p_{T}^{miss} [GeV]'},
	#{'variable':'emulatedMET',              'nBins':11,             'xAxis':ar.array('d', [50,100,125,150,175,200,250,300,350,400,500,600]),     'title':'Emulated p_{T}^{miss} [GeV]'},
        #{'variable':'met_pt',              'nBins':11,             'xAxis':ar.array('d', [50,100,125,150,175,200,250,300,350,400,500,600]),     'title':'p_{T}^{miss} [GeV]'},
	]

_nVars = len(Var_Dict)

#WZ Control Region
#_cuts = "((lep_category==4 || lep_category==5) && Z_pt>60 && Z_mass > 76 && Z_mass < 106 && ngood_jets < 2 && ngood_bjets == 0 && met_pt > 30 && mass_alllep > 100 && abs(sca_balance) < 1.5 && abs(MET_phi - Z_phi) > 2.6)"
#ZZ Control Region
_cuts = "((lep_category==6 || lep_category==7) && Z_pt>60 && Z_mass > 61 && Z_mass < 121 && ngood_jets < 2 && abs(MET_phi - Z_phi) > 2.6)"
#NRB Control Region
#_cuts = "((lep_category==2) && Z_pt>60 && Z_mass > 76 && Z_mass < 106 && ngood_jets < 2 && ngood_bjets == 0 && met_pt > 30 )"
#DY Control Region
_cuts = "((lep_category==3 || lep_category==1) && Z_mass > 76 && Z_mass < 106 && Z_pt>60 && ngood_jets < 2 && ngood_bjets == 0 && met_pt<100 && met_pt > 50 && abs(MET_phi - Z_phi) > 2.6 && nhad_taus == 0 && abs(sca_balance) < 1.5 && abs(delta_phi_j_met) > 0.5 && delta_R_ll < 1.8)"
#_cuts = "((lep_category==3 || lep_category==1) && Z_mass > 76 && Z_mass < 106 && Z_pt>60 && ngood_jets < 2 && ngood_bjets == 0 && met_pt<100 && met_pt > 50 && abs(delta_phi_ZMet) > 2.6 && delta_R_ll < 1.8 && abs(delta_phi_j_met) > 0.5 && sca_balance > 0.5 && sca_balance < 1.5 && nhad_taus == 0 )"
#_cuts = "((lep_category==1 || lep_category==3))"# && Z_mass > 76 && Z_mass < 106 && Z_pt>60)"# && ngood_jets < 2 && ngood_bjets == 0)"# && met_pt > 100 && Flag_METFilters == 1)"# && abs(delta_met_rec) < 1)"
#_cuts = "((lep_category==6 || lep_category==7) && Z_pt>60 && Z_mass > 61 && Z_mass < 121 && ngood_jets < 2 && abs(emulatedMET_phi-Z_phi) > 2.5 && emulatedMET > 100)"
#_cuts = "((lep_category==4 || lep_category==5) && ngood_bjets == 0 && Z_pt>60 && Z_mass > 76 && Z_mass < 106 && met_pt > 30 && emulatedMET > 100 && mass_alllep > 100 && ngood_jets < 2 && emulatedMET/Z_pt > 0.6 && emulatedMET/Z_pt < 1.4 && abs(emulatedMET_phi-Z_phi) > 2.8 )"#&& delta_R_ll < 1.8)"#
#_cuts = "((lep_category==2) && Z_mass > 76 && Z_mass < 106 && Z_pt>60 && ngood_jets < 2 && ngood_bjets == 0 && met_pt > 50)"

#_cuts = "((lep_category==2) && Z_pt>60 && ngood_jets < 2 && ngood_bjets == 0 && met_pt > 50)"
#_cuts = "((lep_category==2) && Z_mass > 76 && Z_mass < 106 && Z_pt>60 && ngood_jets > 3 && ngood_bjets > 0 && met_pt > 50)"
#_cuts = "((lep_category==1 || lep_category==3) && Z_mass > 76 && Z_mass < 106 && Z_pt>60 && ngood_jets < 2 && ngood_bjets == 0 && met_pt<50)"
#_cuts = "((lep_category==1 || lep_category==3) && Z_mass > 76 && Z_mass < 106 && Z_pt>60 && ngood_jets < 2 && ngood_bjets == 0 && abs(delta_phi_ZMet) < 1)"
#_cuts = "((lep_category==4 || lep_category==5) && ngood_bjets == 0 && Z_pt>60 && Z_mass > 76 && Z_mass < 106 && met_pt > 30 && emulatedMET > 100 && mass_alllep > 100 && ngood_jets < 2 && emulatedMET/Z_pt > 0.6 && emulatedMET/Z_pt < 1.4 && abs(emulatedMET_phi-Z_phi) > 2.8)"# && delta_R_ll < 1.8)"#
#_cuts = "((lep_category==3 || lep_category==1) && Z_mass > 50 &&  Z_pt>60 && met_pt > 40 )"
#_cuts = "((lep_category==2) && ngood_jets < 2 && ngood_bjets == 0 && Z_pt>60 && met_pt > 40)"
def test(_variable,_nBins,_xAxis,title):
   prf = TProof.Open("lite://")
   hists = [None] * len(dataset_info)
   stk = ROOT.THStack("stk", ";;Events / Bin ")
   mc = TH1F('h', 'h', _nBins, _xAxis)
   i = 0
   dathists = [None] * 40
   dat = TH1F('data', 'data',_nBins, _xAxis)
   dat2 = TH1F('data', 'data',_nBins, _xAxis)
   for dataset, thing in dataset_info.items():
      name = dataset_info[dataset]["name"]
      chain = TChain("Events") 
      if (name != "data") and (name != "signal"):
	      Nevt = 0
 	      neg_fac = 0.0
	      for file in _dict_yml[dataset]['files']:
	        chain.Add(file)
		file_in = uproot.open(file)
		Nevt += file_in["Runs"].array("genEventCount").sum()
	      	original_xsec = abs(file_in["Events"].array("xsecscale")[0])
	        neg_fac += np.mean(file_in["Events"].array("xsecscale")/original_xsec)*file_in["Runs"].array("genEventCount").sum()
	      if Nevt == 0 : continue
	      scale = lumi[options.era]/float(Nevt)
	      neg_fac /= float(Nevt)
	      xsec  = xsections[dataset]["xsec"]
	      xsec *= xsections[dataset]["kr"]
	      xsec *= xsections[dataset]["br"]
	      xsec *= 1000.0
	      scale *= xsec/original_xsec
	      scale /= (1+neg_fac)/2.0
	      chain.SetProof()
	      hists[i] = TH1F(name, name,_nBins, _xAxis)
	      if dataset == "WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8" or dataset == "WZTo3LNu_TuneCP5_13TeV-powheg-pythia8" or dataset == "ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8" or dataset == "ZZTo4L_TuneCP5_13TeV_powheg_pythia8" or dataset == "WZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8":
	      	chain.Project(name, _variable, "xsecscale * btagEventWeight * puWeight * kEW * kNNLO * w_muon_SF * w_electron_SF * nvtxWeight * TriggerSFWeight * " + _cuts)
	      else:
              	chain.Project(name, _variable, "xsecscale * btagEventWeight * puWeight * w_muon_SF * w_electron_SF * nvtxWeight * TriggerSFWeight * " + _cuts)
              #chain.Project(name, _variable, "xsecscale * puWeight * w_muon_SF * w_electron_SF * nvtxWeight * TriggerSFWeight * " + _cuts)
	      hists[i].SetName(name)
	      chain.Reset()
	      chain.Delete()
	      hists[i].Scale(scale)
	      print "========================================================"
	      print "       ++  dataset :", dataset
	      print "       + old xsec [fb] = ", original_xsec
	      print "       + new xec [fb]  = ", xsec
	      print "       + nevents       = ", Nevt
	      print "       + scale         = ", scale
              print "       + neg factor    = ", (1+neg_fac)/2.0
	      print "       + yield in hist = ", hists[i].Integral()*scale
	      print "========================================================"
	      hists[i].SetFillColor(dataset_info[dataset]["Color"])
	      hists[i].SetLineColor(dataset_info[dataset]["Color"])
	      stk.Add(hists[i])
	      mc.Add(hists[i])
	      i += 1
      if name == "data":
      	chain = TChain("Events")
      	for file in _dict_yml[dataset]['files']:
      	   chain.Add(file)
      	chain.SetProof()
      	hists[i] = TH1F('data', 'data',_nBins, _xAxis)
      	chain.Project('data', _variable, _cuts)
      	hists[i].SetName("data")
      	chain.Reset()
      	chain.Delete()
      	dat.Add(hists[i])   
      	i += 1
      if name == "signal":
        chain = TChain("Events")
        for file in _dict_yml[dataset]['files']:
           chain.Add(file)
        chain.SetProof()
        hists[i] = TH1F('signal', 'signal',_nBins, _xAxis)
        chain.Project('signal', _variable, _cuts)
        hists[i].SetName("signal")
        chain.Reset()
        chain.Delete()
        i += 1
   ZZ.SetFillColor(800-2)
   WZ.SetFillColor(860-4)
   WW.SetFillColor(840+2)
   TT.SetFillColor(920+1)
   VVV.SetFillColor(900-5)
   DY.SetFillColor(900+1)
   leg  = TLegend(.7,.7,.9,.9, "", "fNDC")
   #leg.AddEntry(Other, "Other","F")
   leg.AddEntry(ZZ,"ZZ","F")
   leg.AddEntry(WZ, "WZ","F")
   leg.AddEntry(WW,"WW","F")
   leg.AddEntry(TT,"TT","F")
   leg.AddEntry(VVV,"VVV","F")
   leg.AddEntry(DY,"DY","F")

   integ = mc.Integral(0,31)
   print " MC : "
   print " sumW    : ", integ
   integ2 = dat.Integral(0,31)
   print " data : "
   print " sumW    : ", integ2  
   cOutput = TCanvas("cOutput", "cOutput", 800, 800)
   cOutput.SetFillStyle(4000)
   gStyle.SetOptStat(0)
   p1 = TPad("p1", "p1", 0, 0.25, 1, 1)
   p1.SetLogy()
   p1.SetBottomMargin(0)  # joins upper and lower plot
   p1.Draw()
   p1.cd()

   stk.SetMinimum(1.0)
   stk.SetMaximum(10000)
   stk.SetTitle(" ;"+ title + ";Events / Bin")
   stk.Draw("hist")
   dat.SetMarkerStyle(20)
   dat.SetMarkerColor(kBlack)
   dat.SetMarkerSize(0.5)
   dat.Draw("Esame")
   #hists[i-1].Draw("Esame")
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
   cmsTag = '#bf{CMS}'
   lab1.DrawLatexNDC(l+0.01, 1-t+0.029, cmsTag)
   lab2 = TLatex()
   lab2.SetTextSize(0.03)
   lab2.SetTextAlign(11)
   lab2.SetTextFont(42)
   cmsTag = 'll ch., 60.0 fb^{-1} (13 TeV)'
   lab1.DrawLatexNDC(l+0.5, 1-t+0.029, cmsTag)

   cOutput.cd()
   p2 = TPad("p2", "p2", 0, 0.05, 1, 0.25)
   p2.SetTopMargin(0)  # joins upper and lower plot
   p2.SetBottomMargin(0.2)
   p2.SetGridx()
   p2.Draw()
   p2.cd()

   #Ratio Parameters
   dat2 = dat.Clone()
   dat2.Divide(mc)
   dat2.SetTitle("")
   dat2.SetMaximum(2.00)
   dat2.SetMinimum(0.00)
   dat2.SetStats(0)
   dat2.SetMarkerColor(kBlack)
   dat2.SetMarkerStyle(20)

   #Adjust y-axis settings
   y = dat2.GetYaxis()
   y.SetTitle("Data/#Sigma MC")
   y.SetNdivisions(505)
   y.SetTitleSize(15)
   y.SetTitleFont(43)
   y.SetTitleOffset(1.75)
   y.SetLabelFont(43)
   y.SetLabelSize(15)
 
   # Adjust x-axis settings
   x = dat2.GetXaxis()
   x.SetTitle(title)
   x.SetTitleSize(15)
   x.SetTitleFont(43)
   x.SetTitleOffset(4.2)
   x.SetLabelFont(43)
   x.SetLabelSize(15)

   #Add a line at 1 for the ratio plot
   ll = TLine(_xAxis[0], 1., _xAxis[_nBins], 1.)
   ll.SetLineWidth(2)
   ll.SetLineStyle(7)
   ll.SetLineColor(kBlack)
   
   dat2.Draw("P")
   ll.Draw("same")

   cOutput.SaveAs("plots/" + _variable + "_2018_redone.png")

   dat.Delete()
   dat2.Delete()
   stk.Delete()
   mc.Delete()
   prf.Close()
   prf.Delete()
   return ()


def ratioplot():

   for var in range( _nVars):
        var_dictionary = Var_Dict[var]
        #test(var_dictionary['variable'],var_dictionary['nBins'],var_dictionary['xLow'],var_dictionary['xHi'],var_dictionary['title'])
        test(var_dictionary['variable'],var_dictionary['nBins'],var_dictionary['xAxis'],var_dictionary['title'])
if __name__ == "__main__":
   ratioplot()
