import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetSysColl import JetSysColl, JetSysObj

class JetProducer(Module):
    def __init__(self, jetSelection, systvals):
        self.jetSel = jetSelection
        self.systvals = systvals
        self.systs = [
            'nom',
            'pu_up',  'pu_dn',
            'pdf_up', 'pdf_dn',
            'ps_up',  'ps_dn',
            'jec_up', 'jec_dn',
            'jer_up', 'jer_dn',
            'jms_up', 'jms_dn',
            'jmr_up', 'jmr_dn'
        ]
        
        self.systvals = []
        for isys,sys in enumerate(self.systs):
            setattr( self, sys, isys)
            self.systvals.append( getattr(self,sys) )
            
        self.jets = None
        pass
        
    def beginJob(self):
        pass

    def endJob(self):
        pass
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("yacine_HT",  "F")
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.jets = Collection(event, "Jet")
    
        jets = JetSysColl(self.jets, self.systvals, sel = lambda x : x.pt > 0)
        print " N_jets = ", len(jets.jets_raw()),  " jets : ", len(self.jets)
	print " --------------------------------------- "
        for ijet, jet in enumerate(jets.jets_raw()):
           	# if ijet not in jets[self.nom].keys():
        	print "    jets[",ijet, "] : pt_nom : ", jet.pt_nom,  " : pt_jerUp : ", jet.pt_jerUp
        #print "             : ", dir(self)
        #print "             : ", self.systvals
        print "             : ", self.systs
        var_HT = ROOT.TLorentzVector()
        
        #for j in filter(self.jetSel,jets):
        #    var_HT += j.p4()
        #

        self.out.fillBranch("yacine_HT", var_HT.Pt())
        return True
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
exampleJetProducer = lambda : JetProducer(jetSelection= lambda j : j.pt > 0)
