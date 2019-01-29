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
	#{'dataset':'GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8',				'name':'Other',			'Scale':1.0000362066412656*1.0/1000.0, 		'FillColor': 880+1, 		'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8',                   	'name':'Other',                 'Scale':1.0000377165908536*1.0/1000.0,          'FillColor': 880+1,             'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8',                   	'name':'Other',                 'Scale':1.0000360831761363*1.0/1000.0,          'FillColor': 880+1,             'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo2mu2nu_13TeV_MCFM701_pythia8',                   	'name':'Other',                 'Scale':1.000036739050646*1.0/1000.0,           'FillColor': 880+1,             'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8',                   	'name':'Other',                 'Scale':1.0000344760838633*1.0/1000.0,          'FillColor': 880+1,             'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8',                   		'name':'Other',                 'Scale':1.0000344984862481*1.0/1000.0,          'FillColor': 880+1,             'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8',                   		'name':'Other',                 'Scale':1.000033746620705*1.0/1000.0,           'FillColor': 880+1,             'LineColor':880+1 },
        {'dataset':'GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8',                   		'name':'Other',                 'Scale':1.0000342868480752*1.0/1000.0,          'FillColor': 880+1,             'LineColor':1 },
        {'dataset':'ZZTo2L2Nu_13TeV_powheg_pythia8',                   				'name':'ZZ',                    'Scale':1.6642683283450472,                     'FillColor': 800-2,             'LineColor':800-2 },
        {'dataset':'WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8',                   		'name':'WZ',                    'Scale':0.11620249895326198*0.85,               'FillColor': 860-4,             'LineColor':1 },
        {'dataset':'WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8',                   		'name':'WW',                    'Scale':0.09026903803982789,                    'FillColor': 840+2,             'LineColor':1 },
        #{'dataset':'WWTo2L2Nu_NNPDF31_TuneCP5_PSweights_13TeV-powheg-pythia8',                 'name':'WW',                    'Scale':0.11620249895326198,                    'FillColor': 840+2,             'LineColor':1 },
        {'dataset':'ZZZ_TuneCP5_13TeV-amcatnlo-pythia8',                   			'name':'VVV',                   'Scale':67.8391334859334,                      	'FillColor': 900-5,             'LineColor':900-5 },
        {'dataset':'WZZ_TuneCP5_13TeV-amcatnlo-pythia8',                   			'name':'VVV',                   'Scale':17.926871172229877,                     'FillColor': 900-5,             'LineColor':1 },
        #{'dataset':'WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8',                   			'name':'VVV',                   'Scale':1.0000342868480752,                     'FillColor': 900-5,             'LineColor':900-5 },
        #{'dataset':'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8',                   		'name':'TT',                    'Scale':0.013873208098316917,                   'FillColor': 920+1,             'LineColor':920+1 },
        {'dataset':'TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8',                   			'name':'TT',                    'Scale':1.9579072463512601,                     'FillColor': 920+1,             'LineColor':920+1 },
        {'dataset':'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',                  		'name':'TT',                    'Scale':4.114175980028324,                      'FillColor': 920+1,             'LineColor':920+1 },
        {'dataset':'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',                   'name':'TT',                    'Scale':2.9187223944620277,                     'FillColor': 920+1,             'LineColor':920+1 },
        {'dataset':'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',                    'name':'TT',                    'Scale':1.4479458997439978,                     'FillColor': 920+1,             'LineColor':920+1 },
        {'dataset':'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',             'name':'TT',                    'Scale':0.028592390600870286,                   'FillColor': 920+1,             'LineColor':920+1 },
        {'dataset':'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',                 'name':'TT',                    'Scale':0.028646991701397357,                   'FillColor': 920+1,             'LineColor':920+1 },
        {'dataset':'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',                  	'name':'TT',                    'Scale':0.013873005409467596,                   'FillColor': 920+1,             'LineColor':1 },
        {'dataset':'DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8',                   	'name':'DY',                    'Scale':0.00005603985310/0.6,               'FillColor': 900+1,             'LineColor':900+1 },
        #{'dataset':'DY1JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8',           'name':'DY',                    'Scale':0.00019966935814257948/1.2,                 'FillColor': 900+1,             'LineColor':900+1 },
        #{'dataset':'DY1JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',          'name':'DY',                    'Scale':0.016779882370808786/1.2,                   'FillColor': 900+1,             'LineColor':900+1 },
        #{'dataset':'DY1JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',          'name':'DY',                    'Scale':0.13838894560722576/1.2,                    'FillColor': 900+1,             'LineColor':900+1 },
        #{'dataset':'DY1JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',          'name':'DY',                    'Scale':1.1417575373019058/1.2,                     'FillColor': 900+1,             'LineColor':900+1 },
        #{'dataset':'DY2JetsToLL_M-50_LHEZpT_50-150_TuneCP5_13TeV-amcnloFXFX-pythia8',           'name':'DY',                    'Scale':0.0003776394424266632/1.2,                  'FillColor': 900+1,             'LineColor':900+1 },
        #{'dataset':'DY2JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8',          'name':'DY',                    'Scale':0.014432142715805535/1.2,                   'FillColor': 900+1,             'LineColor':900+1 },
        #{'dataset':'DY2JetsToLL_M-50_LHEZpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8',          'name':'DY',                    'Scale':0.11950809213291834/1.2,                    'FillColor': 900+1,             'LineColor':900+1 },
        #{'dataset':'DY2JetsToLL_M-50_LHEZpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8',          'name':'DY',                    'Scale':1.0074427610853405/1.2,                     'FillColor': 900+1,             'LineColor':1 },
        #{'dataset':'ZZTo4L_13TeV_powheg_pythia8',                   				'name':'ZZ',                    'Scale':0.7548052739055428,                     'FillColor': 800-2,             'LineColor':1 }
	]

