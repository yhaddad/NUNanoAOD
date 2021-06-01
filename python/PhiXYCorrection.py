#Written for NanoAOD March 2020. Chad Freer
#Thanks to Laurent Thomas for corrections. See:
#https://lathomas.web.cern.ch/lathomas/METStuff/XYCorrections/XYMETCorrection.h
import ROOT
import os
import numpy as np
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class PhiXYCorrection(Module):
    def __init__(self, norm=True, era='2019', metBranchName="MET", isMC=1, isUL=0, sys='', verbose=False):
        self.era = era
        self.isMC = isMC
        self.isUL = isUL
        self.sys = '_nom' if sys=='' else '_'+sys
        self.verbose = verbose
        self.metBranchName = metBranchName
        self.xy_corr = {
            # isUL==0
            'y2016B' : [-0.0478335, -0.108032, 0.125148, 0.355672],
            'y2016C' : [-0.0916985, 0.393247, 0.151445, 0.114491],
            'y2016D' : [-0.0581169, 0.567316, 0.147549, 0.403088],
            'y2016E' : [-0.065622, 0.536856, 0.188532, 0.495346],
            'y2016F' : [-0.0313322, 0.39866, 0.16081, 0.960177],
            'y2016G' : [0.040803, -0.290384, 0.0961935, 0.666096],
            'y2016H' : [0.0330868, -0.209534, 0.141513, 0.816732],
            'y2017B' : [-0.259456, 1.95372, 0.353928, -2.46685],
            'y2017C' : [-0.232763, 1.08318, 0.257719, -1.1745],
            'y2017D' : [-0.238067, 1.80541, 0.235989, -1.44354],
            'y2017E' : [-0.212352, 1.851, 0.157759, -0.478139],
            'y2017F' : [-0.232733, 2.24134, 0.213341, 0.684588],
            'y2018A' : [0.362865, -1.94505, 0.0709085, -0.307365],
            'y2018B' : [0.492083, -2.93552, 0.17874, -0.786844],
            'y2018C' : [0.521349, -1.44544, 0.118956, -1.96434],
            'y2018D' : [0.531151, -1.37568, 0.0884639, -1.57089],
            'y2016MC' : [-0.195191, -0.170948, -0.0311891, 0.787627],
            'y2017MC' : [-0.217714, 0.493361, 0.177058, -0.336648],
            'y2018MC' : [0.296713, -0.141506, 0.115685, 0.0128193],

            # isUL==1
            'yUL2016B' : [-0.0214894, -0.188255, 0.0876624, 0.812885],
            'yUL2016C' : [-0.032209, 0.067288, 0.113917, 0.743906],
            'yUL2016D' : [-0.0293663, 0.21106, 0.11331, 0.815787],
            'yUL2016E' : [-0.0132046, 0.20073, 0.134809, 0.679068],
            'yUL2016F' : [-0.0543566, 0.816597, 0.114225, 1.17266],
            'yUL2016Flate' : [0.134616, -0.89965, 0.0397736, 1.0385],
            'yUL2016G' : [0.121809, -0.584893, 0.0558974, 0.891234],
            'yUL2016H' : [0.0868828, -0.703489, 0.0888774, 0.902632],
            'yUL2017B' : [-0.211161, 0.419333, 0.251789, -1.28089],
            'yUL2017C' : [-0.185184, -0.164009, 0.200941, -0.56853],
            'yUL2017D' : [-0.201606, 0.426502, 0.188208, -0.58313],
            'yUL2017E' : [-0.162472, 0.176329, 0.138076, -0.250239],
            'yUL2017F' : [-0.210639, 0.72934, 0.198626, 1.028],
            'yUL2018A' : [0.263733, -1.91115, 0.0431304, -0.112043],
            'yUL2018B' : [0.400466, -3.05914, 0.146125, -0.533233],
            'yUL2018C' : [0.430911, -1.42865, 0.0620083, -1.46021],
            'yUL2018D' : [0.457327, -1.56856, 0.0684071, -0.928372],
            'yUL2016MCnonAPV' : [-0.153497, -0.231751, 0.00731978, 0.243323],
            'yUL2016MCAPV' : [-0.188743, 0.136539, 0.0127927, 0.117747],
            'yUL2017MC' : [-0.300155, 1.90608, 0.300213, -2.02232],
            'yUL2018MC' : [0.183518, 0.546754, 0.192263, -0.42121],
        }

        self.xy_corr_v2 = {
            'y2016B' : [-0.0374977, 0.00488262, 0.107373, -0.00732239],
            'y2016C' : [-0.0832562, 0.550742, 0.142469, -0.153718],
            'y2016D' : [-0.0400931, 0.753734, 0.127154, 0.0175228],
            'y2016E' : [-0.0409231, 0.755128, 0.168407, 0.126755],
            'y2016F' : [-0.0161259, 0.516919, 0.141176, 0.544062],
            'y2016G' : [0.0583851, -0.0987447, 0.0641427, 0.319112],
            'y2016H' : [0.0706267, -0.13118, 0.127481, 0.370786],
            'y2017B' : [-0.19563, 1.51859, 0.306987, -1.84713],
            'y2017C' : [-0.161661, 0.589933, 0.233569, -0.995546],
            'y2017D' : [-0.180911, 1.23553, 0.240155, -1.27449],
            'y2017E' : [-0.149494, 0.901305, 0.178212, -0.535537],
            'y2017F' : [-0.165154, 1.02018, 0.253794, 0.75776],
            'y2018A' : [0.362642, -1.55094, 0.0737842, -0.677209],
            'y2018B' : [0.485614, -2.45706, 0.181619, -1.00636],
            'y2018C' : [0.503638, -1.01281, 0.147811, -1.48941],
            'y2018D' : [0.520265, -1.20322, 0.143919, -0.979328],
            'y2016MC' : [-0.159469, -0.407022, -0.0405812, 0.570415],
            'y2017MC' : [-0.182569, 0.276542, 0.155652, -0.417633],
            'y2018MC' : [0.299448, -0.13866, 0.118785, 0.0889588],
        }


    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("MET_pt"+self.sys, "F")
        self.out.branch("MET_phi"+self.sys, "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        year = self.era
        isMC = self.isMC
        #Get the variables we need.
        if hasattr(event, "PV_npvs"): npv = int(getattr(event, "PV_npvs"))
        if hasattr(event, "run"): runnb = int(getattr(event, "run")) 
        
        _sys = '' if self.sys=='_nom' else self.sys
        _br_pt = self.metBranchName + "_T1Smear_pt" + _sys if self.isMC else self.metBranchName + "_T1_pt" + _sys
        _br_phi = self.metBranchName + "_T1Smear_phi" + _sys if self.isMC else self.metBranchName + "_T1_phi" + _sys
        if hasattr(event, _br_pt): uncormet = float(getattr(event, _br_pt))
        if hasattr(event, _br_phi): uncormet_phi =float(getattr(event, _br_phi))
   
        if npv > 100: npv = 100
        runera='y2019MC'
        usemetv2 = False
        #Determine the era for MC samples
        if isMC:
            if(year == '2016'): runera = 'y2016MC'
            elif(year == '2017'): runera = 'y2017MC'; usemetv2 = True
            elif(year == '2018'): runera = 'y2018MC'
            #Couldn't find data/MC era => no correction applied
            else: return
        else:
            #Find the data era via run number
            if not self.isUL:
                #2016
                if(272007 <= runnb <= 275376): runera = 'y2016B'
                elif(275657 <= runnb <= 276283): runera = 'y2016C'
                elif(276315 <= runnb <= 276811): runera = 'y2016D'
                elif(276831 <= runnb <= 277420): runera = 'y2016E'
                elif(277772 <= runnb <= 278808): runera = 'y2016F'
                elif(278820 <= runnb <= 280385): runera = 'y2016G'
                elif(280919 <= runnb <= 284044): runera = 'y2016H'
                #2017
                elif(297020 <= runnb <= 299329): runera = 'y2017B'; usemetv2 = True
                elif(299337 <= runnb <= 302029): runera = 'y2017C'; usemetv2 = True
                elif(302030 <= runnb <= 303434): runera = 'y2017D'; usemetv2 = True
                elif(303435 <= runnb <= 304826): runera = 'y2017E'; usemetv2 = True
                elif(304911 <= runnb <= 306462): runera = 'y2017F'; usemetv2 = True
                #2018
                elif(315252 <= runnb <= 316995): runera = 'y2018A'
                elif(316998 <= runnb <= 319312): runera = 'y2018B'
                elif(319313 <= runnb <= 320393): runera = 'y2018C'
                elif(320394 <= runnb <= 325273): runera = 'y2018D'
                #Couldn't find data/MC era => no correction applied
                else: return 
            else:
                # UL 2016
                if(272007 <= runnb <= 275376) : runera = 'yUL2016B';
                elif(275657 <= runnb <= 276283) : runera = 'yUL2016C';
                elif(276315 <= runnb <= 276811) : runera = 'yUL2016D';
                elif(276831 <= runnb <= 277420) : runera = 'yUL2016E';
                elif((277772 <= runnb <= 278768) or runnb==278770) : runera = 'yUL2016F';
                elif((278801 <= runnb <= 278808) or runnb==278769) : runera = 'yUL2016Flate';
                elif(278820 <= runnb <= 280385) : runera = 'yUL2016G';
                elif(280919 <= runnb <= 284044) : runera = 'yUL2016H';
                # UL 2017
                elif(297020 <= runnb <= 299329) : runera = 'yUL2017B'; usemetv2 = False;
                elif(299337 <= runnb <= 302029) : runera = 'yUL2017C'; usemetv2 = False;
                elif(302030 <= runnb <= 303434) : runera = 'yUL2017D'; usemetv2 = False;
                elif(303435 <= runnb <= 304826) : runera = 'yUL2017E'; usemetv2 = False;
                elif(304911 <= runnb <= 306462) : runera = 'yUL2017F'; usemetv2 = False;
                # UL 2018
                elif(315252 <= runnb <= 316995) : runera = 'yUL2018A';
                elif(316998 <= runnb <= 319312) : runera = 'yUL2018B';
                elif(319313 <= runnb <= 320393) : runera = 'yUL2018C';
                elif(320394 <= runnb <= 325273) : runera = 'yUL2018D';
                #Couldn't find data/MC era => no correction applied
                else: return 

        METxcorr = 0.
        METycorr = 0. 
        if not usemetv2: 
            #Current recommendation for 2016 and 2018
            METxcorr = -(self.xy_corr[runera][0] * npv + self.xy_corr[runera][1])
            METycorr = -(self.xy_corr[runera][2] * npv + self.xy_corr[runera][3])
        else: 
            #these are the corrections for v2 MET recipe (currently recommended for 2017)
            METxcorr = -(self.xy_corr_v2[runera][0] * npv + self.xy_corr_v2[runera][1])
            METycorr = -(self.xy_corr_v2[runera][2] * npv + self.xy_corr_v2[runera][3])

        #Now time to remake the MET_pt
        CorrectedMET_x = uncormet * math.cos(uncormet_phi) + METxcorr
        CorrectedMET_y = uncormet * math.sin(uncormet_phi) + METycorr
        CorrectedMET = math.sqrt(CorrectedMET_x*CorrectedMET_x+CorrectedMET_y*CorrectedMET_y)

        #Now time to recalculate the MET_phi
        if(CorrectedMET_x==0. and CorrectedMET_y>0.)    : CorrectedMETPhi = math.pi
        elif(CorrectedMET_x==0. and CorrectedMET_y<0.)  : CorrectedMETPhi = -math.pi
        elif(CorrectedMET_x > 0.)                       : CorrectedMETPhi = math.atan(CorrectedMET_y/CorrectedMET_x)
        elif(CorrectedMET_x < 0. and CorrectedMET_y>0.) : CorrectedMETPhi = math.atan(CorrectedMET_y/CorrectedMET_x) + math.pi
        elif(CorrectedMET_x < 0. and CorrectedMET_y<0.) : CorrectedMETPhi = math.atan(CorrectedMET_y/CorrectedMET_x) - math.pi
        else                                            : CorrectedMETPhi = 0.
        self.out.fillBranch("MET_pt"+self.sys, CorrectedMET)
        self.out.fillBranch("MET_phi"+self.sys, CorrectedMETPhi)
        return True
