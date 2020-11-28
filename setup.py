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
        try:
            for (i,i_group) in enumerate(container):
                #print(i,i_group)
                subfolder_id = container[i]
                for (parent_dir, children_dirs) in subfolder_id.items():
                    subfolder = os.path.join(project_path,parent_dir)
                    self.makedir(subfolder)
                    print(subfolder)

                    for (j,j_group) in enumerate(children_dirs):
                        child_folder_id = children_dirs[j]

                        for (x_folder, dummy) in child_folder_id.items():
                            mod_path = os.path.join(subfolder,x_folder)
                            print(mod_path)
                            self.makedir(mod_path)
                            #print(new_path)
                            self.recursive_foldering(mod_path,child_folder_id[x_folder])
        except:
            pass


    def makedir(self,folder_name):
            try:
                os.makedirs(folder_name, exist_ok=True)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
                pass

#os.rmdir('/home/kg/Documents/MIKE')
setup = setup_maker('/home/kg/Documents')
setup.folder_setup('MENGELE','/home/kg/Documents/','MENGELE.json')
