#!/usr/bin/python3
import sqlite3
import pyqtgraph
import pg_time_axis
from PyQt5 import QtGui, QtCore


class PlotWindow(pyqtgraph.PlotWidget):
    def __init__(self):
        pyqtgraph.PlotWidget.__init__(self)

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
        axis.attachToPlotItem(self.getPlotItem())

        # Add Legend
        self.addLegend()

        # Plot data
        self.plot(x=data_tst, y=data_temp_1, pen="r", name="Top °C")
        self.plot(x=data_tst, y=data_av_temp_1, pen="r", style=QtCore.Qt.DotLine)
        self.plot(x=data_tst, y=data_temp_2, pen="y", name="Middle °C")
        self.plot(x=data_tst, y=data_av_temp_2, pen="y", style=QtCore.Qt.DotLine)
        self.plot(x=data_tst, y=data_temp_3, pen="g", name="Bottom °C")
        self.plot(x=data_tst, y=data_av_temp_3, pen="g", style=QtCore.Qt.DotLine)
        self.plot(x=data_tst, y=data_temp_4, pen="b", name="Water °C")
        self.plot(x=data_tst, y=data_av_temp_4, pen="b", style=QtCore.Qt.DotLine)
        self.plot(x=data_tst, y=data_temp_5, pen="m", name="Room °C")
        self.plot(x=data_tst, y=data_av_temp_5, pen="m", style=QtCore.Qt.DotLine)

        # Add Legend
        #l = pyqtgraph.LegendItem((150, 150), offset=(250, 250))  # args are (size, offset)
        #l.setParentItem(self.graphicsItem())   # Note we do NOT call plt.addItem in this case

        # Plot data
        #plt1 = self.plot(x=data_tst, y=data_temp_1, pen="r", name="Top °C")
        #plt2 = self.plot(x=data_tst, y=data_av_temp_1, pen="r", style=QtCore.Qt.DotLine)
        #plt3 = self.plot(x=data_tst, y=data_temp_2, pen="y", name="Middle °C")
        #plt4 = self.plot(x=data_tst, y=data_av_temp_2, pen="y", style=QtCore.Qt.DotLine)
        #plt5 = self.plot(x=data_tst, y=data_temp_3, pen="g", name="Bottom °C")
        #plt6 = self.plot(x=data_tst, y=data_av_temp_3, pen="g", style=QtCore.Qt.DotLine)
        #plt7 = self.plot(x=data_tst, y=data_temp_4, pen="b", name="Water °C")
        #plt8 = self.plot(x=data_tst, y=data_av_temp_4, pen="b", style=QtCore.Qt.DotLine)
        #plt9 = self.plot(x=data_tst, y=data_temp_5, pen="m", name="Room °C")
        #plt10 = self.plot(x=data_tst, y=data_av_temp_5, pen="m", style=QtCore.Qt.DotLine)

        #l.addItem(plt1, "Top °C")
        #l.addItem(plt3, "Middle °C")
        #l.addItem(plt5, "Bottom °C")
        #l.addItem(plt7, "Water °C")
        #l.addItem(plt9, "Room °C")

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()


if __name__ == '__main__':
    w = PlotWindow()
    w.show()
    QtGui.QApplication.instance().exec_()

