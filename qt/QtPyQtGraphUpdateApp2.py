#!/usr/bin/python3
import sys
import os
import sqlite3
import pyqtgraph
import pg_time_axis
from PyQt5 import QtWidgets, QtCore, QtGui

# Import UI.py
# Convert .ui to .py in Terminal
# python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py
from QtPyQtGraph import Ui_MainWindow


class Ui(QtWidgets.QMainWindow):
    def __init__(self, parent=None, **kwargs):
        super(Ui, self).__init__(parent, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect button actions
        self.ui.pbExit.clicked.connect(self.exit)
        self.ui.pbReboot.clicked.connect(self.reboot)
        self.ui.pbShutdown.clicked.connect(self.shutdown)

        # Configure Plot
        # Initialise data arrays
        self.data_tst = []
        self.data_temp_1 = []
        self.data_av_temp_1 = []

        # Add Legend
        self.ui.plotWindow.addLegend()

        # Set Update Timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updater)
        self.timer.start(5000)

        self.showFullScreen()
        self.show()

    def updater(self):
        # Initialise sqlite
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS temperature
                    (timestamp real, temperature1 real, temperature2 real, 
                    temperature3 real, temperature4 real, temperature5 real)''')

        # Select all data ordered and append lists
        cur.execute("SELECT * FROM temperature ORDER BY timestamp DESC LIMIT 1440")
        self.data = cur.fetchall()
        for row in self.data:
            self.data_tst.append(row[0])
            self.data_temp_1.append(row[1])

        # Average value
        self.average_1 = sum(self.data_temp_1) / float(len(self.data_temp_1))
        for i in self.data_temp_1:
            self.data_av_temp_1.append(self.average_1)

        # Add the Date-time axis
        axis = pg_time_axis.DateAxisItem(orientation='bottom')
        #axis.attachToPlotItem(self.ui.plotWindow.getPlotItem())

        # Plot data
        self.ui.plotWindow.plot(x=self.data_tst, y=self.data_temp_1, pen="r", name="Top °C")
        self.ui.plotWindow.plot(x=self.data_tst, y=self.data_av_temp_1, pen="r")

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()

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
