#!/usr/bin/python3
import sys
import os
import sqlite3
import pyqtgraph
import pg_time_axis
from PyQt5 import QtWidgets, QtCore, QtGui

from testFullscreen import Ui_MainWindow

# Convert .ui to .py in Terminal
# python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py


class Ui(QtWidgets.QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super(Ui, self).__init__(parent, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pbExit.clicked.connect(self.exit)
        self.ui.pbReboot.clicked.connect(self.reboot)
        self.ui.pbShutdown.clicked.connect(self.shutdown)

        self.showFullScreen()
        self.show()

    def exit(self):
        sys.exit()

    def reboot(self):
        os.system("sudo shutdown -r now")

    def shutdown(self):
        os.system("sudo shutdown -P now")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
