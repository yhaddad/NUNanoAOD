from ROOT import *
import yaml
import os
import argparse
import multiprocessing as mp



parser = argparse.ArgumentParser()
parser.add_argument("-yml_in", "--yml_in", type=str, 
   default='ROOTfiles_CtgryFltrd_2016.yml', 
   help="yml_in")
parser.add_argument("-sub_dir", "--sub_dir", type=str, 
   default='MonoZAnalysis_BladeRunner_MonoZ_2016_0212_data_test', 
   help="tsub_dir")
parser.add_argument("-new_dir", "--new_dir", type=str, 
   default='MonoZAnalysis_BladeRunner_MonoZ_2016_0212_data_NoDplct', 
   help="new_dir")
options = parser.parse_args()


def filter_file(file_in, file_out, run_event):
   f_in = TFile(file_in, "READ")
   tree_in = f_in.Get("Events")
   f_out = TFile(file_out, "recreate")
   tree_out = tree_in.CloneTree(0)

   for i in xrange(tree_in.GetEntries()):
      tree_in.GetEntry(i)
      _run = tree_in.run
      _event = tree_in.event
      if _run not in run_event:
         run_event[_run] = set()
      if _event in run_event[_run]:
         continue
      run_event[_run].add(_event)
      tree_out.Fill()

   f_out.Write()
   f_out.Close()
   f_in.Close()
   print 'finished:', file_in.split('/eos/cms/store/group/phys_exotica/monoZ/')[-1]


def main():
   with open(options.yml_in, 'r') as f_yml: 
      dict_yml = yaml.load(f_yml)

   datasets = ['MuonEG', 'DoubleEG', 'DoubleMuon', 'SingleElectron', 'SingleMuon']
   run_event = {}

   # manager = mp.Manager()
   # run_event = manager.dict()

   # pool = mp.Pool(processes=10)

   for dataset in datasets:
      for file_in in dict_yml[dataset]['files']:
         file_out = file_in.replace(options.sub_dir, options.new_dir)
         dir_out = '/'.join(file_out.split('/')[:-1])
         if not os.path.exists(dir_out):
            os.makedirs(dir_out)
         filter_file(file_in, file_out, run_event)
         # jobs.append(pool.apply_async( filter_file, args=(file_in, file_out, run_event) ) )

   # pool.close()
   # pool.join()

         # f_in = TFile(file_in, "READ")
         # tree_in = f_in.Get("Events")
         # f_out = TFile(file_out, "recreate")
         # tree_out = tree_in.CloneTree(0)

         # for i in xrange(tree_in.GetEntries()):
         #    tree_in.GetEntry(i)

         #    _run = tree_in.run
         #    _event = tree_in.event
         #    if _run not in run_event:
         #       run_event[_run] = set()
         #    if _event in run_event[_run]:
         #       continue

         #    run_event[_run].add(_event)
         #    tree_out.Fill()

         # f_out.Write()
         # f_out.Close()
         # f_in.Close()
         # print 'finished:', file_in.split('/eos/cms/store/group/phys_exotica/monoZ/')[-1]
         

if __name__ == "__main__":
   main()
