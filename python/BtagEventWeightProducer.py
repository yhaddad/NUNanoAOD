import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class BtagEventWeightProducer(Module):
    def __init__(self, targetfile, era, name="btagEventWeight", norm=True, verbose=False, doSysVar=True):
        self.name = name
        self.norm = norm
        self.era = era
        self.verbose = verbose
        self.doSysVar = doSysVar
        # load efficiency hists
        print("b-tagging file:", targetfile)
        self.eff_hist_dict = {5: self.loadHisto(targetfile, "bottom_eff"), 
                              4: self.loadHisto(targetfile, "charm_eff"), 
                              0: self.loadHisto(targetfile, "light_eff")}

    def loadHisto(self, filename, hname):
        tf = ROOT.TFile.Open(filename)
        hist_eff = tf.Get(hname)
        hist_eff.SetDirectory(None)
        tf.Close()
        return hist_eff

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.name, "F")
        self.out.branch(self.name + "Up", "F")
        self.out.branch(self.name + "Down", "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def btag_id(self, wp):
        # using deepjet
        # ref : https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation
        dict_wp = {"2016preVFP": {"loose": 0.0508, "medium": 0.2598, "tight": 0.6502},
                   "2016postVFP": {"loose": 0.0480, "medium": 0.2489, "tight": 0.6377},
                   "2017": {"loose": 0.0532, "medium": 0.3040, "tight": 0.7476},
                   "2018": {"loose": 0.0490, "medium": 0.2783, "tight": 0.7100},}
        return dict_wp[self.era][wp]

    def analyze(self, event):
        # process event, return True (go to next module) or False (fail, go to next event)
        # Weight calclulated on an event-by-event basis assuming a bjet veto following:
        # https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#1a_Event_reweighting_using_scale

        # probability of jet configuration for MC
        prob_MC = 1.0
        prob_MC_up = 1.0
        prob_MC_down = 1.0

        # probability of jet configuration for Data
        prob_Data = 1.0
        prob_Data_up = 1.0
        prob_Data_down = 1.0

        # iterate over all jets
        jets = list(Collection(event, "Jet"))
        for i,j in enumerate(jets):
            # jet info
            j_id = j.jetId
            j_pt = j.pt
            j_eta = j.eta
            j_flav = j.hadronFlavour
            j_deepjet = j.btagDeepFlavB 

            # jet selections. tightLepVeto ID applied, so ignoring dR(l, j) for now
            if (j_id != 6) or (j_pt < 30.0) or (abs(j_eta) > 4.7):
                continue
            b_tagged = (abs(j_eta) <= 2.4) and (j_deepjet > self.btag_id("loose"))

            # choose efficiency histogram
            hist_eff = self.eff_hist_dict[j_flav]
            x_ax = hist_eff.GetXaxis()
            y_ax = hist_eff.GetYaxis()

            # find ith x-bin from pT
            idx_binx = x_ax.FindBin(j_pt)
            idx_binx = max(idx_binx, 1)
            idx_binx = min(idx_binx, x_ax.GetNbins())

            # find ith y-bin from eta
            idx_biny = y_ax.FindBin(j_eta)
            idx_biny = max(idx_biny, 1)
            idx_biny = min(idx_biny, y_ax.GetNbins())

            # get jet efficiency with variations from 2D histograms
            eff = hist_eff.GetBinContent(idx_binx, idx_biny)                
            # eff_err = hist_eff.GetBinError(idx_binx, idx_biny)
            eff_err = np.sqrt(eff * (1.0 - eff) / 5000.)
            eff_up = eff + eff_err
            eff_down = eff - eff_err

            # scale factors provided by NanoAOD-tools
            SF = j.btagSF_deepjet_L
            SF_up = j.btagSF_deepjet_L_up
            SF_down = j.btagSF_deepjet_L_down 

            # update MC probabiliry
            prob_MC *= eff if b_tagged else (1.0 - eff)
            prob_MC_up *= eff_up if b_tagged else (1.0 - eff_up)
            prob_MC_down *= eff_down if b_tagged else (1.0 - eff_down)

            # update Data probabiliry
            prob_Data *= SF * eff if b_tagged else (1.0 - SF * eff)
            prob_Data_up *= SF_up * eff_up if b_tagged else (1.0 - SF_up * eff_up)
            prob_Data_down *= SF_down * eff_down if b_tagged else (1.0 - SF_down * eff_down)

        # MC event weight (i.e. b-tagging scale factor)
        weight = prob_Data / prob_MC
        weight_up = prob_Data_up / prob_MC_up
        weight_down = prob_Data_down / prob_MC_down

        self.out.fillBranch(self.name, weight)
        if self.doSysVar:
            self.out.fillBranch(self.name+"Up", weight_up)
            self.out.fillBranch(self.name+"Down", weight_down)

        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
BtagEff_2016 = "%s/src/PhysicsTools/MonoZ/data/BTagEff/BTagEff_2016.root" % os.environ['CMSSW_BASE']
# BtagEventWeight_2016 = lambda : BtagEventWeightProducer(BtagEff_2016, verbose=False, doSysVar=True)
BtagEventWeight_2016preVFP = lambda : BtagEventWeightProducer(BtagEff_2016, era="2016preVFP", verbose=False, doSysVar=True)
BtagEventWeight_2016postVFP = lambda : BtagEventWeightProducer(BtagEff_2016, era="2016postVFP", verbose=False, doSysVar=True)

BtagEff_2017 = "%s/src/PhysicsTools/MonoZ/data/BTagEff/BTagEff_2017.root" % os.environ['CMSSW_BASE']
BtagEventWeight_2017 = lambda : BtagEventWeightProducer(BtagEff_2017, era="2017", verbose=False, doSysVar=True)

BtagEff_2018 = "%s/src/PhysicsTools/MonoZ/data/BTagEff/BTagEff_2018.root" % os.environ['CMSSW_BASE']
BtagEventWeight_2018 = lambda : BtagEventWeightProducer(BtagEff_2018, era="2018", verbose=False, doSysVar=True)
