from PyQt5 import QtWidgets, uic, QtGui
import os
import os.path, time
import datetime
from pathlib import Path
from pydub import AudioSegment
import scipy.signal
from scipy.io import wavfile
import numpy as np
#from main2 import MainWindow

ui = "resources/open.ui"

"""
    Class : openWindow
    - File>Open 실행 시 띄워지는 Dialog Class
"""
class openWindow(QtWidgets.QDialog):
    def __init__(self, mw):
        super().__init__()
        #Load the UI Page
        uic.loadUi(ui, self)

        self.mw = mw
        self.openFilename=""

        self.BrowseButton.clicked.connect(self.btn_BrowseButton)
        self.openButton.clicked.connect(self.btn_openButton)
        self.closeButton.clicked.connect(self.btn_closeButton)


    # event
    def btn_openButton(self):
        self.fileLabel.text()
        #MainWindow.loadInit(self.fileLabel.text())
        self.mw.loadInit(self.fileLabel.text())
        self.close()

    def btn_closeButton(self):
        self.close()

    def btn_BrowseButton(self):
        #dname = QtWidgets.QFileDialog.getExistingDirectory(self)
        fname = QtWidgets.QFileDialog.getOpenFileName(self)
        self.fileLabel.setText(fname[0])





