import ROOT
import sys
import numpy as np
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import PhysicsTools.NanoAODTools.postprocessing.tools as tk

ROOT.PyConfig.IgnoreCommandLineOptions = True


class MonoZProducer(Module):
    def __init__(self, isMC, era, do_syst=False, syst_var=None):
        self.isMC = isMC
        self.era = era
        self.do_syst = do_syst
        self.syst_var = syst_var
        self.syst_suffix = '_sys_' + self.syst_var if self.do_syst else ''

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("met_pt{}".format(self.syst_suffix), "F")
        self.out.branch("met_phi{}".format(self.syst_suffix), "F")
        self.out.branch("ngood_leptons{}".format(self.syst_suffix), "I")
        self.out.branch("nmore_leptons{}".format(self.syst_suffix), "I")
        self.out.branch("lep_category{}".format(self.syst_suffix), "I")

        self.out.branch("Z_pt{}".format(self.syst_suffix), "F")
        self.out.branch("Z_eta{}".format(self.syst_suffix), "F")
        self.out.branch("Z_phi{}".format(self.syst_suffix), "F")
        self.out.branch("Z_mass{}".format(self.syst_suffix), "F")
        self.out.branch("Z_mt{}".format(self.syst_suffix), "F")

        self.out.branch("delta_phi_ZMet{}".format(self.syst_suffix), "F")
        self.out.branch("Balance{}".format(self.syst_suffix), "F")
        self.out.branch("delta_phi_ll{}".format(self.syst_suffix), "F")
        self.out.branch("delta_eta_ll{}".format(self.syst_suffix), "F")
        self.out.branch("delta_R_ll{}".format(self.syst_suffix), "F")

        self.out.branch("ngood_jets{}".format(self.syst_suffix), "I")
        self.out.branch("ngood_bjets{}".format(self.syst_suffix), "I")
        self.out.branch("lead_jet_pt{}".format(self.syst_suffix), "F")
        self.out.branch("lead_bjet_pt{}".format(self.syst_suffix), "F")
        self.out.branch("delta_phi_j_met{}".format(self.syst_suffix), "F")

        self.out.branch("nhad_taus{}".format(self.syst_suffix), "I")
        self.out.branch("lead_tau_pt{}".format(self.syst_suffix), "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    # def met(self, met, isMC):
    # """
    # The MC has JER smearing applied which has output
    # branch met_[pt/phi]_nom this should be compared
    # with data branch MET_[pt/phi]. This essentially
    # aliases the two branches to one common variable.
    # """
    # if isMC:
    # return (met.pt_nom, met.phi_nom)
    # else:
    # return (met.pt, met.phi)

    def electron_id(self, electron, wp):
        if (self.era == "2016" and wp == "80"):
            return electron.mvaSpring16GP_WP80
        elif (self.era == "2016" and wp == "90"):
            return electron.mvaSpring16GP_WP90
        elif (self.era == "2017" and wp == "80"):
            return electron.mvaFall17Iso_WP80
        elif (self.era == "2017" and wp == "90"):
            return electron.mvaFall17Iso_WP90

    def corrected_pt(self):
        pass

    def analyze(self, event):
        """
        process event, return True (go to next module)
        or False (fail, go to next event)
        """
        electrons = list(Collection(event, "Electron"))
        muons = list(Collection(event, "Muon"))
        jets = list(Collection(event, "Jet"))
        taus = list(Collection(event, "Tau"))
        met = Object(event, "MET")

        # met_pt, met_phi = self.met(met, self.isMC)
        self.out.fillBranch("met_pt{}".format(self.syst_suffix), met.pt)
        self.out.fillBranch("met_phi{}".format(self.syst_suffix), met.phi)

        # count electrons and muons
        good_leptons = []
        good_muons = []
        good_electrons = []
        lep_category = -1
        for mu in muons:
            isoLep = mu.pfRelIso04_all
            pass_ips = abs(mu.dxy) < 0.02 and abs(mu.dz) < 0.1
            pass_fid = abs(mu.eta) < 2.4
            pass_ids = mu.tightId and isoLep <= 0.15
            if pass_fid and pass_ids and pass_ips:
                good_muons.append(mu)

        for el in electrons:
            id_CB = el.cutBased
            if el.pt >= 20 and abs(el.eta) <= 2.5 and id_CB >= 3:
                good_electrons.append(el)

        # let sort the muons in pt
        good_muons.sort(key=lambda x: x.pt, reverse=True)
        good_electrons.sort(key=lambda x: x.pt, reverse=True)

        z_candidate = []
        lep_category = 0
        if len(good_muons) >= 2:
            if good_muons[0].pt > 20:
                for i in range(1, len(good_muons)):
                    if good_muons[0].charge * good_muons[i].charge < 0:
                        lep_category = 1
                        z_candidate = [good_muons[0], good_muons[i]]
                        break

        elif len(good_electrons) >= 2:
            if good_electrons[0].pt > 20:
                for i in range(1, len(good_electrons)):
                    if good_electrons[0].charge * good_electrons[i].charge < 0:
                        lep_category = 2
                        z_candidate = [good_electrons[0], good_electrons[i]]
                        break
        if len(good_electrons) == 1 and len(good_muons) == 1:
            if good_electrons[0].pt < 20 or good_muons[0].pt < 20:
                z_candidate = [good_electrons[0], good_muons[0]]
                if good_electrons[0].charge * good_muons[0].charge < 0:
                    lep_catgeory = 3
                else:
                    lep_catgeory = 4
        ngood_leptons = len(good_leptons)
        good_leptons = good_electrons + good_muons

        self.out.fillBranch("ngood_leptons{}".format(self.syst_suffix), ngood_leptons)
        self.out.fillBranch("lep_category{}".format(self.syst_suffix), lep_category)
        Z_4vec = ROOT.TLorentzVector()
        if lep_category > 0:
            for lep in z_candidate:
                lep_4vec = ROOT.TLorentzVector()
                lep_4vec.SetPtEtaPhiM(lep.pt, lep.eta, lep.phi, lep.mass)
                Z_4vec = Z_4vec + lep_4vec

            self.out.fillBranch("Z_pt{}".format(self.syst_suffix), Z_4vec.Pt())
            self.out.fillBranch("Z_eta{}".format(self.syst_suffix), Z_4vec.Eta())
            self.out.fillBranch("Z_phi{}".format(self.syst_suffix), Z_4vec.Phi())
            self.out.fillBranch("Z_mass{}".format(self.syst_suffix), Z_4vec.M())
            self.out.fillBranch("Z_mt{}".format(self.syst_suffix), Z_4vec.Mt())
            _delta_zphi = tk.deltaPhi(z_candidate[0].phi, z_candidate[1].phi)
            _delta_zdR = tk.deltaR(z_candidate[0].eta, z_candidate[0].phi,
                                   z_candidate[1].eta, z_candidate[1].phi,)
            _delta_zeta = abs(z_candidate[0].eta - z_candidate[1].eta)
            _delta_phi_zmet = tk.deltaPhi(Z_4vec.Phi(), met.phi)
            _delta_balance = abs(met.pt - Z_4vec.Pt())/Z_4vec.Pt() if Z_4vec.Pt() != 0 else -1
            self.out.fillBranch("delta_phi_ll{}".format(self.syst_suffix), _delta_zphi)
            self.out.fillBranch("delta_eta_ll{}".format(self.syst_suffix), _delta_zeta)
            self.out.fillBranch("delta_R_ll{}".format(self.syst_suffix), _delta_zdR)
            self.out.fillBranch("delta_phi_ZMet{}".format(self.syst_suffix), _delta_phi_zmet)
            self.out.fillBranch("Balance{}".format(self.syst_suffix), _delta_balance)
        # process jet
        good_jets = []
        good_bjets = []
        for jet in jets:
            if jet.pt < 30.0 or abs(jet.eta) > 4.7:
                continue
            if not jet.jetId:
                continue
            good_jets.append(jet)
            if abs(jet.eta) <= 2.4 and jet.btagCSVV2 > 0.8484:
                good_bjets.append(jet)

        good_jets.sort(key=lambda jet: jet.pt, reverse=True)
        good_bjets.sort(key=lambda jet: jet.pt, reverse=True)

        _dphi_j_met = tk.deltaPhi(good_jets[0], met.phi) if len(good_jets) else -99.0
        _lead_jet_pt = good_jets[0].pt if len(good_jets) else 0.0
        _lead_bjet_pt = good_bjets[0].pt if len(good_bjets) else 0.0

        self.out.fillBranch("ngood_jets{}".format(self.syst_suffix), len(good_jets))
        self.out.fillBranch("ngood_bjets{}".format(self.syst_suffix), len(good_bjets))
        self.out.fillBranch("lead_jet_pt{}".format(self.syst_suffix), _lead_jet_pt)
        self.out.fillBranch("lead_bjet_pt{}".format(self.syst_suffix), _lead_bjet_pt)
        self.out.fillBranch("delta_phi_j_met{}".format(self.syst_suffix), _dphi_j_met)

        # process taus
        had_taus = []
        for tau in taus:
            if tk.closest(tau, good_leptons)[1] < 0.4:
                continue
            # only hadronic tau decay
            if tau.decayMode() != 5:
                continue
            if tau.pt > 18 and abs(tau.eta) <= 2.3:
                had_taus.append(tau)
        self.out.fillBranch("nhad_taus{}".format(self.syst_suffix), len(had_taus))
        self.out.fillBranch("lead_tau_pt{}".format(self.syst_suffix), had_taus[0].pt if len(had_taus) else 0)

        return True

MonoZ_2016_mc = lambda: MonoZProducer(True, "2016")
MonoZ_2017_mc = lambda: MonoZProducer(True, "2017")
MonoZ_2016_data = lambda: MonoZProducer(False, "2016")
MonoZ_2017_data = lambda: MonoZProducer(False, "2017")
