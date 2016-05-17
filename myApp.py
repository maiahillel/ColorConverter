import sys
import subprocess
import time
from PyQt4 import QtCore
import Controller
import webbrowser
import VideoWidget

from PyQt4.QtGui import *

from PyQt4 import QtGui

controller = Controller.Controller()
app = None
w = None

def welcomeWindow():

    app = QtGui.QApplication(sys.argv)

    boxLayout = QtGui.QVBoxLayout()

    w = QtGui.QWidget()

    sshFile="style1.stylesheet"
    with open(sshFile,"r") as fh:
        w.setStyleSheet(fh.read())

    image = QtGui.QLabel()
    pixMap = QtGui.QPixmap("Binocolors.jpg")
    pixMap = pixMap.scaledToHeight(116)
    pixMap = pixMap.scaledToWidth(300)
    image.setPixmap(pixMap)
    boxLayout.addWidget(image)

    w.setGeometry(300,50,600,400)

    label = QtGui.QLabel(w)
    label.setText("What type of colorblind are you?")
    label.move(50, 20)
    boxLayout.addWidget(label)

    #hbox = QtGui.QHBoxLayout()


    button = QPushButton(w)
    #hbox.addStretch()
    #hbox.addWidget(button)
    #hbox.addStretch()
    #boxLayout.addLayout(hbox)
    button.setText("Problem with Red Cone")
    button.setGeometry(100, 100, 200, 200)
    button.clicked.connect(launch_clickedD)
    boxLayout.addWidget(button)
    button.show()

    button = QPushButton(w)
    boxLayout.addWidget(button)
    button.setText("Problem with Green Cone")
    #button.setGeometry(100,100,200,200)
    button.clicked.connect(launch_clickedP)
    button.show()

    button = QPushButton(w)
    boxLayout.addWidget(button)
    button.setText("Problem with Blue Cone")
    button.setGeometry(100, 100, 200, 200)
    button.clicked.connect(launch_clickedT)
    button.show()

    button = QPushButton(w)
    boxLayout.addWidget(button)
    button.setText("Not sure? Let's Check")
    button.setGeometry(100, 100, 200, 200)
    button.clicked.connect(open_test)
    button.show()

    endButton = QPushButton(w)
    boxLayout.addWidget(endButton)
    endButton.setText("End")
    endButton.setGeometry(100, 100, 200, 100)
    endButton.clicked.connect(kill_clicked)
    endButton.show()


    w.setLayout(boxLayout)

    w.show()

    app.exec_()

def open_test():
    webbrowser.open('http://www.color-blindness.com/farnsworth-munsell-100-hue-color-vision-test/#prettyPhoto')

pid = None

# def valuechange():
#   size = sl.value()
#   l1.setFont(QFont("Arial",size))

def launch_clickedD():

    controller.main('d', app)
    # global pid
    # if (pid != None):
    #      pid.kill()
    # pid = subprocess.Popen([sys.executable, "/Users/orbarda/Documents/Studies/Milab/ColorConverter/main.py"])

    # time.sleep(20)
    # pid.kill()

def launch_clickedP():

    controller.main('p', app)


def launch_clickedT():

    controller.main('t', app)

def kill_clicked():
    controller.kill()


if __name__ == '__main__':


    welcomeWindow()


