import os
import sys
from collections import defaultdict

import json

class source_structure(object):

    def __init__(self,proj_name):
        self.proj_name = proj_name
    
    def check_folder(self,parent_folder):
        children_files = os.listdir(parent_folder)
        
        for data in children_files:
            data_path = os.path.join(parent_folder,data)
            if os.path.isdir(data_path):
                self.write_a_structure(data_path)


                self.check_folder(data_path)
     
     def write_a_structure(self,folder_basename):



#os.rmdir('/home/kg/Documents/MIKE')
source_structure('FIDO').check_folder('/home/kg/Downloads')
