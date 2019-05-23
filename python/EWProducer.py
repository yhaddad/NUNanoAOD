import ROOT
import sys
import numpy as np
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

ROOT.PyConfig.IgnoreCommandLineOptions = True


class EWProducer(Module):
    def __init__(self, process, do_syst=False, syst_var=''):
        self.process = process
        if process==1:
            self.table = np.loadtxt('../data/data_ZZ_EwkCorrections.dat')
        elif process==2:
            self.table = np.loadtxt('../data/data_WZ_EwkCorrections.dat')

        self.do_syst = do_syst
        self.syst_var = syst_var
        # No HIST for now
        if self.syst_var !='':
            self.syst_suffix = '_sys_' + syst_var if do_syst else ''
        else:
            self.syst_suffix = syst_var


    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("kEW", "F")
        

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        # EW correction
        gen_part = Collection(event, "GenPart")

        fq1 = abs(gen_part[0].pdgId)
        fq2 = abs(gen_part[1].pdgId)
        print " --------------- "
        for parton in gen_part:
            print " --- parton : ", parton.pdgId, " :pt: ", parton.pt, " :status: ", parton.statusFlags, " :mother: ", parton.genPartIdxMother
        print " --------------- "

        if ( (fq1>=1 and fq1<=6) or fq1==21 ):
            # q1 = ROOT.TLorentzVector( gen_part[0].p4().X(), gen_part[0].p4().Y(), gen_part[0].p4().Z(), gen_part[0].p4().T() )
            q1 = ROOT.TLorentzVector( 0, 0, 100., 100. )
        else:
            raise Exception("monoZ/EWKcorrection, GenParticle element 0 is neither a quark nor a gluon.")

        if ( (fq2>=1 and fq2<=6) or fq2==21 ):
            # q2 = ROOT.TLorentzVector( gen_part[1].p4().X(), gen_part[1].p4().Y(), gen_part[1].p4().Z(), gen_part[1].p4().T() )
            q2 = ROOT.TLorentzVector( 0, 0, -100., 100. )
        else:
            raise Exception("monoZ/EWKcorrection, GenParticle element 1 is neither a quark nor a gluon.")

        if ( gen_part[2].pdgId==23 or abs(gen_part[2].pdgId)==24 ):
            # v1 = ROOT.TLorentzVector( gen_part[2].p4().X(), gen_part[2].p4().Y(), gen_part[2].p4().Z(), gen_part[2].p4().T() )
            v1 = gen_part[2].p4()
        else:
            raise Exception("monoZ/EWKcorrection, GenParticle element 2 is neither a Z nor a W boson.")

        if ( gen_part[3].pdgId==23 or abs(gen_part[3].pdgId)==24 ):
            # v2 = ROOT.TLorentzVector( gen_part[3].p4().X(), gen_part[3].p4().Y(), gen_part[3].p4().Z(), gen_part[3].p4().T() )
            v2 = gen_part[3].p4()
        else:
            raise Exception("monoZ/EWKcorrection, GenParticle element 3 is neither a Z nor a W boson.")


        # Diboson center of mass
        vv = v1 + v2

        # Mandelstam variable s (square of center of mass energy)
        sqrshat = vv.Mag()
        shat = vv.Mag2()

        # Boost to the VV center of mass frame
        q1.Boost( -vv.BoostVector() )
        q2.Boost( -vv.BoostVector() )
        v1.Boost( -vv.BoostVector() )

        # Unitary vectors
        uq1 = q1.Vect() * (1./q1.P())
        uq2 = q2.Vect() * (1./q2.P())
        uv1 = v1.Vect() * (1./v1.P())

        # Effective beam axis
        dq = uq1 - uq2
        # effective beam direction
        udq = dq * (1./dq.Mag()) 
        costheta = udq.Dot(uv1)

        # # Z boson mass, assumed to be on-shell
        # mz = 91.1876
        # # W boson mass, assumed to be on-shell
        # mw = 80.385
        that = 0.

        # if self.process==1: 
        #     that = mz*mz - 0.5*shat + costheta * np.sqrt(0.25*shat*shat - mz*mz*shat)
        # elif self.process==2: 
        #     b = 0.5/sqrshat * np.sqrt((shat - mz*mz - mw*mw)**2 - 4*mw*mw*mz*mz)
        #     a = np.sqrt(b*b + mz*mz)
        #     # Bad calculation! But needed to boost to the WZ c.m. frame (different masses)
        #     that = mz*mz - sqrshat * (a - b*costheta)
        # thad = v1^2 + q1^2 - 2*v1*q1*costheta = v1^2 + 0 - 2*v1.T*q1*T + 2*v1.p*q1.p
        that = v1.Mag2() - 2 * v1.T() * np.sqrt(shat / 4.) + 2 * v1.Vect().Mag() * np.sqrt(0.25*shat) * costheta

        # Select table row, based on s_hat and t_hat
        itab = 40000
        # highest value of sqrt(s_hat) in the table
        sqrshatmax = 0.8E+04 
        if sqrshat>sqrshatmax: 
            itab = 39800
        else:
            for itmp in range(0, 40000, 200):
                if abs(sqrshat - self.table[itmp][0])<sqrshatmax:
                    sqrshatmax = abs(sqrshat - self.table[itmp][0])
                    itab = itmp
                else:
                    break
        sqrshatmax = self.table[itab+199][1]
        # In case sqrshat exceeds sqrshatmax
        # (the table is for 8 TeV, we run at 13 TeV)
        if that>sqrshatmax:
            itab += 199
        else:
            sqrshatmax = 0.1E+09
            for itmp in range(itab, itab+200):
                if abs(that - self.table[itmp][1])<sqrshatmax:
                    sqrshatmax = abs(that - self.table[itmp][1])
                    itab = itmp
                else:
                    break
        # Select table column, based on quark flavor (for ZZ)
        # always for WZ
        jtab = 2
        # ZZ
        if self.process==1:
            # Flavor of incident quark (std::min in case one is a gluon)
            qtype = min(fq1, fq2)
            # d, s
            if (qtype==1 or qtype==3): 
                jtab = 3
            elif (qtype==2 or qtype==4): 
                # u, c
                jtab = 2
            elif qtype==5: 
                # b
                jtab = 4
            else:
                raise Exception("monoZ/EWKcorrection, Unknown quark type.")

        kEW = 1. + self.table[itab][jtab]

        if ( self.syst_var == "EWKUp" or self.syst_var == "EWKDown" ):
            nlept = 0
            sumptl = 0.
            for parton in gen_part:
                if ( parton.statusFlags & 128 ) == 0:
                    continue
                if parton.status != 1:
                    continue
                if ( abs(parton.pdgId) < 11 or abs(parton.pdgId) > 16 ): 
                    continue
                sumptl += parton.pt
                nlept += 1

            if nlept != 4:
                # There are cases like this, namely tau and Z->4lep decays
                # Could handle, but should really make no difference
                # So just go conservative
                sumptl = 1E-9

            rhozz = vv.Pt() / sumptl

            # Average QCD NLO k factors from arXiv:1105.0020
            dkfactor_qcd = 0.
            if process == 1:       
                dkfactor_qcd = 15.99/ 9.89 - 1. # ZZ
            elif process == 2: 
                if ( gen_part[2].pdgId * gen_part[3].pdgId > 0 ): 
                    dkfactor_qcd = 28.55 / 15.51 - 1. # W+Z
                else:                  
                    dkfactor_qcd = 18.19 / 9.53 - 1. # W-Z
            
            ewkUncert = 1. + abs(dkfactor_qcd * self.table[itab][jtab]) if rhozz<0.3 else 1. + abs(self.table[itab][jtab])

            if self.syst_var == "EWKUp": 
                kEW *= ewkUncert
            elif self.syst_var == "EWKDown": 
                kEW /= ewkUncert
        
        self.out.fillBranch("kEW", kEW)
        return True

