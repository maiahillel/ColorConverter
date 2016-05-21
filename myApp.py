import sys
from PyQt4 import QtCore
import Controller
import webbrowser
import WelcomeDialog

from PyQt4.QtGui import *

from PyQt4 import QtGui

controller = Controller.Controller()
app = None
w = None

def welcomeWindow():

    app = QtGui.QApplication(sys.argv)

    welcomeW = QtGui.QWidget()

    # Show welcome window with the option to do the test
    dialog = WelcomeDialog.WelcomeDialog(welcomeW)
    result = dialog.exec_()

    w = QtGui.QWidget()

    sshFile="style1.stylesheet"
    with open(sshFile,"r") as fh:
        w.setStyleSheet(fh.read())

    w.setGeometry(300,50,600,400)

    image = QtGui.QLabel(w)
    pixmap = QPixmap("Binocolors.png")
    image.setPixmap(pixmap)
    image.move(150,0)
    image.show()

    label = QtGui.QLabel(w)
    label.setText("What type of colorblind are you?")
    label.move(180, 130)

    button = QPushButton(w)
    button.setText("Deuteranope deficiency")
    button.move(120, 180)
    button.clicked.connect(launch_clickedD)
    button.show()

    button = QPushButton(w)
    button.setText("Protanope deficiency")
    button.move(120, 250)
    button.clicked.connect(launch_clickedP)
    button.show()

    button = QPushButton(w)
    button.setText("Tritanope deficiency")
    button.move(120, 320)
    button.clicked.connect(launch_clickedT)
    button.show()

    p = w.palette()
    p.setColor(w.backgroundRole(), QtCore.Qt.white)
    w.setPalette(p)

    w.show()

    app.exec_()

#def open_test():
#    webbrowser.open('http://www.color-blindness.com/fm100hue/FM100Hue.swf?width=980&height=500')


def launch_clickedD():


    controller.main('d', app)



def launch_clickedP():

    controller.main('p', app)


def launch_clickedT():

    controller.main('t', app)

def kill_clicked():
    controller.kill()


if __name__ == '__main__':

    welcomeWindow()


