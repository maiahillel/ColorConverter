# coding=utf8

# Copyright (C) 2011 Saúl Ibarra Corretgé <saghul@gmail.com>
#

# Some inspiration taken from: http://www.morethantechnical.com/2009/03/05/qt-opencv-combined-for-face-detecting-qwidgets/

import ColorConverter
import sys

sys.path.append('/usr/lib/pymodules/python2.7/')
sys.path.append('/usr/lib/python2.7/dist-packages')
sys.path.append('/usr/lib/pyshared/python2.7/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

import numpy
import cv2 as cv
from PyQt4.QtCore import *
import IplQImage

from PyQt4.QtGui import *

class VideoWidget(QWidget):
    """ A class for rendering video coming from OpenCV """

    def __init__(self, color_deficit, parent=None):
        QWidget.__init__(self)
        self.capture = cv.VideoCapture(0)
        # Take one frame to query height
        ret, frame = self.capture.read()
        self.color_converter = ColorConverter.ColorConverter(color_deficit)
        image = self.color_converter.convert(frame)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(self.minimumSize())
        self._frame = None
        self._image = self._build_image(image)
        # Paint every 50 ms
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.queryFrame)
        self._timer.start(50)



    def _build_image(self, frame):
        self._frame = frame
        # if frame.origin == cv.IPL_ORIGIN_TL:
        #     cv.Copy(frame, self._frame)
        # else:
        #     cv.Flip(frame, self._frame, 0)
        return IplQImage.IplQImage(numpy.fliplr(self._frame))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(QPoint(0, 0), self._image)

    def queryFrame(self):
        ret, frame = self.capture.read()
        image = self.color_converter.convert(frame)
        self._image = self._build_image(image)
        self.update()

