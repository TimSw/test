#!/usr/bin/python3
import sys
import os
import sqlite3
import pyqtgraph
import pg_time_axis
from PyQt5 import QtWidgets, QtCore, QtGui

from test import Ui_MainWindow

# Convert .ui to .py in Terminal
# python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py


class Ui(QtWidgets.QMainWindow):
    def __init__(self, parent=None, **kwargs):
        # super().__init__(parent, **kwargs)
        # uic.loadUi("test.ui", self)
        # self.show()
        super(Ui, self).__init__(parent, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.showFullScreen()

        self.ui.pbExit.clicked.connect(self.exit)
        self.ui.pbReboot.clicked.connect(self.reboot)
        self.ui.pbShutdown.clicked.connect(self.shutdown)

        self.ui.tabTempData = PlotWindow()

        self.show()

    def exit(self):
        sys.exit()

    def reboot(self):
        os.system("sudo shutdown -r now")

    def shutdown(self):
        os.system("sudo shutdown -P now")


class PlotWindow(pyqtgraph.PlotWidget):
    def __init__(self):
        pyqtgraph.PlotWidget.__init__(self)

        # Initialise sqlite
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS temperature
            (timestamp real, temperature real)''')

        # Initialise data arrays
        x1data = []
        y1data = []
        x2data = []
        y2data = []

        # Select all data ordered and append lists
        cur.execute("SELECT * FROM temperature ORDER BY timestamp DESC LIMIT 1440")
        data = cur.fetchall()
        for row in data:
            x1data.append(row[0])
            y1data.append(row[1])

        # Average value
        average = sum(y1data) / float(len(y1data))
        for i in y1data:
            y2data.append(average)

        x2data = x1data

        # Add the Date-time axis
        axis = pg_time_axis.DateAxisItem(orientation='bottom')
        axis.attachToPlotItem(self.getPlotItem())

        # Plot data
        self.plot(x=x1data, y=y1data, pen="g", name="Actual °C")
        self.plot(x=x2data, y=y2data, pen="r", name="Average °C")

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
