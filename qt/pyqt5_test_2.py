#!/usr/bin/env python3
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 800, 480)
        self.setWindowTitle("PyQT tuts!")

        extract_action = QtWidgets.QAction("&GET TO THE CHOPPAH!!!", self)
        extract_action.setShortcut("Ctrl+Q")
        extract_action.setStatusTip('Leave The App')
        extract_action.triggered.connect(self.close_application)

        self.statusBar()

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(extract_action)

        self.home()

    def home(self):
        btn = QtWidgets.QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.minimumSizeHint())
        btn.move(100, 100)

        extract_action = QtWidgets.QAction(QIcon("pythonlogo.png"), "Flee the Scene", self)
        extract_action.triggered.connect(self.close_application)

        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extract_action)

        check_box = QtWidgets.QCheckBox('Enlarge Window', self)
        check_box.move(100, 25)
        check_box.stateChanged.connect(self.enlarge_window)
        # depending on what you want the default to be.
        # checkBox.toggle()

        print(self.style().objectName())
        self.styleChoice = QtWidgets.QLabel("windows", self)

        combo_box = QtWidgets.QComboBox(self)
        combo_box.addItem("windows")
        combo_box.addItem("macintosh")
        combo_box.move(50, 250)

        self.styleChoice.move(50, 150)
        combo_box.activated[str].connect(self.style_choice)

        self.show()

    def style_choice(self, text):
        self.styleChoice.setText(text)
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create(text))

    def enlarge_window(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(50, 50, 1000, 600)
        else:
            self.setGeometry(50, 50, 800, 480)

    def close_application(self):
        choice = QtWidgets.QMessageBox.question(self, "Extract!",
                    "Get into the chopper?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if choice == QtWidgets.QMessageBox.Yes:
            print("Extracting Naaaaaaoooww!!!!")
            sys.exit()
        else:
            pass


def run():
    app = QtWidgets.QApplication(sys.argv)
    gui = Window()
    sys.exit(app.exec_())


run()
