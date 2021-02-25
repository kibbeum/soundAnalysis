from PyQt5 import QtWidgets, uic, QtGui
import os
import os.path, time
import datetime
from pathlib import Path
from pydub import AudioSegment

ui = "resources/concat.ui"

sound_extension_list = ["wav", "mp3", "m4a", "flac", "mp4", "wma", "aac"]


"""
    Class : concatWindow
    - Edit>Concat Files 선택 시 띄워지는 Dialog Class
"""
class concatWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        #Load the UI Page
        uic.loadUi(ui, self)

        # event
        self.BrowseButton.clicked.connect(self.btn_BrowseButton)
        self.PreviewButton.clicked.connect(self.btn_PreviewButton)
        self.concatButton.clicked.connect(self.btn_concatButton)
        self.closeButton.clicked.connect(self.btn_closeButton)

        self.tableWidget.setHorizontalHeaderLabels(["filename", "modified time", "size"])

        self.concatButton.setEnabled(False)

        self.concatList = []
        self.concatPath = ""

    # event handler
    def btn_concatButton(self):
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

        self.close()

    def btn_closeButton(self):
        self.close()

    def btn_BrowseButton(self):
        dname = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.directoryLabel.setText(dname)

    def btn_PreviewButton(self):
        dpath = self.directoryLabel.text()
        self.tableWidget.setRowCount(0)

        if os.path.exists(dpath) and os.path.isdir(dpath):
            self.concatButton.setEnabled(True)
            sort_key = self.SortComboBox.currentText()
            files = os.listdir(dpath)
            audio_list = []

            if(sort_key == "filename"):
                files.sort()
                #print(files)
            else:
                files_fullpath = [dpath + os.path.sep + s for s in files]
                files_fullpath.sort(key=os.path.getmtime)
                files = [os.path.basename(s) for s in files_fullpath]
                #print(files)

            rp = 0
            for f in files:
                fullpath = dpath + os.path.sep + f
                if (os.path.isfile(fullpath) and os.path.splitext(f)[1][1:].lower() in sound_extension_list):
                    #mtime = time.ctime(os.path.getmtime(fullpath))
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fullpath)).strftime('%Y-%m-%d %H:%M:%S')
                    size = os.path.getsize(fullpath)
                    #print("filename: %s, modified time: %s, size: %s" % (f,mtime, size))
                    self.tableWidget.insertRow(rp)
                    self.tableWidget.setItem(rp, 0, QtGui.QTableWidgetItem(str(f)))
                    self.tableWidget.setItem(rp, 1, QtGui.QTableWidgetItem(str(mtime)))
                    self.tableWidget.setItem(rp, 2, QtGui.QTableWidgetItem(str(size)))
                    rp = rp + 1
                    audio_list.append(fullpath)


            if (self.tableWidget.rowCount()==0):
                self.concatButton.setEnabled(False)
            else:
                self.concatPath = dpath
                self.concatList = audio_list
        else:
            print("error")


