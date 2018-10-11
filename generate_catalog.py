import argparse
import yaml
import ROOT 

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--config", type=str, default='configs/sample_mc_2017.dat',help="directory config")
parser.add_argument("-d", "--dir"   , type=str, default='/eos/cms/', help="scan this directory")
parser.add_argument("-x", "--xsec"  , type=str, default='configs/xsections.yaml', help="scan this directory")
options = parser.parse_args()

def get_nevent(infile):
    rootf= ROOT.TFile.Open(infile, 'READ')
    tree = rootf.Get("Events")
    print ("root event : ", infile , " : ", tree.GetEntries())

xsec_data = None 
with open(options.xsec, 'r') as stream:
    try:
        xsec_data = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

import os
import os.path


files = []
for dirpath, dirnames, filenames in os.walk(options.dir):
    for filename in [f for f in filenames if f.endswith(".root")]:
        files.append(os.path.join(dirpath, filename))
        get_nevent(os.path.join(dirpath, filename))

data_file = open(options.config, "r")
data = data_file.read()


catalog = {}
for s in data.split('\n'):
    if len(s) <= 1: continue
    tag = s.split("/")[1]
    files_ = []
    for f in files:
        if tag in f:
            files_.append(f)
    xsec, err = 0, 0
    if tag in xsec_data.keys():
        xsec = xsec_data[tag].get('xsec', 0.0)
    if len(files_) == 0: continue
    catalog[tag] = { "files" : files_, "xsec": xsec, "xsec_err": err} 


import yaml
with open('catalog.yml', 'w') as outfile:
    yaml.dump(catalog, outfile, default_flow_style=False)
