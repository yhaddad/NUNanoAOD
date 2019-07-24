import yaml
import sys
import os

def get_files():
   # The top directory which contains all the datasets
   dir_monoZ = '/eos/cms/store/group/phys_exotica/monoZ/LionKing2016/'
   if len(sys.argv) == 2:
      dir_monoZ = sys.argv[1]

   dict_files = {}
   for path, subdirs, files in os.walk(dir_monoZ): 
      sub_path_splited = path.split(dir_monoZ)[1].split('/')
      #if len(sub_path_splited) != 4:
      #   continue
      dataset = sub_path_splited[0]
      if dataset not in dict_files:
         dict_files[dataset] = {'files':[]}
      for name in files:
         if name.split('.')[-1] == 'root':
            dict_files[dataset]['files'].append( os.path.join(path, name) )

   with open('LionKing2016_ROOTfiles.yml', 'w') as outfile:
      yaml.dump(dict_files, outfile, default_flow_style=False)

get_files()
