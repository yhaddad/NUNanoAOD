import yaml
from ROOT import *
import ROOT
import sys
from array import array

gROOT.SetBatch(1)

with open('ROOTfiles.yml', 'r') as f_yml:
    _dict_yml = yaml.load(f_yml)

with open('ROOTfiles_CtgryFltrd.yml', 'r') as f2_yml:
    _dict_yml_ctgry = yaml.load(f2_yml)

_datasets = [
   #'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8',
   #'GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8',
   #'GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8',
   #'GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8',
   #'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8',
   #'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8',
   #'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8',
   #'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8',
   'ZZTo2L2Nu_13TeV_powheg_pythia8',
   'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8',
   #'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8',
   'WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8',
   ##'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8',
   ##'WZZ_TuneCP5_13TeV-amcatnlo-pythia8',
   #'WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8',
   ##'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',
   #'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8',
   #'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8',
   #'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',
   #'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',
   #'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',
   #'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',
   #'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',
   ##'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',
   #'DY1JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8',
   #'DY1JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',
   #'DY1JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',
   #'DY1JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',
   #'DY2JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8',
   #'DY2JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',
   #'DY2JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',
   #'DY2JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',
   #'ZZTo4L_13TeV_powheg_pythia8']
   ]

_ndatasets = len(_datasets)

_PDs = [
   #'MuonEG',
   #'SingleElectron',
   #'SingleMuon',
   #'DoubleMuon',
   'DoubleEG']

_nPDs = len(_PDs)

_nBins = [
   #8,
   30,
   #14,
   #23,
   32,
   20]

_xLow = [
   #0,
   #0,
   #0,
   #0,
   #0,
   70]

_xHi = [
   #8,
   #300,
   #14,
   #260,
   #3.2,
   110]

_variable = [
   #"ngood_leptons",
   #"Z_pt",
   #"ngood_jets",
   #"emulatedMET",
   #"delta_phi_ZMet",
   #"Z_mass"
   "met_pt"]
   #"vec_balance"]
   

_nVars = len(_variable)


