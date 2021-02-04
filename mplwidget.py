
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
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)

        self.lx = self.ax2.axhline(color='g')  # the horiz line
        self.ly = self.ax2.axvline(color='g')  # the vert line
        self.lx2 = self.ax2.axhline(color='y')  # the horiz line
        self.ly2 = self.ax2.axvline(color='y')  # the vert line



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
        self.canvas.mpl_connect("motion_notify_event", self.on_move)

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
        if(event.inaxes==self.canvas.ax1):
            if (isinstance(event.xdata, float) and isinstance(event.ydata, float)):
                self.parent().parent().label1.setText("Time: " + str(np.round(event.xdata, 2)) + "s")
                self.parent().parent().label2.setText("Min: " + str(np.round(event.ydata, 2)) )
                self.parent().parent().label3.setText("Max: "  )
        if (event.inaxes == self.canvas.ax2):
            if (isinstance(event.xdata, float) and isinstance(event.ydata, float)):
                self.parent().parent().label1.setText("Time: " + str(np.round(event.xdata, 2)) + "s")
                self.parent().parent().label2.setText("Freq: " + str(np.round(event.ydata, 2)) + "Hz")

                #######################################################
                # stft spectrum data (x, y)
                # x : input_x * sr * amplitude_x_size / audio_y size
                # y : input_y * amplitude_y_size * 2 / sr
                sptx = int(event.xdata * self.audio_sr * np.shape(self.spectrum)[0] / np.size(self.audio_y))
                spty = int(event.ydata * np.shape(self.spectrum)[1] * 2 / self.audio_sr)
                self.parent().parent().label3.setText("Power: "+ str(self.spectrum[sptx][spty]) + "dB")



                #print(int(self.audio_sr / event.xdata))
                #print(self.audio_y[int(self.audio_sr/event.xdata)])
                #self.parent().parent().label3.setText("Power: "+ str(event.ydata/self.audio_sr*160 - 80))









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