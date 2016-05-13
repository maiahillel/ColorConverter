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
import VideoWidget
from PyQt4 import QtGui

class Controller(object):


    def main(self, color_deficit):

        widget = VideoWidget.VideoWidget(color_deficit)

        sshFile="style.stylesheet"
        with open(sshFile,"r") as fh:
            widget.setStyleSheet(fh.read())

        widget.setWindowTitle('PyQt - OpenCV Test')

        red = QPushButton(widget)
        red.setAccessibleName("Red")
        red.move(100, 500)
        red.show()

        green = QPushButton(widget)
        green.setAccessibleName("Green")
        green.move(300, 500)
        green.show()

        blue = QPushButton(widget)
        blue.setAccessibleName("Blue")
        blue.move(500, 500)
        blue.show()

        scroller = QScrollBar(widget)
        scroller.setMaximum(100)
        scroller.move(750, 100)
        scroller.show()

        widget.show()




