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

audio_filename = "resources/Myotis ikonnikovi.WAV"
audio_y, audio_sr = librosa.load(audio_filename, sr=None)




"""
plt.subplot(211)
plt.title('Spectrogram')
librosa.display.specshow(stft_db, x_axis='time', y_axis='log')

plt.subplot(212)
plt.title('Audioform')
librosa.display.waveplot(y, sr=sr)
"""


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('C:/projects/SoundAnalysis/ui.ui', self)

        self.spectrumWidgetPlot(self.spectrumWidget.canvas)
        #self.signalWidgetPlot(self.signalWidget.canvas)


    def spectrumWidgetPlot(self, canvas):
        self.spectrumWidget.audio_sr = audio_sr
        self.spectrumWidget.audio_y = audio_y

        #waveform graph
        librosa.display.waveplot(audio_y, sr=audio_sr, ax=canvas.ax1)
        #audio_x = np.linspace(0, len(audio_y) / audio_sr, num=len(audio_y))
        #canvas.ax1.plot(audio_x, audio_y)


        #spectrum graph
        S = np.abs(librosa.stft(audio_y))
        self.spectrumWidget.spectrum = amplitude = librosa.amplitude_to_db(S, ref=np.max)
        #img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=canvas.ax)
        librosa.display.specshow(amplitude, y_axis='linear', x_axis='s', ax=canvas.ax2, sr=audio_sr)
        #canvas.ax2.set_title('Power spectrogram')
        #canvas.fig.colorbar(img, ax=canvas.ax2, format="%+2.0f dB")



    def signalWidgetPlot(self, canvas):
        librosa.display.waveplot(audio_y, sr=audio_sr)
        audio_x = np.linspace(0, len(audio_y) / audio_sr, num=len(audio_y))
        canvas.ax.plot(audio_x, audio_y)
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





