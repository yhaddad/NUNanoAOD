import yaml
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", type=str, default='/eos/cms/store/group/phys_exotica/monoZ/LionKing2018/', help="top directory containing all the datasets")
options = parser.parse_args()

dir_monoZ = options.dir

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

with open('LionKing2018_ROOTfiles.yml', 'w') as outfile:
   yaml.dump(dict_files, outfile, default_flow_style=False)


