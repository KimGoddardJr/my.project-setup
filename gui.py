import sys
import os
from subprocess import Popen, PIPE
import shlex
from pathlib import Path
import platform

import configparser
from glob import glob
import base64
from collections import defaultdict
from PyQt5.QtWidgets import QApplication, QTabWidget, QLabel, QCheckBox, QComboBox, QWidget, QMainWindow, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QSystemTrayIcon
from PyQt5.QtCore import Qt, QSize, QByteArray, pyqtSignal, pyqtSlot
from PyQt5 import QtGui

from draw_items import hslu_icon_large, hslu_icon_small
from setup import setup_maker
from source_structure import source_structure

class QPaxButton(QPushButton):

        def __init__(self, *args, **kwargs):
                super(QPaxButton, self).__init__(*args, **kwargs)
                #self.parent = parent
                #resolution = ScreenInfo.resolution()

                self.setFixedSize( 120, 40 )

class QComboPax(QComboBox):

        def __init__(self, *args, **kwargs):
                super(QComboPax, self).__init__(*args, **kwargs)
                #self.parent = parent
                #resolution = ScreenInfo.resolution()

                self.setStyleSheet("""
                        QComboBox::down-arrow {
                        image: url(PICS/dropdown_arrow.png);
                        width: 14px;
                        height: 14px;
                        }                   
                        """)

class SizePimp(object):

        def launch_decorator(launch):
                def check_exec_type(self,software):
                        cmd = "{}".format(software)
                        executable = os.access(cmd,os.X_OK)

                        if executable:
                                if os.path.isfile(cmd):
                                        if self.app_base in os.path.basename(cmd):
                                                content_path = cmd
                                                launch(content_path)
                                else:
                                        for content in os.listdir(cmd):
                                                content_path = os.path.join(cmd,content)
                                                check_exec_type(self,content_path)                    
                return check_exec_type

        @launch_decorator
        def launch_app(insert):
                print(insert)
                process = Popen(shlex.split(insert), stdout=PIPE)
                #process.communicate()
                #self.exit_code = process.wait()

        def iconFromBase64(self,base64):
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(QByteArray.fromBase64(base64))
                icon = QtGui.QIcon(pixmap)
                return icon

        def imageFromBase64(self,base64):
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(QByteArray.fromBase64(base64))
                return pixmap


        def draw_image(self,image_pic):
                labelImage = QLabel()
                pixmap = QtGui.QPixmap(image_pic)
                pixmap_small = pixmap.scaled(128, 128, Qt.KeepAspectRatio)
                labelImage.setPixmap(pixmap_small)
                pic_layout = QHBoxLayout()
                pic_layout.addWidget(labelImage)
                pic_layout.setAlignment(Qt.AlignCenter)
                return pic_layout


class App(QMainWindow):

        def __init__(self):
                super(App,self).__init__()
                # size definitions
                
                x, y = self.get_resolution()

                if platform.system() == 'Linux':
                        int_x = int(x/8)
                        int_y = int(y/4)
                elif platform.system() == 'MacOS':
                        int_x = int(x/4)
                        int_y = int(y/2)
                else:
                        int_x = int(x/4)
                        int_y = int(y/2)
                
                self.setMinimumWidth(int_x)
                self.setMinimumHeight(int_y)

                if x > 1920 and y > 1080:
                        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
                        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

                else:
                        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, False)
                        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, False)

                #self.resolution = self.screen()
                #self.main_W = int(self.resolution[0] / 3)
                #self.main_H = int(self.resolution.height() / 2)

                sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                self.setSizePolicy(sizePolicy)
                #create a style guide for the layout colors
                self.setStyleSheet(open('stylesheets/hslu_animation.css').read())
                #self.setStyle("plastique")

                self.setWindowTitle('HSLU PROJECT SETUP')

                # The main layout for the window
                #self.main_layout = QVBoxLayout()
                #self.setLayout(self.main_layout)
                #window icon
                hslu_image_icon = SizePimp().iconFromBase64(hslu_icon_large.encode('utf-8'))
                self.setWindowIcon(hslu_image_icon)

                # Create the tray
                self.tray = QSystemTrayIcon()
                self.tray.setIcon(hslu_image_icon)
                self.tray.setVisible(True)

                self.project_manager = ProjectManager(self)
                self.tab_options = ProjectTabs(self)
                self.setMenuWidget(self.project_manager)
                self.setCentralWidget(self.tab_options)

                self.project_manager.project_name_start.connect(self.tab_options.receive_name_from_ProjectManager)
                self.project_manager.project_path_start.connect(self.tab_options.receive_path_from_ProjectManager)

                self.show()

        def get_resolution(self):
                temporary_app = QApplication
                screen = temporary_app.primaryScreen()
                geo = screen.availableGeometry()
                        
                return (geo.width(), geo.height())


