from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib
from BoundrySelector import  BoundrySelector
from matplotlib.widgets import RectangleSelector

"""
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGroupBox, QHBoxLayout
from PyQt5.QtGui import QPainter, QPixmap, QPen, QBrush, QImage, QIcon
"""

matplotlib.use('QT5Agg')

# Matplotlib canvas class to create figure
"""
    Class : MplCanvas
    - MplWidget Class의 field중 하나
    - plot하기 위한 요소들이 있다
"""
class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)

        Canvas.__init__(self, self.fig)
        #Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        Canvas.updateGeometry(self)


# Matplotlib widget
"""
    Class : MplWidget
    - Matplotlib widget의 Class
"""
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.canvas)
        self.vbl.addWidget(self.scroll)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        #self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

        # event
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("button_release_event", self.on_release)
        self.canvas.mpl_connect("motion_notify_event", self.on_move)


        # init values
        self.isPressd = False
        self.rectStartX=0
        self.rectStartY=0
        self.rectEndX=0
        self.rectEndY=0
        self.whichEventAx = ""
        self.rectFlag = False

        self.rectAx=0
        self.rectMinX=0
        self.rectMaxX=0
        self.rectMinY = 0
        self.rectMaxY = 0


        # init selector
        self.RS = RectangleSelector(self.canvas.ax2, self.rs_ax2_callback,
                                       drawtype='box', useblit=True,
                                       button=[1],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)

        self.RS2 = BoundrySelector(self.canvas.ax1, self.rs_ax1_callback,
                                       drawtype='box', useblit=True,
                                       button=[1],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)



    """
        func : myInit
        - Main Window init 시 실행
    """
    def myInit(self, mw):
        self.mw = mw
        #w, h = self.canvas.fig.get_size_inches()
        #self.canvas.fig.set_size_inches(w,h)


    """
        func : rs_ax2_callback
        - RectangleSelector의 callback
    """
    def rs_ax2_callback(self, eclick, erelease):
        self.whichEventAx="ax2"
        #self.rectStartX = 0
        #self.rectStartY = 0
        #self.rectEndX = 0
        #self.rectEndY = 0

    """
        func : rs_ax1_callback
        - BoundrySelector의 callback
    """
    def rs_ax1_callback(self, eclick, erelease):
        self.whichEventAx="ax1"
        #self.rectStartX = 0
        #self.rectStartY = 0
        #self.rectEndX = 0
        #self.rectEndY = 0


    #   mouse event
    def on_press(self, event):
        self.isPressd = True
        self.rectStartX = event.xdata
        self.rectStartY = event.ydata
        self.rectEndX = event.xdata
        self.rectEndY = event.ydata
        #print("press")
        #print("event.xdata", event.xdata)
        #print("event.ydata", event.ydata)

    def on_release(self, event):
        self.isPressd = False
        #self.rectStartX = 0
        #self.rectStartY = 0
        self.rectEndX = event.xdata
        self.rectEndY = event.ydata
        #print("release:")
        #print("event.xdata", event.xdata)
        #print("event.ydata", event.ydata)
        #self.canvas.draw()
        self.rectFlag = True

        self.rectMinX = min(self.rectStartX, self.rectEndX)
        self.rectMaxX = max(self.rectStartX, self.rectEndX)
        self.rectMinY = min(self.rectStartY, self.rectEndY)
        self.rectMaxY = max(self.rectStartY, self.rectEndY)

        if (event.inaxes == self.canvas.ax1):
            self.rectAx = 1
            self.mw.label_rect.setText("Begin Time(s): %.3fs   End Time(s): %.3fs" % (self.rectMinX, self.rectMaxX))

        if (event.inaxes == self.canvas.ax2):
            self.rectAx = 2
            self.mw.label_rect.setText("Begin Time(s): %.3f   End Time(s): %.3f   Low Freq(Hz): %.3f   High Freq(Hz): %.3f" % (self.rectMinX, self.rectMaxX, self.rectMinY, self.rectMaxY))


    def on_move(self, event):
        if(self.isPressd is True):
            self.rectEndX = event.xdata
            self.rectEndY = event.ydata

        if(event.inaxes==self.canvas.ax1):
            if (isinstance(event.xdata, float) and isinstance(event.ydata, float)):
                self.mw.label1.setText("Time: " + str(np.round(event.xdata, 2)) + "s")
                #                                      "Min: " + str(np.round(event.ydata, 2)) + "   " +
                #                                      "index: " + str(int(event.xdata*self.audio_sr)) + "   " +
                #                                      "value: " + str(self.audio_y[int(event.xdata * self.audio_sr)]))


        if (event.inaxes == self.canvas.ax2):
            if (isinstance(event.xdata, float) and isinstance(event.ydata, float)):
                #######################################################
                # stft spectrum data (x, y)
                # x : input_x * sr * amplitude_x_size / audio_y size
                # y : input_y * amplitude_y_size * 2 / sr
                sptx = int(event.xdata * self.audio_sr * np.shape(self.spectrum)[0] / np.size(self.audio_y))
                spty = int(event.ydata * np.shape(self.spectrum)[1] * 2 / self.audio_sr)
                self.mw.label1.setText("Time: " + str(np.round(event.xdata, 3)) + "s   " +
                                                      "Freq: " + str("{:,}".format(int(event.ydata))) + "Hz   " +
                                                      "Power: " + str(np.round(self.spectrum[sptx][spty], 1)) + "dB")

