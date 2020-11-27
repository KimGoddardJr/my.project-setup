import os
import sys
from collections import defaultdict

import json

class source_structure(object):

    def __init__(self,proj_name):
        self.proj_name = proj_name
    
    def check_folder(self,parent_folder):
        #children_files = os.listdir(parent_folder)
        if os.path.isdir(parent_folder):
            folder_dict = {'{}'.format(os.path.basename(parent_folder)) : {} }
            for folder, folders in folder_dict.items():
                try:
                    #folder_dict['type'] = "directory"
                    folder_dict[folder] = [self.check_folder(os.path.join(parent_folder,x)) for x in os.listdir\
                    (parent_folder)]
                    #print(data_path)
                except:
                    print('no folder inside')

                return folder_dict
     
    def write_a_structure(self,output_path,folder_dict):
         file_path = os.path.join(output_path,self.proj_name)
         with open("{}.json".format(file_path), "w") as json_file:

            json_file.write(folder_dict)
         
         json_file.close()
        



#os.rmdir('/home/kg/Documents/MIKE')
json_result = json.dumps(source_structure('FIDO').check_folder('/Users/patagu/Dropbox/orga_shit'), indent = 2, sort_keys = True)
#print(json_result)


print(json_result)