class ProjectManager(QWidget):

        project_name_start = pyqtSignal(str)
        project_path_start = pyqtSignal(str)

        def __init__(self, *args, **kwargs):
                super(ProjectManager, self).__init__(*args, **kwargs)
                #self.parent = parent
                #resolution = ScreenInfo.resolution()
                self.initUI()

        def initUI(self):
                self.toolbox = QVBoxLayout()

                self.image_box = QVBoxLayout()
                hslu_image_menu = SizePimp().imageFromBase64(hslu_icon_large.encode('utf-8'))
                #bergli_pic = os.path.join('PICS','bergli_circle.png')
                self.image_box.addLayout(SizePimp().draw_image(hslu_image_menu))
                #self.project_info = QLabel('Project Setup')
                #self.image_box.addWidget(self.project_info)
                ######
                self.toolbox.addLayout(self.image_box)
                ######

                self.project_box = QHBoxLayout()
                self.project_name_label = QLabel('Project Name:')
                self.project_name = QLineEdit('Awesome Project')
                self.project_name.setStyleSheet(
                        """
                        QLineEdit {
                        font-size: 16px;
                        font-weight: bold;
                        color: black;
                        border: 3px solid black;
                        border-radius: 3px;
                        }
                        """
                                                )
                self.project_name.textChanged.connect(self.text_changes)
                
                self.path_btn = QPushButton('PATH')
                self.path_btn.clicked.connect(self.choose_directory)

                self.project_box.addWidget(self.project_name_label)
                self.project_box.addWidget(self.project_name)
                self.project_box.addWidget(self.path_btn)
                ######
                self.toolbox.addLayout(self.project_box)
                ######

                self.path_box = QVBoxLayout()
                
                #self.path_label = QLabel('Project PATH:')
                default_path = Path.home()
                default_text = os.path.join(default_path,'Documents',self.project_name.text())
                self.path_text = QLineEdit(default_text)
                self.path_text.textChanged.connect(self.path_text_change)

                self.text_changes()
                self.path_text_change()
                #self.path_box.addWidget(self.path_label)
                self.path_box.addWidget(self.path_text)
                ######
                self.toolbox.addLayout(self.path_box)
                ######

                self.setLayout(self.toolbox)

        
        def choose_directory(self):
                input_dir = QFileDialog.getExistingDirectory(None, 'Select a folder:', os.path.expanduser("~"))
                entire_path = os.path.join(input_dir,self.project_name.text())
                self.path_text.setText(entire_path)

        def text_changes(self):
                try:
                        proj_name = self.project_name.text()
                        proj_path = os.path.dirname(self.path_text.text())
                        dynamic_path = os.path.join(proj_path,proj_name)
                        self.path_text.setText(dynamic_path)
                        
                        self.project_name_start.emit(self.project_name.text())
                        

                        return proj_name,proj_path

                except OSError as exc:
                        if exc.errno != errno.EEXIST:
                                raise
                        pass
       
        def path_text_change(self):
                self.project_path_start.emit(self.path_text.text())