_Stuff = [100,125,150,175,200,250,300,350,400,500,600]
#_Stuff = [0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0]
#_cuts = "(lep_category==7 && Z_mass > 81 && Z_mass < 101  && Z_pt>60 && met_pt>40 && ngood_bjets==0 && delta_phi_ZMet > 2)"
#_cuts = "((lep_category==1 || lep_category==3) && Z_mass > 81 && Z_mass < 101  && Z_pt>60 && met_pt>40 && ngood_jets < 2 && ngood_bjets == 0)"   
#_cuts = "((lep_category==1 || lep_category==3) && Z_mass > 76 && Z_mass < 106 && Z_pt>60 && ngood_jets < 2 && ngood_bjets == 0 && delta_phi_ZMet > 2.8 && met_pt>100 && delta_R_ll < 1.8 && delta_phi_j_met > 0.5)" #&& vec_balance < 0.4)"# && delta_R_ll < 1.8 && delta_phi_j_met > 0.5)"
_cuts = "((lep_category==1) && Z_mass > 76 && Z_mass < 106 && Z_pt>60 && ngood_jets < 2 && ngood_bjets == 0 && abs(delta_phi_ZMet) > 2.8 && met_pt>100 && delta_R_ll < 1.8 && abs(delta_phi_j_met) > 0.5 && vec_balance > 0.4 && nhad_taus==0)"
def test(_variable):
   prf = TProof.Open("lite://")
   hists = [None] * _ndatasets
   stk = ROOT.THStack("stk", ";;Events / Bin ")
   mc = TH1F('h', 'h',10,array('d',_Stuff))
   for i in range(_ndatasets):
      dataset = _datasets[i]
      chain = TChain("Events") 
      for file in _dict_yml[dataset]['files']:
         chain.Add(file)
      chain.SetProof()
      if dataset == 'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8': name = 'Other'
      if dataset == 'GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8': name = 'Other'
      if dataset == 'GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8': name = 'Other'
      if dataset == 'GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8': name = 'Other'
      if dataset == 'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8': name = 'Other'
      if dataset == 'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8': name = 'Other'
      if dataset == 'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8': name = 'Other'
      if dataset == 'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8': name = 'Other'
      if dataset == 'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8': name = 'TT'
      if dataset == 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8': name = 'TT'
      if dataset == 'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8': name = 'TT'
      if dataset == 'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8': name = 'TT'
      if dataset == 'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8': name = 'TT'
      if dataset == 'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8': name = 'TT'
      if dataset == 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8': name = 'TT'
      if dataset == 'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8': name = 'TT'
      if dataset == 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8': name = 'DY'
      if dataset == 'DY1JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      if dataset == 'DY1JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      if dataset == 'DY1JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      if dataset == 'DY1JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      if dataset == 'DY2JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      if dataset == 'DY2JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      if dataset == 'DY2JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'
      if dataset == 'DY2JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8': name = 'DY'    
      if dataset == 'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8': name = 'WW'
      if dataset == 'WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8': name = 'WW' 
      if dataset == 'ZZTo2L2Nu_13TeV_powheg_pythia8': name = 'ZZ'
      if dataset == 'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8': name = 'WZ'
      if dataset == 'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8': name = 'VVV'
      if dataset == 'WZZ_TuneCP5_13TeV-amcatnlo-pythia8': name = 'VVV'
      if dataset == 'WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8': name = 'VVV'
      if dataset == 'ZZTo4L_13TeV_powheg_pythia8': name = 'ZZ'
      hists[i] = TH1F(name, name,10,array('d',_Stuff))
      #print chain.GetEntries(_cuts)
      chain.Project(name, _variable, "abs(weight) * " + _cuts)
      #chain.Project(name, 'Z_mass', "puWeight * lumiWeight * (lep_category==2 && Z_pt>60 && met_pt>40 && ngood_jets<2 && ngood_bjets==0)")
      hists[i].SetName(name)
      chain.Reset()
      chain.Delete()
      hists[i].Scale(41.5)
      if dataset == 'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8': 
                hists[i].Scale(1.0/1000.0)
		hists[i].SetFillColor(kViolet+1)
      if dataset == 'GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8': 
                hists[i].Scale(1.0/1000.0)
		hists[i].SetFillColor(kViolet+1)
      if dataset == 'GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8': 
                hists[i].Scale(1.0/1000.0)
		hists[i].SetFillColor(kViolet+1)
      if dataset == 'GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8': 
                hists[i].Scale(1.0/1000.0)
		hists[i].SetFillColor(kViolet+1)
      if dataset == 'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8': 
                hists[i].Scale(1.0/1000.0)
		hists[i].SetFillColor(kViolet+1)
      if dataset == 'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8': 
                hists[i].Scale(1.0/1000.0)
		hists[i].SetFillColor(kViolet+1)
      if dataset == 'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8': 
                hists[i].Scale(1.0/1000.0)
		hists[i].SetFillColor(kViolet+1)
      if dataset == 'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8': 
                hists[i].Scale(1.0/1000.0)
		hists[i].SetFillColor(kViolet+1)
      if dataset == 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8': hists[i].SetFillColor(kGray+1)
      if dataset == 'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8': hists[i].SetFillColor(kGray+1)
      if dataset == 'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8': hists[i].SetFillColor(kGray+1)
      if dataset == 'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8': hists[i].SetFillColor(kGray+1)
      if dataset == 'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8': hists[i].SetFillColor(kGray+1)
      if dataset == 'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8': hists[i].SetFillColor(kGray+1)
      if dataset == 'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8': hists[i].SetFillColor(kGray+1)
      if dataset == 'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8': hists[i].SetFillColor(kGray+1)
      if dataset == 'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8':
         #hists[i].Scale(687.1/66761812)
         #hists[i].Scale(87.3/66761.812)
         hists[i].SetFillColor(kGray+1)
      if dataset == 'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8':
         #hists[i].Scale(41.5*6529000/207497932)
         hists[i].SetFillColor(kPink+1)
      if dataset == 'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8': hists[i].SetFillColor(kTeal+2)
      if dataset == 'WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8': 
		hists[i].SetFillColor(kTeal+2)
                hists[i].Scale(0.11620249895326198)
      if dataset == 'ZZTo2L2Nu_13TeV_powheg_pythia8': 
		hists[i].SetFillColor(kOrange-2)
       		hists[i].Scale(1.6642683283450472)
      if dataset == 'ZZTo4L_13TeV_powheg_pythia8': hists[i].SetFillColor(kOrange-2)
      if dataset == 'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8': 
		hists[i].SetFillColor(kAzure-4)
                hists[i].Scale(0.11620249895326198)
      if dataset == 'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8': hists[i].SetFillColor(kPink-5)
      if dataset == 'WZZ_TuneCP5_13TeV-amcatnlo-pythia8': hists[i].SetFillColor(kPink-5)
      if dataset == 'WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8': hists[i].SetFillColor(kPink-5)
      if dataset == 'DY1JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8': 
	hists[i].SetFillColor(kPink+1)
        hists[i].SetLineColor(kPink+1)
	hists[i].Scale(1.23)
      if dataset == 'DY1JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8': 
        hists[i].SetFillColor(kPink+1)
        hists[i].SetLineColor(kPink+1)
        hists[i].Scale(1.23)
      if dataset == 'DY1JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8': 
        hists[i].SetFillColor(kPink+1)
        hists[i].SetLineColor(kPink+1)
        hists[i].Scale(1.23)
      if dataset == 'DY1JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8': 
        hists[i].SetFillColor(kPink+1)
        hists[i].SetLineColor(kPink+1)
        hists[i].Scale(1.23)
      if dataset == 'DY2JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8': 
	hists[i].SetFillColor(kPink+1)
        hists[i].SetLineColor(kPink+1)
        hists[i].Scale(1.23)
      if dataset == 'DY2JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8': 
	hists[i].SetFillColor(kPink+1)
        hists[i].SetLineColor(kPink+1)
        hists[i].Scale(1.23)
      if dataset == 'DY2JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8': 
	hists[i].SetFillColor(kPink+1)
        hists[i].SetLineColor(kPink+1)
        hists[i].Scale(1.23)
      if dataset == 'DY2JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8': 
	hists[i].SetFillColor(kPink+1)
        hists[i].SetLineColor(kPink+1)
        hists[i].Scale(1.23)
      stk.Add(hists[i])
      mc.Add(hists[i])

      integ = hists[i].Integral(0,1000)
      print dataset
      print integ

   #Other.SetFillColor(kOrange-5)
   #TT.SetFillColor(kGray+1)
   WW.SetFillColor(kTeal+2)
   ZZ.SetFillColor(kOrange-2)
   WZ.SetFillColor(kAzure-4)
   #DY.SetFillColor(kPink+1)
   #VVV.SetFillColor(kPink-5)

   leg  = TLegend(.7,.7,.9,.9, "", "fNDC")
   #leg.AddEntry(Other, "Other","F")
   leg.AddEntry(ZZ,"ZZ","F")
   leg.AddEntry(WZ, "WZ","F")
   leg.AddEntry(WW,"WW","F")
   #leg.AddEntry(TT,"TT","F")
   #leg.AddEntry(VVV,"VVV","F")
   #leg.AddEntry(DY,"DY","F")

   dathists = [None] * _nPDs
   dat = TH1F('data', 'data',10,array('d',_Stuff))
   for j in range(_nPDs):
      pd = _PDs[j]
      chain = TChain("Events")
      for file in _dict_yml_ctgry[pd]['files']:
         chain.Add(file)
      chain.SetProof()
      hist_name = pd.split('_')[0]
      dathists[j] = TH1F('data', 'data',10,array('d',_Stuff))
      chain.Project('data', _variable, _cuts +"&& met_pt < 50" )
      #chain.Project('data', 'Z_mass', "(lep_category==2  && Z_pt>60 && met_pt>40 && ngood_jets<2 && ngood_bjets==0)")
      dathists[j].SetName(hist_name)
      chain.Reset()
      chain.Delete()
      dat.Add(dathists[j])   
   
   cOutput = TCanvas("cOutput", "cOutput", 600, 800)
   cOutput.SetFillStyle(4000)
   gStyle.SetOptStat(0)
   p1 = TPad("p1", "p1", 0, 0.25, 1, 1)
   #p1.SetLogy()
   p1.SetBottomMargin(0)  # joins upper and lower plot
   p1.Draw()
   p1.cd()

   stk.SetMinimum(0.1)
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
   cmsTag = 'ee ch., 41.5 fb^{-1} (13 TeV)'
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
   ll = TLine(100., 1., 600., 1.)
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
	test(_variable[var])

if __name__ == "__main__":
   ratioplot()
