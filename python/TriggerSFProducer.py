import ROOT
import os
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class TriggerSFProducer(Module):
    def __init__(self, era, name="TriggerSFWeight", norm=True, verbose=False, doSysVar=True):
        self.era = str(era)
        self.targetfile = "%s/src/PhysicsTools/MonoZ/data/TriggerSFs/histo_triggerEff_sel0_%s.root" % (os.environ['CMSSW_BASE'], self.era)
        self.name = name
        self.norm = norm
        self.verbose = verbose
        self.doSysVar = doSysVar

        self.hist_trgSFMMBB = self.loadHisto(self.targetfile,"trgSFMMBB")
        self.hist_trgSFMMEB = self.loadHisto(self.targetfile,"trgSFMMEB")
        self.hist_trgSFMMBE = self.loadHisto(self.targetfile,"trgSFMMBE")
        self.hist_trgSFMMEE = self.loadHisto(self.targetfile,"trgSFMMEE")
        self.hist_trgSFEEBB = self.loadHisto(self.targetfile,"trgSFEEBB")
        self.hist_trgSFEEEB = self.loadHisto(self.targetfile,"trgSFEEEB")
        self.hist_trgSFEEBE = self.loadHisto(self.targetfile,"trgSFEEBE")
        self.hist_trgSFEEEE = self.loadHisto(self.targetfile,"trgSFEEEE")
        self.hist_trgSFMEBB = self.loadHisto(self.targetfile,"trgSFMEBB")
        self.hist_trgSFMEEB = self.loadHisto(self.targetfile,"trgSFMEEB")
        self.hist_trgSFMEBE = self.loadHisto(self.targetfile,"trgSFMEBE")
        self.hist_trgSFMEEE = self.loadHisto(self.targetfile,"trgSFMEEE")
        self.hist_trgSFEMBB = self.loadHisto(self.targetfile,"trgSFEMBB")
        self.hist_trgSFEMEB = self.loadHisto(self.targetfile,"trgSFEMEB")
        self.hist_trgSFEMBE = self.loadHisto(self.targetfile,"trgSFEMBE")
        self.hist_trgSFEMEE = self.loadHisto(self.targetfile,"trgSFEMEE")


    def loadHisto(self,filename,hname):
        tf = ROOT.TFile.Open(filename)
        hist = tf.Get(hname)
        hist.SetDirectory(None)
        tf.Close()
        return hist
    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.name, "F")
        self.out.branch(self.name+"Up", "F")
        self.out.branch(self.name+"Down", "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        lep_cat = 0
        if hasattr(event,"lep_category"):
            lep_cat = int(getattr(event,"lep_category"))
        if lep_cat < 1 :
            l1_pt = 0
            l1_eta = 0
            l2_pt = 0
            l2_eta = 0
            l1_flavor = 0
        else:
            l1_pt = float(getattr(event,"leading_lep_pt"))
            l1_eta = abs(float(getattr(event,"leading_lep_eta")))
            l2_pt = float(getattr(event,"trailing_lep_pt"))
            l2_eta = abs(float(getattr(event,"trailing_lep_eta")))
            l1_flavor = int(getattr(event,"leading_lep_flavor"))
        weight = 1
        weightError = 0
        if lep_cat==3 or lep_cat==5 or lep_cat==7 : #these are MM. MML and MMLL lepton categories
            if l1_eta <= 1.5 and l2_eta <= 1.5:
                hist = self.hist_trgSFMMBB
            elif l1_eta >= 1.5 and l2_eta <= 1.5:
                hist = self.hist_trgSFMMEB
            elif l1_eta <= 1.5 and l2_eta >= 1.5:
                hist = self.hist_trgSFMMBE
            elif l1_eta >= 1.5 and l2_eta >= 1.5:
                hist = self.hist_trgSFMMEE
        elif lep_cat==1 or lep_cat==4 or lep_cat==6 : #these are EE. EEL and EELL lepton categories
            if l1_eta <= 1.5 and l2_eta <= 1.5:
                hist = self.hist_trgSFEEBB
            elif l1_eta >= 1.5 and l2_eta <= 1.5:
                hist = self.hist_trgSFEEEB
            elif l1_eta <= 1.5 and l2_eta >= 1.5:
                hist = self.hist_trgSFEEBE
            elif l1_eta >= 1.5 and l2_eta >= 1.5:
                hist = self.hist_trgSFEEEE
        else : #This is the EM and ME categories
            if l1_flavor == 1: #This is the muon leading
                if l1_eta <= 1.5 and l2_eta <= 1.5:
                    hist = self.hist_trgSFMEBB
                elif l1_eta >= 1.5 and l2_eta <= 1.5:
                    hist = self.hist_trgSFMEEB
                elif l1_eta <= 1.5 and l2_eta >= 1.5:
                    hist = self.hist_trgSFMEBE
                elif l1_eta >= 1.5 and l2_eta >= 1.5:
                    hist = self.hist_trgSFMEEE
            elif l1_flavor == 0: #This is the electron leading
                if l1_eta <= 1.5 and l2_eta <= 1.5:
                    hist = self.hist_trgSFEMBB
                elif l1_eta >= 1.5 and l2_eta <= 1.5:
                    hist = self.hist_trgSFEMEB
                elif l1_eta <= 1.5 and l2_eta >= 1.5:
                    hist = self.hist_trgSFEMBE
                elif l1_eta >= 1.5 and l2_eta >= 1.5:
                    hist = self.hist_trgSFEMEE
        nxBins = 7
        nyBins = 7
        searchbinx = -1
        searchbiny = -1
        for xbin in range(1,nxBins+1):
            if l1_pt > hist.GetXaxis().GetBinLowEdge(nxBins) + hist.GetXaxis().GetBinWidth(nxBins):
                searchbinx = 7
                break
            if l1_pt > hist.GetXaxis().GetBinLowEdge(xbin) and l1_pt < hist.GetXaxis().GetBinLowEdge(xbin) + hist.GetXaxis().GetBinWidth(xbin) :
                searchbinx = xbin
        for ybin in range(1,nyBins+1):
            if l2_pt > hist.GetYaxis().GetBinLowEdge(nyBins) + hist.GetYaxis().GetBinWidth(nyBins):
                searchbiny = 7
                break
            if l2_pt > hist.GetYaxis().GetBinLowEdge(ybin) and l2_pt < hist.GetYaxis().GetBinLowEdge(ybin) + hist.GetYaxis().GetBinWidth(ybin) :
                searchbiny = ybin

        weight = hist.GetBinContent(searchbinx,searchbiny)
        self.out.fillBranch(self.name, weight)
        if self.doSysVar:
            weightError = hist.GetBinErrorUp(searchbinx,searchbiny)
            self.out.fillBranch(self.name+"Up", weight+weightError)
            weightError = hist.GetBinErrorLow(searchbinx,searchbiny)
            self.out.fillBranch(self.name+"Down", weight-weightError)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
TriggerSF_2016 = lambda : TriggerSFProducer(era="2016", verbose=False, doSysVar=True)
TriggerSF_2017 = lambda : TriggerSFProducer(era="2017", verbose=False, doSysVar=True)
TriggerSF_2018 = lambda : TriggerSFProducer(era="2018", verbose=False, doSysVar=True)

