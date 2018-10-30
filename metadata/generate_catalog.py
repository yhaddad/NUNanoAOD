from Utilities.General.cmssw_das_client import get_data as das_query
import argparse
import yaml
import ROOT 

parser = argparse.ArgumentParser()

parser.add_argument("-c", "--config", type=str, default='configs/sample_mc_2017.dat',help="directory config")
parser.add_argument("-p", "--use_parent", type=str, default='True',
                    help="use MiniAOD parent instead of NanoAOD")
parser.add_argument("--include_files", "--include_files", type=str, default='True', help="")
options = parser.parse_args()

def get_nevent(infile):
        rootf= ROOT.TFile.Open(infile, 'READ')
        tree = rootf.Get("Events")
        print ("root event : ", infile , " : ", tree.GetEntries())

def files_from_das(dataset):
        if options.use_parent :
                format_ = dataset.split("/")[2]
                if 'SIM' in format_:
                        dataset.replace("NANOAODSIM", "MINIAODSIM")
                else:
                        dataset.replace("NANOAOD", "MINIAOD")
        response = das_query(
                "file dataset=%s | grep file.name,file.nevents" % ( dataset )
        )
        root_file_list = []
        nevents = 0
        for d in response.get("data",[]):
                for jf in d["file"]:
                        if "nevents" in jf:
                                nevents += jf["nevents"]
                                root_file_list.append({ 
                                        "name" : str(jf["name"]), 
                                        "nevents" : int(jf["nevents"]) 
                                })
                                break
        return root_file_list, nevents

data_file = open(options.config, "r")
data = data_file.read()

catalog = {}
import yaml

xsection = None
with open("configs/xsections.yaml", 'r') as stream:
        try:
                xsection = yaml.load(stream)
        except yaml.YAMLError as exc:
                print(exc)


for s in data.split('\n'):
        if len(s) <= 1: continue
        if "#" in s: continue
        tag = s.split("/")[1]
        print " --- ",  tag 
        files_, nevents = files_from_das(s)
        xsec = xsection[tag].get("xsec", 1.0)
        catalog[s] = {
                "sample": tag,
                #"files" : [ f["name"] for f in files_ ],
                "nevents" : nevents,
                "xsec"    : xsec
        }
        
import yaml
with open('catalog_2017.yml', 'w') as outfile:
        yaml.dump(catalog, outfile, default_flow_style=False)
