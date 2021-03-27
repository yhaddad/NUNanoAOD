# VBS
import ROOT
import sys, os
import numpy as np
import math
from importlib import import_module
import itertools
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import PhysicsTools.NanoAODTools.postprocessing.tools as tk

ROOT.PyConfig.IgnoreCommandLineOptions = True


class VBSProducer(Module):
    def __init__(self, isMC, era, do_syst=False, syst_var=None):
        self.isMC = isMC
        self.era = era
        self.do_syst = do_syst
        self.syst_var = syst_var
        self.zmass = 91.1873
        if self.syst_var !='':
          self.syst_suffix = '_sys_' + self.syst_var if self.do_syst else ''
        else:
          self.syst_suffix = syst_var

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        self.out.branch("dijet_abs_dEta{}".format(self.syst_suffix), "F")
        self.out.branch("dijet_Mjj{}".format(self.syst_suffix), "F")
        self.out.branch("dijet_Zep{}".format(self.syst_suffix), "F")
        self.out.branch("dijet_centrality{}".format(self.syst_suffix), "F")
        self.out.branch("S_T_hard{}".format(self.syst_suffix), "F")
        self.out.branch("S_T_jets{}".format(self.syst_suffix), "F")
        self.out.branch("S_T_all{}".format(self.syst_suffix), "F")

        self.out.branch("HT_F{}".format(self.syst_suffix), "F")
        self.out.branch("Jet_pt_Ratio{}".format(self.syst_suffix), "F")
        self.out.branch("R_pt{}".format(self.syst_suffix), "F")
        self.out.branch("Jet_etas_multiplied{}".format(self.syst_suffix), "F")    
        self.out.branch("dPT_OZ{}".format(self.syst_suffix), "F")


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        # skip useless events
        lep_category = getattr(event, "lep_category")
        if lep_category <= 0:
            return False

        # Get variables from event tree
        met_pt = getattr(event, "met_pt{}".format(self.syst_suffix))
        met_phi = getattr(event, "met_phi{}".format(self.syst_suffix))
        met_p4 = ROOT.TLorentzVector()
        met_p4.SetPtEtaPhiM(met_pt, 0., met_phi, 0.)

        lead_lep_pt = getattr(event, "lead_lep_pt{}".format(self.syst_suffix))
        trail_lep_pt = getattr(event, "trail_lep_pt{}".format(self.syst_suffix))

        Z_pt = getattr(event, "Z_pt{}".format(self.syst_suffix))
        Z_eta = getattr(event, "Z_eta{}".format(self.syst_suffix))
        Z_phi = getattr(event, "Z_phi{}".format(self.syst_suffix))
        Z_mass = getattr(event, "Z_mass{}".format(self.syst_suffix))
        Z_p4 = ROOT.TLorentzVector()
        Z_p4.SetPtEtaPhiM(Z_pt, Z_eta, Z_phi, Z_mass)

        # jets
        ngood_jets = getattr(event, "ngood_jets{}".format(self.syst_suffix))

        lead_jet_pt = getattr(event, "lead_jet_pt{}".format(self.syst_suffix))
        lead_jet_eta = getattr(event, "lead_jet_eta{}".format(self.syst_suffix))
        lead_jet_phi = getattr(event, "lead_jet_phi{}".format(self.syst_suffix))
        lead_jet_p4 = ROOT.TLorentzVector()
        lead_jet_p4.SetPtEtaPhiM(Z_pt, Z_eta, Z_phi, Z_mass)

        trail_jet_pt = getattr(event, "trail_jet_pt{}".format(self.syst_suffix))
        trail_jet_eta = getattr(event, "trail_jet_eta{}".format(self.syst_suffix))
        trail_jet_phi = getattr(event, "trail_jet_phi{}".format(self.syst_suffix))
        trail_jet_p4 = ROOT.TLorentzVector()
        trail_jet_p4.SetPtEtaPhiM(Z_pt, Z_eta, Z_phi, Z_mass)

        third_jet_pt = getattr(event, "third_jet_pt{}".format(self.syst_suffix))
        third_jet_eta = getattr(event, "third_jet_eta{}".format(self.syst_suffix))
        third_jet_phi = getattr(event, "third_jet_phi{}".format(self.syst_suffix))
        third_jet_p4 = ROOT.TLorentzVector()
        third_jet_p4.SetPtEtaPhiM(Z_pt, Z_eta, Z_phi, Z_mass)

        # more variables
        H_T = getattr(event, "H_T{}".format(self.syst_suffix))
        HT_F = (lead_jet_pt + trail_jet_pt) / H_T if H_T > 0. else 0.
        Jet_etas_multiplied = lead_jet_eta * trail_jet_eta

        # more variables
        if ngood_jets >= 2:
            S_T_jets = (lead_jet_p4+trail_jet_p4).Pt() / (lead_jet_pt+trail_jet_pt)
            S_T_hard = (lead_jet_p4+trail_jet_p4+Z_p4).Pt() / (lead_jet_pt+trail_jet_pt+Z_pt)
            S_T_all = (lead_jet_p4+trail_jet_p4+Z_p4+met_p4).Pt() / (lead_jet_pt+trail_jet_pt+Z_pt+met_pt)
            Jet_pt_Ratio = trail_jet_pt / lead_jet_pt
            R_pt = lead_lep_pt * trail_lep_pt / (lead_jet_pt * trail_jet_pt)
            dijet_abs_dEta = abs(lead_jet_eta-trail_jet_eta)
            dijet_Mjj = (lead_jet_p4 + trail_jet_p4).M()
            dijet_Zep = Z_eta - 0.5 * (lead_jet_eta + trail_jet_eta)
            dijet_centrality = np.exp(-4 * (dijet_Zep / dijet_abs_dEta)**2) if dijet_abs_dEta>0 else -99.
        else:
            S_T_jets = -99.
            S_T_hard = -99.
            S_T_all = -99.
            Jet_pt_Ratio = -99.
            R_pt = -99.
            dijet_abs_dEta = -99.
            dijet_Mjj = -99.
            dijet_Zep = -99.
            dijet_centrality = -99.

        # more variables
        dPT_OZ = (lead_jet_pt + trail_jet_pt) / Z_pt if Z_pt > 0. else -99.

        self.out.fillBranch("dijet_abs_dEta{}".format(self.syst_suffix), dijet_abs_dEta)
        self.out.fillBranch("dijet_Mjj{}".format(self.syst_suffix), dijet_Mjj)
        self.out.fillBranch("dijet_Zep{}".format(self.syst_suffix), dijet_Zep)
        self.out.fillBranch("dijet_centrality{}".format(self.syst_suffix), dijet_centrality)
        self.out.fillBranch("S_T_hard{}".format(self.syst_suffix), S_T_hard)
        self.out.fillBranch("S_T_jets{}".format(self.syst_suffix), S_T_jets)
        self.out.fillBranch("S_T_all{}".format(self.syst_suffix), S_T_all)

        self.out.fillBranch("HT_F{}".format(self.syst_suffix), HT_F)
        self.out.fillBranch("Jet_pt_Ratio{}".format(self.syst_suffix), Jet_pt_Ratio)
        self.out.fillBranch("R_pt{}".format(self.syst_suffix), R_pt)
        self.out.fillBranch("Jet_etas_multiplied{}".format(self.syst_suffix), Jet_etas_multiplied)
        self.out.fillBranch("dPT_OZ{}".format(self.syst_suffix), dPT_OZ)


        return True

