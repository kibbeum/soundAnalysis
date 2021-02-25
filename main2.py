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
import threading
from scipy.io import wavfile
import mplwidget

# Ensure using PyQt5 backend
#matplotlib.use('QT5Agg')
matplotlib.style.use('fast')

"""
    Class : MainWindow 
    - 첫 ui화면
"""
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        ui = "resources/main.ui"
        uic.loadUi(ui, self)

        # matplot plot speed up
        matplotlib.rcParams['path.simplify'] = True
        matplotlib.rcParams['path.simplify_threshold'] = 1.0
        matplotlib.rcParams['agg.path.chunksize'] = 10000

        # init
        self.menuspectrogram_color_init()
        self.menuspectrogram_type_init()
        self.spectrumWidget.myInit(self)

        # event
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

    """
        func : loadInit 
        - File>Open하여 파일을 불러올 때 실행
    """
    def loadInit(self, filename):

        # pygame quit
        pygame.quit()

        # generate tmp files for play audio and split file
        audio = AudioSegment.from_file(filename, os.path.splitext(filename)[1][1:])
        audio_path = "resources/tmp.mp3"
        if os.path.exists(audio_path):
            os.remove(audio_path)
        audio.export(audio_path, format="mp3")

        signal = AudioSegment.from_file(filename, os.path.splitext(filename)[1][1:])
        signal_path = "resources/tmp.wav"
        if os.path.exists(signal_path):
            os.remove(signal_path)
        signal.export(signal_path, format="wav")
        self.signal_filename = signal_path

        self.audio_filename = filename
        # extract audio raw and sr
        self.audio_y, self.audio_sr = librosa.load(filename, sr=None)

        # init animation
        if hasattr(self, 'line_anim'):
            self.line_anim=None

        self.aniTest(self.audio_sr, self.audio_y )
        self.line_anim.event_source.stop()

        # plot spectrum
        self.spectrumWidgetPlot(self.spectrumWidget.canvas, self.audio_y, self.audio_sr)

        # init pygame for audio
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        self.pos_init()


    """
        func : menuspectrogram_color_init
        - init spectrogram color 
    """
    def menuspectrogram_color_init(self):
        self.spectrum_color_group = QtWidgets.QActionGroup(self.menuspectrogram_color)
        texts = ["magma", "Greys"]
        for text in texts:
            action = QtWidgets.QAction(text, self.menuspectrogram_color, checkable=True, checked=text == texts[0])
            self.menuspectrogram_color.addAction(action)
            self.spectrum_color_group.addAction(action)
        self.spectrum_color_group.setExclusive(True)
        self.spectrum_color_group.triggered.connect(self.btn_clicked_menuspectrogram_color)
        self.spectrum_color = texts[0]

    """
        func : menuspectrogram_type_init
        - init spectrogram type
    """
    def menuspectrogram_type_init(self):
        self.spectrum_type_group = QtWidgets.QActionGroup(self.menuspectrogram_type)
        texts = ["linear", "log", "mel", "cqt_hz", "cqt_note"]
        for text in texts:
            action = QtWidgets.QAction(text, self.menuspectrogram_type, checkable=True, checked=text == texts[0])
            self.menuspectrogram_type.addAction(action)
            self.spectrum_type_group.addAction(action)
        self.spectrum_type_group.setExclusive(True)
        self.spectrum_type_group.triggered.connect(self.btn_clicked_menuspectrogram_type)
        self.spectrum_type = texts[0]


    """
        func : pos_init
        - init audio play position
    """
    def pos_init(self):
        self.pos_start = 0
        self.pos_end = np.shape(self.audio_y)[0]/self.audio_sr
        #print(self.pos_start, self.pos_end)


    """
        func : update_line2
        - line update if you're playing audio
    """
    def update_line2(self, num, vl, vl2, period):
        #t = num * period / 1000
        if pygame.mixer.get_init() and pygame.mixer.music.get_pos()!=-1:
            #vl.set_xdata([pygame.mixer.music.get_pos(), pygame.mixer.music.get_pos()])
            index = pygame.mixer.music.get_pos() / 1000.0 +self.pos_start
            vl.set_xdata([index, index])
            vl2.set_xdata([index, index])

            if self.pos_end < index:
                self.btn_clicked_actionStop()
        else:
            self.line_anim.event_source.stop()

        return vl, vl2

    """
        func : aniTest
        - init line update animation
    """
    def aniTest(self, audio_sr, audio_y):
        refreshPeriod = 100  # in ms
        self.X_MIN = 0
        self.X_MAX = int(np.shape(self.audio_y)[0]/self.audio_sr)
        self.Y_MIN = -1.0
        self.Y_MAX = 1.0
        self.X_VALS = range(self.X_MIN, self.X_MAX + 1)  # possible x values for the line
        #self.l, v  = self.spectrumWidget.canvas.ax1.plot(0, 0, 0, 0,  linewidth=2, color='red')
        vl = self.spectrumWidget.canvas.ax1.axvline(0, ls='-', color='r', lw=1, zorder=10)
        vl2 = self.spectrumWidget.canvas.ax2.axvline(0, ls='-', color='r', lw=1, zorder=10)
        self.line_anim = animation.FuncAnimation(self.spectrumWidget.canvas.fig, self.update_line2,
                                                 fargs=(vl, vl2, refreshPeriod), interval=refreshPeriod, blit=True)
        self.line_anim.event_source.stop()


    """
        event handler
    """
    def btn_clicked_menuspectrogram_color(self, action):
        self.spectrum_color = action.text()
        self.spectrumWidgetPlot(self.spectrumWidget.canvas, self.audio_y, self.audio_sr)

    def btn_clicked_menuspectrogram_type(self, action):
        self.spectrum_type = action.text()
        self.spectrumWidgetPlot(self.spectrumWidget.canvas, self.audio_y, self.audio_sr)

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
        #splitWin = sw.splitWindow(self.audio_filename, self.spectrumWidget.whichEventAx, self.spectrumWidget.rectMinX, self.spectrumWidget.rectMaxX, self.spectrumWidget.rectMinY, self.spectrumWidget.rectMaxY)
        splitWin = sw.splitWindow(self.signal_filename, self.spectrumWidget.whichEventAx, self.spectrumWidget.rectMinX,
                                  self.spectrumWidget.rectMaxX, self.spectrumWidget.rectMinY,
                                  self.spectrumWidget.rectMaxY)
        splitWin.exec_()


    def btn_clicked_actionPlay(self):
        if(self.actionPlay.text()=="Play"):
            self.actionPlay.setText("Pause")
            if(pygame.mixer.music.get_pos()==-1):
                if self.spectrumWidget.rectFlag:
                    self.pos_start = self.spectrumWidget.rectMinX
                    self.pos_end = self.spectrumWidget.rectMaxX
                print("play")
                #pygame.mixer.music.play()
                pygame.mixer.music.play(start=self.pos_start)
                self.line_anim.event_source.start()
            else:
                print("play")
                pygame.mixer.music.unpause()
                self.line_anim.event_source.start()
        else:
            print("pause")
            pygame.mixer.music.pause()
            self.actionPlay.setText("Play")
            self.line_anim.event_source.stop()


    def btn_clicked_actionStop(self):
        print("stop")
        pygame.mixer.music.stop()
        self.actionPlay.setText("Play")
        self.line_anim.event_source.stop()

    def btn_clicked_actionPos(self):
        print("pos")
        print(pygame.mixer.music.get_pos())
        #t = threading.Timer(interval=1, function=self.draw_timeline)
        #t.start()
        self.spectrumWidget.rectFlag=False
        self.pos_init()


    """
        func : spectrumWidgetPlot
        - plot spectrum and audio signal
    """
    def spectrumWidgetPlot(self, canvas, audio_y, audio_sr):
        canvas.ax1.cla()
        canvas.ax2.cla()
        self.spectrumWidget.audio_sr = audio_sr
        self.spectrumWidget.audio_y = audio_y

        #waveform graph
        librosa.display.waveplot(audio_y, sr=audio_sr, ax=canvas.ax1)

        #spectrum graph
        S = np.abs(librosa.stft(audio_y))
        self.spectrumWidget.spectrum = amplitude = librosa.amplitude_to_db(S, ref=np.max)
        #img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=canvas.ax)
        #librosa.display.specshow(amplitude, y_axis='linear', x_axis='s', ax=canvas.ax2, sr=audio_sr, cmap=self.spectrum_color)
        librosa.display.specshow(amplitude, y_axis=self.spectrum_type, x_axis='s', ax=canvas.ax2, sr=audio_sr,
                                 cmap=self.spectrum_color)
        #librosa.display.specshow(amplitude, y_axis='linear', x_axis='s', ax=canvas.ax2, sr=audio_sr, cmap='Greys')

        canvas.fig.canvas.draw()


    """
        func : signalWidgetPlot
        - plot audio signal (deplicated)
    """
    def signalWidgetPlot(self, canvas, audio_y, audio_sr):
        librosa.display.waveplot(audio_y, sr=audio_sr)
        audio_x = np.linspace(0, len(audio_y) / audio_sr, num=len(audio_y))
        canvas.ax.plot(audio_x, audio_y)
        #img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=canvas.ax)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()





