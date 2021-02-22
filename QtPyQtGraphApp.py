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

        # Connect PlotWidget
        # Initialise sqlite
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS temperature
                    (timestamp real, temperature1 real, temperature2 real, 
                    temperature3 real, temperature4 real, temperature5 real)''')

        # Initialise data arrays
        data_tst = []
        data_temp_1 = []
        data_av_temp_1 = []
        data_temp_2 = []
        data_av_temp_2 = []
        data_temp_3 = []
        data_av_temp_3 = []
        data_temp_4 = []
        data_av_temp_4 = []
        data_temp_5 = []
        data_av_temp_5 = []

        # Select all data ordered and append lists
        cur.execute("SELECT * FROM temperature ORDER BY timestamp DESC LIMIT 1440")
        data = cur.fetchall()
        for row in data:
            data_tst.append(row[0])
            data_temp_1.append(row[1])
            data_temp_2.append(row[2])
            data_temp_3.append(row[3])
            data_temp_4.append(row[4])
            data_temp_5.append(row[5])

        # Average value
        average_1 = sum(data_temp_1) / float(len(data_temp_1))
        for i in data_temp_1:
            data_av_temp_1.append(average_1)
        average_2 = sum(data_temp_2) / float(len(data_temp_2))
        for i in data_temp_2:
            data_av_temp_2.append(average_2)
        average_3 = sum(data_temp_3) / float(len(data_temp_3))
        for i in data_temp_3:
            data_av_temp_3.append(average_3)
        average_4 = sum(data_temp_4) / float(len(data_temp_4))
        for i in data_temp_4:
            data_av_temp_4.append(average_4)
        average_5 = sum(data_temp_5) / float(len(data_temp_5))
        for i in data_temp_5:
            data_av_temp_5.append(average_5)

        # Add the Date-time axis
        axis = pg_time_axis.DateAxisItem(orientation='bottom')
        axis.attachToPlotItem(self.ui.plotWindow.getPlotItem())

        # Add Legend
        self.ui.plotWindow.addLegend()

        # Plot data
        self.ui.plotWindow.plot(x=data_tst, y=data_temp_1, pen="r", name="Top °C")
        self.ui.plotWindow.plot(x=data_tst, y=data_av_temp_1, pen="r", style=QtCore.Qt.DotLine)
        self.ui.plotWindow.plot(x=data_tst, y=data_temp_2, pen="y", name="Middle °C")
        self.ui.plotWindow.plot(x=data_tst, y=data_av_temp_2, pen="y", style=QtCore.Qt.DotLine)
        self.ui.plotWindow.plot(x=data_tst, y=data_temp_3, pen="g", name="Bottom °C")
        self.ui.plotWindow.plot(x=data_tst, y=data_av_temp_3, pen="g", style=QtCore.Qt.DotLine)
        self.ui.plotWindow.plot(x=data_tst, y=data_temp_4, pen="b", name="Water °C")
        self.ui.plotWindow.plot(x=data_tst, y=data_av_temp_4, pen="b", style=QtCore.Qt.DotLine)
        self.ui.plotWindow.plot(x=data_tst, y=data_temp_5, pen="m", name="Room °C")
        self.ui.plotWindow.plot(x=data_tst, y=data_av_temp_5, pen="m", style=QtCore.Qt.DotLine)

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()

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
