from PyQt5 import QtWidgets, uic, QtGui
import os
import os.path, time
import datetime

ui = "resources/concat.ui"

class concatWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        #Load the UI Page
        uic.loadUi(ui, self)

        self.BrowseButton.clicked.connect(self.btn_BrowseButton)
        self.PreviewButton.clicked.connect(self.btn_PreviewButton)

        self.tableWidget.setHorizontalHeaderLabels(["filename", "modified time", "size"])



    def btn_BrowseButton(self):
        print("123")
        dname = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.directoryLabel.setText(dname)
        print(dname)

    def btn_PreviewButton(self):
        print("456")
        sort_key = self.SortComboBox.currentText()

        if(sort_key == "filename"):
            dpath = self.directoryLabel.text()
            files = os.listdir(dpath)
            print(files)
            rp = 0
            for f in files:
                fullpath = dpath + "/" + f
                if(os.path.isfile(fullpath)):
                    #print("filename: %s, modified time: %s" % (f, time.ctime(os.path.getmtime(fullpath))))
                    mtime = datetime.datetime.fromtimestamp(os.stat(fullpath).st_mtime)
                    size = os.stat(fullpath).st_size
                    print("filename: %s, modified time: %s, size: %s" % (f, mtime, size))
                    self.tableWidget.insertRow(rp)
                    self.tableWidget.setItem(rp, 0, QtGui.QTableWidgetItem(str(f)))
                    self.tableWidget.setItem(rp, 1, QtGui.QTableWidgetItem(str(mtime)))
                    self.tableWidget.setItem(rp, 2, QtGui.QTableWidgetItem(str(size)))
                    rp = rp + 1
