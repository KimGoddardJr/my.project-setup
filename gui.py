import sys
import os
from subprocess import Popen, PIPE
import shlex
from pathlib import Path

import configparser
from glob import glob
import base64
from collections import defaultdict
from PyQt5.QtWidgets import QApplication, QTabWidget, QLabel, QCheckBox, QComboBox, QWidget, QMainWindow, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt, QSize, QByteArray
from PyQt5 import QtGui

from draw_items import hslu_icon_large
from setup import setup_maker
import darkorange



class SizePimp(QWidget):
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                self.resolution = QApplication.desktop().availableGeometry()
                self.main_W = int(self.resolution.width() / 4)
                self.main_H = int(self.resolution.height() / 2)

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
                #unit = resolution.width()/1920
                #checkbox_constant = int(math.ceil(float(resolution.width())/float(unit*160.0)))
                #stylesheet = hou.qt.styleSheet()
                #checkbox_stylesheet = "QListWidget::indicator {0} width: {1}px; height: {1}px;{2}".format("{",checkbox_constant,"}")

                self.setMinimumWidth(SizePimp().main_W)
                self.setMinimumHeight(SizePimp().main_H)
                sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                self.setSizePolicy(sizePolicy)
                #create a style guide for the layout colors
                #self.setStyleSheet(darkorange.getStyleSheet())
                #self.setStyle("plastique")
                self.setWindowTitle('HSLU PROJECT SETUP')

                # The main layout for the window
                self.main_layout = QVBoxLayout()
                self.setLayout(self.main_layout)
                #window icon
                base64_bytes = hslu_icon_large.encode('utf-8')
                #message_bytes = base64.decodebytes(base64_bytes)
                #message = message_bytes.decodebytes('utf-8')
                self.setWindowIcon(SizePimp().iconFromBase64(base64_bytes))
                
                self.project_manager = ProjectManager(self)
                self.setMenuWidget(self.project_manager)

                """
                self.shit_window = ShitWindow(self)
                self.save_window = SavePrefs(self)
                self.pipeline_manager = PipelineManager(self)
                self.setMenuWidget(self.shit_window)
                self.setCentralWidget(self.save_window)
                """
                self.show()
      
class ProjectManager(QWidget):

        def __init__(self, *args, **kwargs):
                super(ProjectManager, self).__init__(*args, **kwargs)
                #self.parent = parent
                #resolution = ScreenInfo.resolution()
                self.initUI()

        def initUI(self):

                self.toolbox = QVBoxLayout()
                
                self.image_box = QVBoxLayout()
                hslu_image = SizePimp().imageFromBase64(hslu_icon_large.encode('utf-8'))
                bergli_pic = os.path.join('PICS','bergli_circle.png')
                self.image_box.addLayout(SizePimp().draw_image(bergli_pic))
                #self.project_info = QLabel('Project Setup')
                #self.image_box.addWidget(self.project_info)
                ######
                self.toolbox.addLayout(self.image_box)
                ######

                self.project_box = QHBoxLayout()
                self.project_name_label = QLabel('Project Name')
                self.project_name = QLineEdit('Awesome Project')
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
                
                self.path_label = QLabel('Project PATH')
                default_path = Path.home()
                default_text = os.path.join(default_path,'Documents',self.project_name.text())
                self.path_text = QLineEdit(default_text)

                self.path_box.addWidget(self.path_label)
                self.path_box.addWidget(self.path_text)
                ######
                self.toolbox.addLayout(self.path_box)
                ######

                setup_type = ['CGI Short','Stop Motion','2D Animation','Mixed Media']

                for project_type in setup_type:
                        self.project_setup_button = QPushButton(project_type)
                        #self.cancel_btn.clicked.connect(self.close)
                        self.toolbox.addWidget(self.project_setup_button)

                #self.pipeline_picker = QComboBox()
                #self.pipeline_picker.addItems(chose)
                #self.toolbox.addWidget(self.pipeline_picker)
                
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


def main():         
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
        main()
