from ROOT import *
import yaml
import os
import multiprocessing as mp


def filter_file(file_in, file_out):
   try:
      f_in = TFile(file_in, "READ")
      if f_in.IsZombie():
         return file_in
      tree_in = f_in.Get("Events")
      if tree_in.GetEntriesFast() <= 1:
         return file_in
      f_out = TFile(file_out, "recreate")
      selection = 'lep_category>0'
      tree_out = tree_in.CopyTree(selection)
      f_out.Write()
      f_out.Close()
      f_in.Close()
   except:
      print 'Bad file:', file_in 
      return file_in
   print 'finished:', file_in


def main():
   with open('ROOTfiles.yml', 'r') as f_yml: 
      dict_yml = yaml.load(f_yml)

   # datasets = ['DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8']
   pool = mp.Pool(processes=10)
   jobs = []
   for dataset in dict_yml:
      for file_in in dict_yml[dataset]['files']:
         file_out = file_in.replace('MonoZAnalysis_BladeRunner_MonoZ_2017', 'MonoZAnalysis_BladeRunner_MonoZ_2017_test')
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
