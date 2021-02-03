
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import numpy as np

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGroupBox, QHBoxLayout



# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.lx = self.ax.axhline(color='g')  # the horiz line
        self.ly = self.ax.axvline(color='g')  # the vert line
        self.lx2 = self.ax.axhline(color='y')  # the horiz line
        self.ly2 = self.ax.axvline(color='y')  # the vert line


        """
        y, sr = librosa.load("resources/bat.wav")
        S = np.abs(librosa.stft(y))
        S_left = librosa.stft(y, center=False)
        D_short = librosa.stft(y, hop_length=64)
        img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time', ax=self.ax)
        self.ax.set_title('Power spectrogram')
        self.fig.colorbar(img, ax=self.ax, format="%+2.0f dB")
        """

        """
        cid = self.fig.canvas.mpl_connect('button_press_event', onclick)
        self.fig.canvas.mpl_disconnect(cid)
        """


        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)




# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)


        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        #self.canvas.mpl_connect("motion_notify_event", self.on_move)

    def on_press(self, event):
        print("press")
        print("event.xdata", event.xdata)
        print("event.ydata", event.ydata)

        self.canvas.lx.set_ydata(event.ydata)
        self.canvas.ly.set_xdata(event.xdata)
        self.canvas.draw()

    def on_release(self, event):
        print("release:")
        print("event.xdata", event.xdata)
        print("event.ydata", event.ydata)
        self.canvas.lx2.set_ydata(event.ydata)
        self.canvas.ly2.set_xdata(event.xdata)
        self.canvas.draw()

    def on_move(self, event):
        print("move")
        #print("event.xdata", event.xdata)
        #print("event.ydata", event.ydata)






class Cursor(object):
    def __init__(self, ax):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line

        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)

    def mouse_move(self, event):
        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        print('x=%1.2f, y=%1.2f' % (x, y))

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        self.ax.figure.canvas.draw()