from PyQt5 import QtWidgets, uic, QtGui
import os
import os.path, time
import datetime
from pathlib import Path
from pydub import AudioSegment

ui = "resources/split.ui"


class splitWindow(QtWidgets.QDialog):
    def __init__(self, ax_info, startX, endX, startY, endY):
        super().__init__()
        #Load the UI Page
        uic.loadUi(ui, self)

        self.BrowseButton.clicked.connect(self.btn_BrowseButton)
        self.splitButton.clicked.connect(self.btn_splitButton)
        self.closeButton.clicked.connect(self.btn_closeButton)


        self.concatList = []
        self.concatPath = ""

        print("ax_info %s" % ax_info)
        print("X %s, %s" % (startX, endX))
        print("Y %s, %s" % (startY, endY))


    def btn_splitButton(self):
        outputFilename = self.outputFilenameLabel.text()

        if bool(outputFilename.strip()):
            audioSegList = []
            for file in self.concatList:
                audioSegList.append(AudioSegment.from_file(file, os.path.splitext(file)[1][1:]))

            combined = AudioSegment.empty()
            for song in audioSegList:
                combined += song

            filename = self.concatPath + os.path.sep + outputFilename + "." + self.concatTypeComboBox.currentText()
            print("outputname: %s, extension: %s" % (filename, self.concatTypeComboBox.currentText()))
            combined.export(filename, format=self.concatTypeComboBox.currentText())
        else:
            print("error")

    def btn_closeButton(self):
        self.close()

    def btn_BrowseButton(self):
        dname = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.directoryLabel.setText(dname)


