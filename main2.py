from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import os

import matplotlib
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

import mplwidget

# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('C:/projects/SoundAnalysis/ui.ui', self)


        self.spectrumWidgetPlot(self.spectrumWidget.canvas)
        self.signalWidgetPlot(self.signalWidget.canvas)


    def spectrumWidgetPlot(self, canvas):
        #y, sr = librosa.load("resources/bat.wav")
        #y, sr = librosa.load("resources/bat.wav", sr=None)
        y, sr = librosa.load("resources/Myotis ikonnikovi.WAV", sr=None)


        S = np.abs(librosa.stft(y))
        #img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=canvas.ax)
        img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='s', ax=canvas.ax, sr=sr)


        canvas.ax.set_title('Power spectrogram')
        canvas.fig.colorbar(img, ax=canvas.ax, format="%+2.0f dB")
        #canvas.ax.set_ylim(9750)



    def signalWidgetPlot(self, canvas):
        y, sr = librosa.load("resources/bat.wav")
        S = np.abs(librosa.stft(y))
        #S_left = librosa.stft(y, center=False)
        #D_short = librosa.stft(y, hop_length=64)
        canvas.ax.plot(y)
        #img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=canvas.ax)
        #canvas.ax.set_title('Power spectrogram')
        #canvas.fig.colorbar(img, ax=canvas.ax, format="%+2.0f dB")


"""
    def mouseMoveEvent(self, event):
        txt = "Mouse 위치 ; x={0},y={1}, global={2},{3}".format(event.x(), event.y(), event.globalX(), event.globalY())
        #self.statusbar.showMessage(txt)
        print(txt)
"""




"""
        self.plot([1,2,3,4,5,6,7,8,9,10], [1,4,9,16,25,36,49,64,81,100])
    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)
"""


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()





