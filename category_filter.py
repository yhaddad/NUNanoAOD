from ROOT import *
import yaml
import os
import argparse
import multiprocessing as mp


parser = argparse.ArgumentParser()
parser.add_argument("-year", "--year", type=str, 
   default='2016', 
   help="year")
parser.add_argument("-yml_in", "--yml_in", type=str, 
   default='ROOTfiles_2016.yml', 
   help="yml_in")
parser.add_argument("-sub_dir", "--sub_dir", type=str, 
   default='MonoZAnalysis_BladeRunner_MonoZ_2016_0212_data', 
   help="tsub_dir")
parser.add_argument("-new_dir", "--new_dir", type=str, 
   default='MonoZAnalysis_BladeRunner_MonoZ_2016_0212_data_test', 
   help="new_dir")
options = parser.parse_args()

if options.year == '2016':
   from HLT_NotIn_2016 import HLT_paths
elif options.year == '2017':
   from HLT_NotIn_2017 import HLT_paths
else:
   print 'Which year?'


def filter_file(file_in, file_out):
   try:
      f_in = TFile(file_in, "READ")
      if f_in.IsZombie():
         return 'Zombie: ' + file_in
      tree_in = f_in.Get("Events")
      if tree_in.GetEntriesFast() <= 1:
         return 'No entry: ' + file_in
      HLT_paths_cut = [HLT for HLT in HLT_paths if tree_in.GetBranchStatus(HLT)]
      if not HLT_paths_cut:
         return 'No HLT: ' + file_in
      f_out = TFile(file_out, "recreate")
      selection = '(lep_category>0)' + " && (" + "||".join(HLT_paths_cut) + ")"
      tree_out = tree_in.CopyTree(selection)
      f_out.Write()
      f_out.Close()
      f_in.Close()
   except:
      print 'Bad file:', file_in 
      return 'exception: ' + file_in
   print 'finished:', file_in.split('/eos/cms/store/group/phys_exotica/monoZ/')[-1]


def main():
   with open(options.yml_in, 'r') as f_yml: 
      dict_yml = yaml.load(f_yml)

   datasets = ['SingleElectron', 'SingleMuon', 'DoubleEG', 'DoubleMuon', 'MuonEG']
   pool = mp.Pool(processes=10)
   jobs = []
   # for dataset in dict_yml:
   for dataset in datasets:
      for file_in in dict_yml[dataset]['files']:
         file_out = file_in.replace(options.sub_dir, options.new_dir)
         dir_out = '/'.join(file_out.split('/')[:-1])
         if not os.path.exists(dir_out):
            os.makedirs(dir_out)
         jobs.append(pool.apply_async( filter_file, args=(file_in, file_out) ) )
         
   pool.close()
   pool.join()
   bad_files = [file for file in [p.get() for p in jobs] if file]
   with open('bad_files.txt', 'w') as f_bad:
      for bad_file in bad_files:
         f_bad.write("%s\n" % bad_file)


if __name__ == "__main__":
   main()
