import os
import sys
from collections import defaultdict

import json


class setup_maker(object):

    def __init__(self,json_path):
        self.json_path = json_path

    def folder_setup(self,project_name,project_path,json_template):
        json_file_path = os.path.join(self.json_path,json_template)

        with open('{}'.format(json_file_path)) as template_file:
            template = json.load(template_file)

        type(template)
        
        project_path = os.path.join(project_path,project_name)
        self.makedir(project_path)
        container = [x for x in template][0]
        self.recursive_foldering(project_path, template[container])

    
    def recursive_foldering(self, project_path, container):

        for (cur_folder, subfolders) in container.items():
            new_path = os.path.join(project_path,cur_folder)
            self.makedir(new_path)
            print(new_path)
            for (x_folder,y_folders) in subfolders.items():
                #print(x_folder)
                mod_path = os.path.join(new_path,x_folder)
                print(mod_path)
                self.makedir(mod_path)
                #print(new_path)
                self.recursive_foldering(mod_path,subfolders[x_folder])

    def makedir(self,folder_name):
            try:
                os.makedirs(folder_name, exist_ok=True)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
                pass

#os.rmdir('/home/kg/Documents/MIKE')
#setup = setup_maker('JSON')
#setup.folder_setup('STELLA','/home/kg/Documents/','model-template.json')