class ProjectTabs(ProjectManager):

        project_name_end = pyqtSignal(str)
        project_path_end = pyqtSignal(str)

        def __init__(self,parent=None):
                super(ProjectManager, self).__init__(parent)
                #self.parent = parent
                ###get variables###
                self.project_manager = ProjectManager(self)
                self.project_name,self.project_path = ProjectManager(self).text_changes()
                self.initUI()

        def initUI(self):
                
                self.main_tab = QTabWidget()

                ###TEMPLATE TAB###
                self.template_widget = QWidget()
                self.template_box = QVBoxLayout()
                
                ###get template preset types and templates###
                cur_path = os.path.dirname(__file__)
                self.json_template_path = os.path.join(cur_path,'JSON')
                self.template_structure = self.update_templates()
                
                """
                self.template_structure = dict()

                for directory in sorted(os.listdir(self.json_template_path)):
                        directory_path = os.path.join(self.json_template_path,directory)
                        self.template_structure[directory] = []
                        json_list_info = dict()
                        for json_file in sorted(os.listdir(directory_path)):
                                json_file_path = os.path.join(directory_path,json_file)
                                json_list_info[json_file.replace('.json','')] = json_file_path
                        
                        self.template_structure[directory].append(json_list_info)
                """
                #print(template_structure)
                ###create menu###
                self.template_to_call = []
                template_items = []
                self.project_button_list = []

                for (project_type, json_list) in self.template_structure.items():
                        self.button_box = QHBoxLayout()
                        self.project_setup_button = QPaxButton(project_type)

                        self.project_setup_button.setFixedSize( 120, 40 )
                        ###store_data###
                        self.project_button_list.append(self.project_setup_button)
                        self.button_templates = QComboPax()

                        for json_file_list in json_list:
                                self.button_templates.addItems(json_file_list)
                                ###store_data###
                                self.template_to_call.append(self.button_templates)
                                template_items.append(json_file_list)

                        self.button_templates.activated.connect(self.return_cur_json)
                        #self.button_name = self.project_setup_button.text()
                        self.project_setup_button.clicked.connect(self.selected_file)

                        self.button_box.addWidget(self.project_setup_button)
                        self.button_box.addWidget(self.button_templates)
                        self.template_box.addLayout(self.button_box)

                self.template_widget.setLayout(self.template_box)
                self.main_tab.addTab(self.template_widget,'TEMPLATES')


                ###SOURCE PROJECT TAB###
                self.source_widget = QWidget()
                self.source_box = QVBoxLayout()
                self.source_box.addStretch()

                ####source path gui####
                self.source_path_box = QHBoxLayout()
                self.choose_source = QPushButton('Source PATH')
                self.choose_source.clicked.connect(self.choose_source_folder)
                self.source_path = QLineEdit(self.project_path)
                self.source_path_box.addWidget(self.source_path)
                self.source_path_box.addWidget(self.choose_source)
                self.source_box.addLayout(self.source_path_box)

                ####store source as template####
                self.create_template_box = QHBoxLayout()
                self.store_template_button = QPaxButton('Save Template')
                self.store_template_button.clicked.connect(self.save_source_folder)
                self.template_choice = QComboPax()
                self.cur_buttons = []
                for b,x in self.template_structure.items():
                        self.cur_buttons.append(b)
                self.template_choice.addItems(sorted(self.cur_buttons))
                self.create_template_box.addWidget(self.store_template_button)
                self.create_template_box.addWidget(self.template_choice)
                self.source_box.addLayout(self.create_template_box)
                self.source_box.addStretch()
                ####link dependencies to your project#####
                self.info_text_box = QVBoxLayout()
                default_dir = os.path.basename(self.source_path.text())
                self.info_text = QLabel('Collect reusable files from \'{}\' Project'.format(default_dir))
                self.info_text_box.addWidget(self.info_text, alignment=Qt.AlignCenter)
                self.source_box.addLayout(self.info_text_box)

                self.proj_fs_box = QHBoxLayout()
                self.project_from_source_button = QPaxButton('Copy')
                #self.proj_fs_box.setAlignment(Qt.AlignCenter)
                self.proj_fs_box.addWidget(self.project_from_source_button)
                self.source_box.addLayout(self.proj_fs_box)
                self.source_box.addStretch()
                #self.source_path.textChanged.connect(self.choose_source_folder)
                
                ###source widgets###
                self.source_widget.setLayout(self.source_box)
                self.main_tab.addTab(self.source_widget,'SOURCE PROJECT')
                
                ###SETUP TABS###
                self.tab_placement = QHBoxLayout()
                self.tab_placement.addWidget(self.main_tab)
                
                self.setLayout(self.tab_placement)


                ###dummy widgets to get data from ProjectManager###
                self.dummy_name = QLineEdit()
                self.dummy_path = QLineEdit()

        def setup_project(self,json_path,json_name,project_path,project_name):
                setup = setup_maker(json_path)
                return setup.folder_setup(project_name,project_path,json_name)
        
        def return_cur_json(self):
                self.cur_templates_list = []
                for i,template in enumerate(self.template_to_call):
                        if isinstance(template, QComboBox):
                                template_name = template.currentText()
                                self.cur_templates_list.append(template_name)
                #print(self.cur_templates_list)
                return self.cur_templates_list

        @pyqtSlot(str)
        def receive_name_from_ProjectManager(self,message):
                self.dummy_name.setText(message)
                print(message)
                return(message)

        @pyqtSlot(str)
        def receive_path_from_ProjectManager(self,message):
                self.dummy_path.setText(message)
                print(message)
                return(message)

        
        def selected_file(self):
                ###self.sender() is the meat of this function. It avoids lambda and saves memory### 
                button_index = self.project_button_list.index(self.sender())
                ###remaining is peanuts###
                button_name = self.project_button_list[button_index].text()
                selected_file = self.return_cur_json()[button_index]
                selected_file_path = self.template_structure[button_name][0][selected_file]
                selected_file_dir = os.path.dirname(selected_file_path)
                selected_file_format = '{}.json'.format(selected_file)
                #print(button_index)
                #print(button_name)
                #print(selected_file)
                #print(selected_file_path)
                #print(selected_file_dir)
                #print(selected_file_format)
                if self.dummy_name.text() == '':
                        project_output_name = self.project_name
                        #print(project_output_name)
                else:   
                        project_output_name = self.dummy_name.text()
                        #print(project_output_name)
                
                if self.dummy_path.text() == '':
                        project_output_path = self.project_path
                        #print(project_output_path)
                else:   
                        if os.path.isdir(os.path.dirname(self.dummy_path.text())):
                                project_output_path = os.path.dirname(self.dummy_path.text())
                                #print(project_output_path)
                        else:   
                                project_output_path = self.project_path
                                print('Your path is empty creating project in Default')

                return self.setup_project(selected_file_dir,selected_file_format,project_output_path,project_output_name)

                #print(self.dummy_name.text())
                #print(self.dummy_path.text())
                #print(global_project_path)
        
        def choose_source_folder(self):
                input_dir = QFileDialog.getExistingDirectory(None, 'Select a folder:', os.path.expanduser("~"))
                self.source_path.setText(input_dir)
                sel_folder = os.path.basename(input_dir)
                new_info_text = 'Collect reusable files from \'{}\' Project'.format(sel_folder)
                self.info_text.setText(new_info_text)

        def save_source_folder(self):
                if self.dummy_name.text() == '':
                        project_output_name = self.project_name
                        #print(project_output_name)
                else:   
                        project_output_name = self.dummy_name.text()
                        #print(project_output_name)
                
                source_project = source_structure(project_output_name)
                data = source_project.check_folder(self.source_path.text())
                save_to = self.template_choice.currentText()
                
                save_to_dir = os.path.join(self.json_template_path,save_to)
                #print(save_to_dir)
                source_project.write_a_structure(save_to_dir,data)

                current_templates = self.update_templates()

                """
                if project_output_name not in self.return_cur_json():
                        self.button_templates.addItem(project_output_name)
                """


        def update_templates(self):

                template_structure = dict()

                for directory in sorted(os.listdir(self.json_template_path)):
                        directory_path = os.path.join(self.json_template_path,directory)
                        template_structure[directory] = []
                        json_list_info = dict()
                        for json_file in sorted(os.listdir(directory_path)):
                                json_file_path = os.path.join(directory_path,json_file)
                                json_list_info[json_file.replace('.json','')] = json_file_path
                        
                        template_structure[directory].append(json_list_info)

                return template_structure



def main():         
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
        main()
