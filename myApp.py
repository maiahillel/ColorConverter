import sys
import subprocess
import time
from PyQt4.QtCore import *
import Controller
import webbrowser


from PyQt4.QtGui import *

from PyQt4 import QtGui

controller = Controller.Controller()

def welcomeWindow():

    app2 = QtGui.QApplication(sys.argv)
    boxLayout = QtGui.QVBoxLayout()

    w = QtGui.QWidget()

    sshFile="style.stylesheet"
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

    sys.exit(app2.exec_())

def open_test():
    webbrowser.open('http://www.color-blindness.com/farnsworth-munsell-100-hue-color-vision-test/#prettyPhoto')

pid = None
def window():

    app = QtGui.QApplication(sys.argv)

    layout = QtGui.QGridLayout()

    w = QtGui.QWidget()

    sshFile="style.stylesheet"
    with open(sshFile,"r") as fh:
        w.setStyleSheet(fh.read())

    label = QtGui.QLabel(w)
    label.setText("Hello! Please Click " +'''<a href='http://www.color-blindness.com/farnsworth-munsell-100-hue-color-vision-test/#prettyPhoto'> This link </a>''' + " and perform the test so we could get started...")
    label.setOpenExternalLinks(True)
    label.move(50,20)
    layout.addWidget(label, 1, 1, 1, 2)

    w.setGeometry(300, 50, 800, 90)
    w.setWindowTitle("Color Converter")
    w.show()

    button = QPushButton(w)
    layout.addWidget(button, 2, 1)
    button.setText("Launch Camera")
    button.setGeometry(100, 100, 200, 100)
    button.clicked.connect(launch_clickedD())
    button.show()

    endButton = QPushButton(w)
    layout.addWidget(endButton, 2, 2)
    endButton.setText("End")
    endButton.setGeometry(100, 100, 200, 100)
    endButton.clicked.connect(kill_clicked)
    endButton.show()


    w.setLayout(layout)
    sys.exit(app.exec_())

# def valuechange():
#   size = sl.value()
#   l1.setFont(QFont("Arial",size))

def launch_clickedD():

    controller.main('d')
    # global pid
    # if (pid != None):
    #      pid.kill()
    # pid = subprocess.Popen([sys.executable, "/Users/orbarda/Documents/Studies/Milab/ColorConverter/main.py"])

    # time.sleep(20)
    # pid.kill()

def launch_clickedP():

    controller.main('p')

def launch_clickedT():

    controller.main('t')


def kill_clicked():
    controller.kill()

if __name__ == '__main__':
    welcomeWindow()

