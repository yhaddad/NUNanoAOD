import yaml
import os

def get_files():
   dir_monoZ = '/eos/cms/store/group/phys_exotica/monoZ/MonoZAnalysis_BladeRunner_MonoZ_2017_1111/'

   dict_files = {}
   for path, subdirs, files in os.walk(dir_monoZ): 
      sub_path_splited = path.split(dir_monoZ)[1].split('/')
      if len(sub_path_splited) != 4:
         continue
      dataset = sub_path_splited[0]
      if dataset not in dict_files:
         dict_files[dataset] = {'files':[]}
      for name in files:
         if name.split('.')[-1] == 'root':
            dict_files[dataset]['files'].append( os.path.join(path, name) )

   with open('ROOTfiles.yml', 'w') as outfile:
      yaml.dump(dict_files, outfile, default_flow_style=False)

get_files()

