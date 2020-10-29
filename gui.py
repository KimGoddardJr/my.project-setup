import sys
import os
from subprocess import Popen, PIPE
import shlex

import configparser
from glob import glob
import base64
from collections import defaultdict
from PyQt5.QtWidgets import QApplication, QTabWidget, QLabel, QCheckBox, QComboBox, QWidget, QMainWindow, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QSize, QByteArray
from PyQt5 import QtGui

from draw_items import davinci_human


class SizePimp(QWidget):
        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                self.resolution = QApplication.desktop().availableGeometry()
                self.main_W = self.resolution.width() / 4
                self.main_H = self.resolution.height() / 2

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
                pixmap_small = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
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
                #self.setStyleSheet(stylesheet)
                self.setWindowTitle('DIGITAL HUMAN SETUP')
                # The main layout for the window
                self.main_layout = QVBoxLayout()
                self.setLayout(self.main_layout)
                #window icon
                base64_bytes = davinci_human.encode('utf-8')
                #message_bytes = base64.decodebytes(base64_bytes)
                #message = message_bytes.decodebytes('utf-8')
                self.setWindowIcon(SizePimp().iconFromBase64(base64_bytes))
                
                """
                self.shit_window = ShitWindow(self)
                self.save_window = SavePrefs(self)
                #self.pipeline_manager = PipelineManager(self)
                self.setMenuWidget(self.shit_window)
                self.setCentralWidget(self.save_window)
                """
                self.show()


if __name__ == '__main__':
        
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
