import yaml
from ROOT import *
import ROOT
import sys
import numpy
import uproot

with open('ROOTfiles_2018_data.yml', 'r') as f2_yml:
    _dict_yml_ctgry = yaml.load(f2_yml)

#_PDs = [# for now since we remove the HLTs here we need this to be in this specific order. Look to change this soon with skimmed trees by HLTs
#   'SingleElectron',
#   'SingleMuon',
#   'DoubleMuon',
#   'DoubleEG',
#   'MuonEG']

_PDs = [# for now since we remove the HLTs here we need this to be in this specific order. Look to change this soon with skimmed trees by HLTs
   'SingleMuon',
   'DoubleMuon',
   'EGamma']
_nPDs = len(_PDs)

event_list = {}
#event_array = []
prf = TProof.Open("lite://")
for j in range(_nPDs):
   pd = _PDs[j]
   chain = TChain("Events")
   for file in _dict_yml_ctgry[pd]['files']:
     print file
     up_file = uproot.open(file)["Events"]
     print 'did I get here?'
     up_data =  up_file.arrays(["run", "luminosityBlock", "event"]) 
     print 'what about here?'
     length = len(up_file)
     for i in range (0,length):
     	if pd not in event_list.keys():
		event_list.setdefault(pd, []).append(up_data["event"][i])
		#event_array.append(up_data["event"][i])
	for key in event_list:
		if up_data["event"][i] in event_list[key]:continue
		else:event_list.setdefault(pd, []).append(up_data["event"][i])
		#event_array.append(up_data["event"][i])
     	#else:
     	#	if up_data["event"][i] not in event_list[pd]:
        #             	event_list.setdefault(pd, []).append(up_data["event"][i])
with open('myfile_2018.txt', 'w') as f:
    print >> f, event_list
