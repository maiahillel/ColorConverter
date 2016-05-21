#The window where the video will be, with the buttons and scrollers

import sys

sys.path.append('/usr/lib/pymodules/python2.7/')
sys.path.append('/usr/lib/python2.7/dist-packages')
sys.path.append('/usr/lib/pyshared/python2.7/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

import VideoWidget
from PyQt4 import QtGui

class Controller(object):

    def set_key(self):
        self.widget.set_key(-1 * self.scale.value(), -1 * self.zoom.value())

    def main(self, color_deficit, app):

        self.widget = VideoWidget.VideoWidget(color_deficit)

        sshFile = "style.stylesheet"
        with open(sshFile, "r") as fh:
            self.widget.setStyleSheet(fh.read())

        self.widget.setWindowTitle('PyQt - OpenCV Test')

        red = QtGui.QPushButton(self.widget)
        red.setAccessibleName("Red")
        red.move(100, 510)
        red.clicked.connect(self.widget.set_to_d)
        red.show()

        green = QtGui.QPushButton(self.widget)
        green.setAccessibleName("Green")
        green.move(300, 510)
        green.clicked.connect(self.widget.set_to_p)
        green.show()

        blue = QtGui.QPushButton(self.widget)
        blue.setAccessibleName("Blue")
        blue.move(500, 510)
        blue.clicked.connect(self.widget.set_to_t)
        blue.show()

        self.scale = QtGui.QScrollBar(self.widget)
        self.scale.setMaximum(0)
        self.scale.setMinimum(-100)
        self.scale.setValue(-100)
        self.scale.move(750, 100)
        self.scale.sliderMoved.connect(self.set_key)
        self.scale.show()

        self.zoom = QtGui.QScrollBar(self.widget)
        self.zoom.setMaximum(0)
        self.zoom.setMinimum(-100)
        self.zoom.move(750, 300)
        self.zoom.sliderMoved.connect(self.set_key)
        self.zoom.setWindowTitle("zoom")
        self.zoom.show()

        self.widget.show()

        sys.exit(app.exec_)




