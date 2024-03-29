import ROOT
import sys, os
import numpy as np
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

ROOT.PyConfig.IgnoreCommandLineOptions = True


class GenWeightProducer(Module):
    def __init__(self, isMC, xsec=1.0, nevt=1, dopdf=True, do_xsecscale=False):
        # lumi and cross sections should be in femptobarn
        self.isMC = isMC
        self.nevt = nevt
        self.xsec = xsec
        self.dopdf = dopdf
        self.do_xsecscale = do_xsecscale
        # pdf's
        self.pset = None
        self.pdfs = None

    def LHAPDFConfig(self):
        if self.pset is not None:
            return True
        current = os.getcwd()
        os.chdir(os.environ["CMSSW_BASE"])
        path = os.popen("scram tool info LAHPDF | grep LIBDIR").read()
        os.chdir(current)
        path = path.split("=")[-1] +"/python2.7/site-packages/"
        path = path.replace("\n","")

        sys.path.insert(1, path)
        try:
            global lhpdf
            import lhpdf
        except:
            return False

        return True

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def LHPDFweight(self, gencol):
        if not self.LHAPDFConfig():
            return 0, None
        if self.pset is None:
            self.pset = lhapdf.getPDFSet("NNPDF31_nnlo_as_0118")
            self.pdfs = self.pset.mkPDFs()

        pdf_weight = np.zeros(self.pset.size)

        x1_nom = self.pdfs[0].xfxQ(gencol.id1, gencol.x1, gencol.sclaePDF)
        x2_nom = self.pdfs[0].xfxQ(gencol.id2, gencol.x2, gencol.sclaePDF)

        w_nom = x1_nom * x2_nom
        for i in range(self.pset.size):
            x1 = self.pdfs[i].xfxQ(gencol.id1, gencol.x1, gencol.scalePDF)
            x2 = self.pdfs[i].xfxQ(gencol.id2, gencol.x2, gencol.scalePDF)
            pdf_weight[i] = x1 * x2 / w_nom

        return self.pset.size, pdf_weight


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.isfirst = True
        self.out = wrappedOutputTree
        infostr =""
        if self.isMC:
            infostr = "section/nEvent (CrossSection={}, nEvent={})".format(self.xsec, self.nevt)
        else:
            infostr = "Storing Lumi={}".format(self.xsec)
        self.out.branch("weight"    , "F") # , title=infostr)
        self.out.branch("xsecscale" , "F") # , title=infostr)
        self.out.branch("pdfw_Up"   , "F") # , title="PDF Weight uncertainty up")
        self.out.branch("pdfw_Down" , "F") # , title="PDF Weight uncertainty down")
        self.out.branch("QCDScale0wUp"  ,   "F")
        self.out.branch("QCDScale0wDown",   "F")
        self.out.branch("QCDScale1wUp"  ,   "F")
        self.out.branch("QCDScale1wDown",   "F")
        self.out.branch("QCDScale2wUp"  ,   "F")
        self.out.branch("QCDScale2wDown",   "F")
        
        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def getobject(self, event, name):
        obj = None
        try:
            obj = getattr(event, name)
        except RuntimeError:
            pass
        return obj

    def analyze(self, event):
        # only valid in the MC samples
        weight = 1.0
        if self.isMC:
            weight = getattr(event, "genWeight")
            if self.do_xsecscale:
                weight = self.xsec/self.nevt * weight
            #signs = 1 if initw > 0 else -1

        self.out.fillBranch("weight"   , weight )
        self.out.fillBranch("xsecscale", weight * self.nevt if self.do_xsecscale else weight )

        # -----------------
        # PDF uncertainties
        # -----------------
        mean = 1.0
        werr = 0.0

        # -----------------------
        # QCD scale uncertainties
        # -----------------------
        try:
            # (ren_sc, fac_sc) = {0: (0.5, 0.5), 1: (0.5, 1.0), 2: (0.5, 2.0), 3: (1.0, 0.5), 4: (1.0, 1.0), 5: (1.0, 2.0), 6: (2.0, 0.5), 7: (2.0, 1.0), 8: (2.0, 2.0)} 
            qcd_scale = self.getobject(event, "LHEScaleWeight")
            # Scale0: ren_sc in [0.5, 2.0] and fac_sc = 1.0
            self.out.fillBranch("QCDScale0wUp"  ,   qcd_scale[1])
            self.out.fillBranch("QCDScale0wDown",   qcd_scale[7])
            # Scale1: ren_sc = 1.0 and fac_sc in [0.5, 2.0]
            self.out.fillBranch("QCDScale1wUp"  ,   qcd_scale[3])
            self.out.fillBranch("QCDScale1wDown",   qcd_scale[5])
            # Scale2: (ren_sc, fac_sc) in [(0.5, 0.5), (2.0, 2.0)]
            self.out.fillBranch("QCDScale2wUp"  ,   qcd_scale[0])
            self.out.fillBranch("QCDScale2wDown",   qcd_scale[8])
        except:
            self.out.fillBranch("QCDScale0wUp"  ,   1.0)
            self.out.fillBranch("QCDScale0wDown",   1.0)
            self.out.fillBranch("QCDScale1wUp"  ,   1.0)
            self.out.fillBranch("QCDScale1wDown",   1.0)
            self.out.fillBranch("QCDScale2wUp"  ,   1.0)
            self.out.fillBranch("QCDScale2wDown",   1.0)

        if not self.isMC:
            return True
        if not self.dopdf:
            return True

        w_pdf = self.getobject(event, "LHEPdfWeight" )
        n_pdf = self.getobject(event, "nLHEPdfWeight" )

        if self.isfirst:
             w_pdf = getattr(event, "LHEPdfWeight" )
             n_pdf = getattr(event, "nLHEPdfWeight")
             self.isfirst = False

        if w_pdf == 0 or n_pdf is None:
            n_pdf, w_pdf = self.LHAPDFweight(Object(event,"Generator"))

        if n_pdf is not None and n_pdf != 0:
            if not isinstance(w_pdf, np.ndarray):
                w_pdf = np.asarray([w_pdf[i] for i in range(n_pdf)])
            if n_pdf == 101:
                pdf_ = np.sort(w_pdf[1:])
                w84_ = pdf_[84]
                w16_ = pdf_[16]
                mean = (w84_ + w16_)/2.0
                werr = (w84_ - w16_)/2.0
            else:
                mean = np.mean(w_pdf[1:])
                werr = np.std(w_pdf[1:])

        self.out.fillBranch("pdfw_Up",   1 + werr/mean)
        self.out.fillBranch("pdfw_Down", 1 - werr/mean)

        return True
