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
from PyQt5.QtCore import Qt, QSize, QByteArray
from PyQt5 import QtGui

from draw_items import hslu_icon_large, hslu_icon_small
from setup import setup_maker



class SizePimp(QWidget):
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

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
                super().__init__()
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

                self.show()

        def get_resolution(self):
                temporary_app = QApplication
                screen = temporary_app.primaryScreen()
                geo = screen.availableGeometry()
                        
                return (geo.width(), geo.height())
      
class ProjectManager(QWidget):

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

                except OSError as exc:
                        if exc.errno != errno.EEXIST:
                                raise
                        pass


class ProjectTabs(QWidget):

        def __init__(self, *args, **kwargs):
                super(ProjectTabs, self).__init__(*args, **kwargs)
                #self.parent = parent
                #resolution = ScreenInfo.resolution()
                self.initUI()

        def initUI(self):
                
                self.main_tab = QTabWidget()

                ###TEMPLATE TAB###
                self.template_widget = QWidget()
                self.template_box = QVBoxLayout()
                
                cur_path = os.path.dirname(__file__)
                json_template_path = os.path.join(cur_path,'JSON')
                template_structure = dict()

                for directory in sorted(os.listdir(json_template_path)):
                        directory_path = os.path.join(json_template_path,directory)
                        template_structure[directory] = []
                        json_list_info = dict()
                        for json_file in sorted(os.listdir(directory_path)):
                                json_file_path = os.path.join(directory_path,json_file)
                                json_list_info[json_file.replace('.json','')] = json_file_path
                        
                        template_structure[directory].append(json_list_info)

                print(template_structure)

                for project_type, json_list in template_structure.items():
                        self.button_box = QHBoxLayout()
                        self.project_setup_button = QPushButton(project_type)
                        self.project_setup_button.setFixedSize( 120, 40 )

                        self.button_templates = QComboBox()
                        self.button_templates.setStyleSheet("""
                        QComboBox::down-arrow {
                        image: url(PICS/dropdown_arrow.png);
                        width: 14px;
                        height: 14px;
                        }                   
                        """)
                        for i,content in enumerate(json_list):
                                self.button_templates.addItems(json_list[i])
                        #self.cancel_btn.clicked.connect(self.close)
                        self.button_box.addWidget(self.project_setup_button)
                        self.button_box.addWidget(self.button_templates)
                        self.template_box.addLayout(self.button_box)

                self.template_widget.setLayout(self.template_box)
                self.main_tab.addTab(self.template_widget,'TEMPLATES')

                ###SOURCE PROJECT###
                self.source_widget = QWidget()
                self.source_box = QVBoxLayout()

                self.source_widget.setLayout(self.source_box)
                self.main_tab.addTab(self.source_widget,'SOURCE PROJECT')

                ###SETUP TABS###s
                self.tab_placement = QHBoxLayout()
                self.tab_placement.addWidget(self.main_tab)
                
                self.setLayout(self.tab_placement)


def main():         
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
        main()
