# Defines the first window that opens when you open the app.
# The user either knows what is his color decifiency, or he doesn't and he does the test

from PyQt4.QtGui import *
from PyQt4 import QtGui
from PyQt4 import QtCore
import webbrowser

class WelcomeDialog(QDialog):
    def __init__(self, parent = None):
        super(WelcomeDialog, self).__init__(parent)

        layout = QVBoxLayout(self)


        sshFile="style1.stylesheet"
        with open(sshFile, "r") as fh:
            self.setStyleSheet(fh.read())

        self.setGeometry(300, 50, 400, 400)

        image = QtGui.QLabel(self)
        pixmap = QPixmap("Binocolors.png")
        image.setPixmap(pixmap)
        image.move(150, 0)
        image.show()

        layout.addWidget(image)
        layout.addStretch()

        label = QtGui.QLabel(self)
        label.setText("Do you know what type of colorblind are you?")
        label.move(180, 130)

        layout.addWidget(label)

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(p)

        yesButton = QPushButton()
        yesButton.setText("Yes!")
        yesButton.setDefault(True)

        noButton = QPushButton()
        noButton.setText("No, Lets Find Out!")
        noButton.setCheckable(True)
        noButton.setAutoDefault(False)

        buttons = QDialogButtonBox(0x2)
        buttons.addButton(yesButton, QDialogButtonBox.AcceptRole)
        buttons.addButton(noButton,  QDialogButtonBox.RejectRole)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.open_test)

        buttons.setGeometry(700, 700, 350, 30)

        layout.addStretch()
        layout.addWidget(buttons)


    def open_test(self):
        webbrowser.open('http://www.color-blindness.com/fm100hue/FM100Hue.swf?width=980&height=500')