_ndatasets = len(Dict)

_PDs = [# for now since we remove the HLTs here we need this to be in this specific order. Look to change this soon with skimmed trees by HLTs
   'SingleElectron',
   'SingleMuon',
   'DoubleMuon',
   'DoubleEG',
   'MuonEG']

_nPDs = len(_PDs)

Var_Dict = [
        #{'variable':'delta_phi_ZMet',        	'nBins':32,             'xLow':-3.2,            'xHi':3.2},
        #{'variable':'Z_mass',        		'nBins':10,             'xLow':0,               'xHi':300},
        #{'variable':'sca_balance',   		'nBins':10,             'xLow':0,               'xHi':5},
        #{'variable':'emulatedMET',         	'nBins':15,             'xLow':0,               'xHi':300},
        {'variable':'Z_pt',         		'nBins':15,             'xLow':0,		'xHi':300}
        #{'variable':'PV_npvs',                     'nBins':100,             'xLow':0,               'xHi':100}
	]

_nVars = len(Var_Dict)

#_cuts = "((lep_category==3 || lep_category==1) && Z_mass > 76 && Z_mass < 106 && Z_pt>60 && ngood_jets < 2 && ngood_bjets == 0 && met_pt<50 && met_pt > 0)"# && abs(delta_phi_ZMet) > 2.8 && met_pt>100 && delta_R_ll < 1.8 && abs(delta_phi_j_met) > 0.5 )"#&& vec_balance > 0.4 && vec_balance < 1.6 )"
_cuts = "((lep_category==1) && Z_mass > 76 && Z_mass < 106 && Z_pt>60 && ngood_jets < 2 && ngood_bjets == 0 && met_pt > 40)"
def test(_variable,_nBins,_xLow,_xHi):
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
      hists[i] = TH1F(name, name,_nBins, _xLow, _xHi)
      chain.Project(name, _variable, "puWeight * weight * " + _cuts)
      #chain.Project(name, 'Z_mass', "puWeight * lumiWeight * (lep_category==2 && Z_pt>60 && met_pt>40 && ngood_jets<2 && ngood_bjets==0)")
      hists[i].SetName(name)
      chain.Reset()
      chain.Delete()
      hists[i].Scale(41.5)
      hists[i].Scale(dictionary['Scale'])
      hists[i].SetFillColor(dictionary['FillColor'])
      hists[i].SetLineColor(dictionary['LineColor'])
      stk.Add(hists[i])
      mc.Add(hists[i])

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
      chain.Project('data', _variable, _cuts)
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
        var_dictionary = Var_Dict[var]
        test(var_dictionary['variable'],var_dictionary['nBins'],var_dictionary['xLow'],var_dictionary['xHi'])
if __name__ == "__main__":
   ratioplot()
