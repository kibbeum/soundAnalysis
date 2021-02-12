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

from pydub import AudioSegment, playback
import audioplayer
import pygame

import matplotlib.animation as animation

import concatWindow as cw
import splitWindow as sw
import openWindow as ow

from scipy.io import wavfile


import mplwidget

# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

"""
#audio_filename = "C:/test2/split2.mp3"
#audio_filename = "C:/test2/splitWithFilter.wav"
#audio_filename = "resources/Myotis ikonnikovi.WAV"
audio_filename = "resources/죽전동 맹꽁이 한마리 2020_07_22_16_16_31.mp3"
audio_y, audio_sr = librosa.load(audio_filename, sr=None)
#sw_sr, sw_y = wavfile.read(audio_filename)
"""


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
        ui = "resources/main.ui"
        uic.loadUi(ui, self)

        self.spectrumWidget.myInit(self)


        """
        self.spectrumWidgetPlot(self.spectrumWidget.canvas)
        #self.signalWidgetPlot(self.signalWidget.canvas)
        audio = AudioSegment.from_file(audio_filename, os.path.splitext(audio_filename)[1][1:])
        #audio.export("mashup.mp3", format="mp3")
        self.player = audioplayer.AudioPlayer(audio_filename)
        """


        self.actionPlay.triggered.connect(self.btn_clicked_actionPlay)
        self.actionStop.triggered.connect(self.btn_clicked_actionStop)
        self.actionPos.triggered.connect(self.btn_clicked_actionPos)

        self.actionConcat_files.triggered.connect(self.btn_clicked_actionConcat_files)
        self.actionSplit_files.triggered.connect(self.btn_clicked_actionSplit_files)

        self.actionOpen.triggered.connect(self.btn_clicked_actionOpen)

        self.zoomInXButton.clicked.connect(self.btn_clicked_zoomInXButton)
        self.zoomOutXButton.clicked.connect(self.btn_clicked_zoomOutXButton)
        self.zoomInYButton.clicked.connect(self.btn_clicked_zoomInYButton)
        self.zoomOutYButton.clicked.connect(self.btn_clicked_zoomOutYButton)


        """
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(audio_filename)
        """

        #self.aniTest()




    # Sound sources: Jon Fincher
    #move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
    #move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
    #collision_sound = pygame.mixer.Sound("Collision.ogg")
    #move_up_sound.play()

    def loadInit(self, filename):
        ## from the top
        # audio_filename = "C:/test2/split2.mp3"
        # audio_filename = "C:/test2/splitWithFilter.wav"
        # audio_filename = "resources/Myotis ikonnikovi.WAV"
        #self.audio_filename = "resources/죽전동 맹꽁이 한마리 2020_07_22_16_16_31.mp3"
        #audio_y, audio_sr = librosa.load(audio_filename, sr=None)
        # sw_sr, sw_y = wavfile.read(audio_filename)

        self.audio_filename = filename
        self.audio_y, self.audio_sr = librosa.load(filename, sr=None)

        ## from the init
        self.spectrumWidgetPlot(self.spectrumWidget.canvas, self.audio_y, self.audio_sr)
        # self.signalWidgetPlot(self.signalWidget.canvas, self.audio_y, self.audio_sr)
        audio = AudioSegment.from_file(filename, os.path.splitext(filename)[1][1:])

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(filename)





    def update_line(self, num, line):
        i = self.X_VALS[num]
        line.set_data([i, i], [self.Y_MIN, self.Y_MAX])
        return line,

    def aniTest(self):
        self.X_MIN = 0
        #self.X_MAX = np.shape(self.audio_y)[0]/self.audio_sr*1000
        self.X_MAX = 500
        self.Y_MIN = -0.5
        #self.Y_MAX = np.max()
        self.Y_MAX = 0.5
        self.X_VALS = range(self.X_MIN, self.X_MAX + 1)  # possible x values for the line
        self.l,  = self.spectrumWidget.canvas.ax1.plot(0, 0,  linewidth=2, color='red')
        self.line_anim = animation.FuncAnimation(self.spectrumWidget.canvas.fig, self.update_line, len(self.X_VALS), fargs=(self.l,))
        #anim = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=20, blit=True)


    def btn_clicked_zoomInXButton(self):
        w, h = self.spectrumWidget.canvas.fig.get_size_inches()
        self.spectrumWidget.canvas.fig.set_size_inches(w+3, h)
        self.spectrumWidgetPlot(self.spectrumWidget.canvas, self.audio_y, self.audio_sr)

    def btn_clicked_zoomOutXButton(self):
        w, h = self.spectrumWidget.canvas.fig.get_size_inches()
        self.spectrumWidget.canvas.fig.set_size_inches(w-3, h)
        self.spectrumWidgetPlot(self.spectrumWidget.canvas, self.audio_y, self.audio_sr)

    def btn_clicked_zoomInYButton(self):
        w, h = self.spectrumWidget.canvas.fig.get_size_inches()
        self.spectrumWidget.canvas.fig.set_size_inches(w, h+3)
        self.spectrumWidgetPlot(self.spectrumWidget.canvas, self.audio_y, self.audio_sr)

    def btn_clicked_zoomOutYButton(self):
        w, h = self.spectrumWidget.canvas.fig.get_size_inches()
        self.spectrumWidget.canvas.fig.set_size_inches(w, h-3)
        self.spectrumWidgetPlot(self.spectrumWidget.canvas, self.audio_y, self.audio_sr)

    def btn_clicked_actionOpen(self):
        openWin = ow.openWindow(self)
        openWin.exec_()

    def btn_clicked_actionConcat_files(self):
        concatWin = cw.concatWindow()
        concatWin.exec_()

    def btn_clicked_actionSplit_files(self):
        splitWin = sw.splitWindow(self.audio_filename, self.spectrumWidget.whichEventAx, self.spectrumWidget.rectStartX, self.spectrumWidget.rectEndX, self.spectrumWidget.rectStartY, self.spectrumWidget.rectEndY)
        splitWin.exec_()


    def btn_clicked_actionPlay(self):
        if(self.actionPlay.text()=="Play"):
            self.actionPlay.setText("Pause")
            if(pygame.mixer.music.get_pos()==-1):
                print("play")
                pygame.mixer.music.play()
            else:
                print("play")
                pygame.mixer.music.unpause()
        else:
            print("pause")
            pygame.mixer.music.pause()
            self.actionPlay.setText("Play")


    def btn_clicked_actionStop(self):
        print("stop")
        pygame.mixer.music.stop()
        self.actionPlay.setText("Play")

    def btn_clicked_actionPos(self):
        print("pos")
        print(pygame.mixer.music.get_pos())


    def spectrumWidgetPlot(self, canvas, audio_y, audio_sr):
        canvas.ax1.cla()
        canvas.ax2.cla()
        self.spectrumWidget.audio_sr = audio_sr
        self.spectrumWidget.audio_y = audio_y

        #print(np.max(audio_y))
        #print(np.min(audio_y))
        #waveform graph
        librosa.display.waveplot(audio_y, sr=audio_sr, ax=canvas.ax1)
        #canvas.ax1.plot(sw_y)
        #audio_x = np.linspace(0, len(audio_y) / audio_sr, num=len(audio_y))
        #canvas.ax1.plot(audio_x, audio_y)


        #spectrum graph
        S = np.abs(librosa.stft(audio_y))
        self.spectrumWidget.spectrum = amplitude = librosa.amplitude_to_db(S, ref=np.max)
        #img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=canvas.ax)
        librosa.display.specshow(amplitude, y_axis='linear', x_axis='s', ax=canvas.ax2, sr=audio_sr)
        #librosa.display.specshow(amplitude, y_axis='linear', x_axis='s', ax=canvas.ax2, sr=audio_sr, cmap='Greys')
        #canvas.ax2.set_title('Power spectrogram')
        #canvas.fig.colorbar(img, ax=canvas.ax2, format="%+2.0f dB")

        canvas.fig.canvas.draw()



    def signalWidgetPlot(self, canvas, audio_y, audio_sr):
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





