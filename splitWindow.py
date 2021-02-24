from PyQt5 import QtWidgets, uic, QtGui
import os
import os.path, time
import datetime
from pathlib import Path
from pydub import AudioSegment
import scipy.signal
from scipy.io import wavfile
import numpy as np

ui = "resources/split.ui"


class splitWindow(QtWidgets.QDialog):
    def __init__(self, audioFilename, ax_info, minX, maxX, minY, maxY):
        super().__init__()
        #Load the UI Page
        uic.loadUi(ui, self)

        self.BrowseButton.clicked.connect(self.btn_BrowseButton)
        self.splitButton.clicked.connect(self.btn_splitButton)
        self.closeButton.clicked.connect(self.btn_closeButton)

        self.audioFilename = audioFilename
        self.ax_info = ax_info
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

        print("ax_info %s" % ax_info)
        print("X %s, %s" % (self.minX, self.maxX))
        print("Y %s, %s" % (self.minY, self.maxY))


    def btn_splitButton(self):
        outputFilename = self.outputFilenameLabel.text()
        dpath = self.directoryLabel.text()

        if bool(outputFilename.strip()):
            if self.ax_info=="ax1":
                audio = AudioSegment.from_file(self.audioFilename, os.path.splitext(self.audioFilename)[1][1:])
                splitAudio = audio[int(self.minX*1000):int(self.maxX*1000)]

                filename = dpath + os.path.sep + outputFilename + "." + self.concatTypeComboBox.currentText()
                print("outputname: %s, extension: %s" % (filename, self.concatTypeComboBox.currentText()))
                splitAudio.export(filename, format=self.concatTypeComboBox.currentText())

            elif self.ax_info=="ax2":
                #scipy.signal.filtfilt -> scipy.io.wirte

                filename = dpath + os.path.sep + outputFilename + "." + self.concatTypeComboBox.currentText()

                """
                if os.path.splitext(self.audioFilename)[1][1:] != "wav":
                    audio = AudioSegment.from_file(self.audioFilename, os.path.splitext(self.audioFilename)[1][1:])
                    print("outputname: %s, extension: %s" % (filename, self.concatTypeComboBox.currentText()))
                    audio.export(filename + ".tmp", format=self.concatTypeComboBox.currentText())
                """

                sr, data = wavfile.read(self.audioFilename)
                print(data.shape)
                print(int(self.minX * sr), int(self.maxX * sr))
                filterdData = self.butter_bandpass_filter(data[int(self.minX*sr):int(self.maxX*sr)], int(self.minY), int(self.maxY), sr, order=5)
                wavfile.write(filename, sr, filterdData.astype(np.int16))





                print("completed")

                #wavfile.write()


            else:
                print("error")
        else:
            print("error")

        self.close()

    def btn_closeButton(self):
        self.close()

    def btn_BrowseButton(self):
        dname = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.directoryLabel.setText(dname)


    def butter_bandpass(self, lowcut, higcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = higcut / nyq
        b, a = scipy.signal.butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, data, lowcut, higcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, higcut, fs, order=order)
        #y = scipy.signal.lfilter(b, a, data)
        y = scipy.signal.filtfilt(b, a, data)
        return y



