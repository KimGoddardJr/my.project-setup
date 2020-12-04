import os
import sys
from collections import defaultdict
from functools import singledispatch

import json

class source_structure(object):

    def __init__(self,proj_name):
        self.proj_name = proj_name
    
    def check_folder(self,parent_folder):
        #children_files = os.listdir(parent_folder)
        if os.path.isdir(parent_folder):
            folder_dict = {'{}'.format(os.path.basename(parent_folder)) : {} }
            for folder in folder_dict:
                subfolders = os.listdir(parent_folder)
                try:
                    #folder_dict['type'] = "directory"
                    folder_dict[folder] = [self.check_folder(os.path.join(parent_folder,x)) for x in subfolders]
                    #print(data_path)
                except:
                    print('no folder inside')

                return folder_dict

    def cleanup(self,data):
        final_dict = {}
        try:
            for a, b in data.items():
                if b:
                    if isinstance(b, dict):
                        final_dict[a] = self.cleanup(b)
                    elif isinstance(b, list):
                        final_dict[a] = list(filter(None, [self.cleanup(i) for i in b]))
                    else:
                        final_dict[a] = b
                else:
                    final_dict[a] = [] 
            return final_dict
        except:
            pass
     
    def write_a_structure(self,output_path,folder_dict):
         
         file_path = os.path.join(output_path,self.proj_name)
         clean_text = self.cleanup(folder_dict)
         json_text = json.dumps(clean_text, indent = 2, sort_keys = True)

         with open("{}.json".format(file_path), "w") as json_file:
             #json_text = json.dumps(clean_text, indent = 2, sort_keys = True)
             json_file.write(json_text)

         json_file.close()


##json_dummy = {'data': {'keyA': [{'subkeyA1': 'valueA1', 'subkeyA2': 'valueA2'}, {'subkeyA3': ''}], 'keyB': [None,None,None]}}

#source_project = source_structure('PINATA')
#data = source_project.check_folder('/Volumes/projects/_TO_BE_DELETED_SOON/2020_BA_LaVidaDeUnaPinata')

#source_project.write_a_structure('/Users/patagu/Documents',data)


#json.dump('/Users/patagu/Documents/dump', remove_null_bool(data))

##print(data)
