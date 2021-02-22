#!/usr/bin/python3
import sys
from PyQt5 import QtWidgets, QtCore, QtGui


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("QThread Test")
        self.setGeometry(500, 500, 800, 800)



        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
