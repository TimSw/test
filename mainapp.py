#!/usr/bin/python3
import sys
import os
import time
import RPi.GPIO
import sqlite3
import pyqtgraph
import pg_time_axis
from PyQt5 import QtWidgets, QtCore, QtGui

# Initialise iconsize
iconsize = QtCore.QSize()
iconsize.setWidth(40)
iconsize.setHeight(40)

# Initialise RPi.GPIO
uit = RPi.GPIO.HIGH
aan = RPi.GPIO.LOW
outputList = (29, 31, 33, 35)
RPi.GPIO.setmode(RPi.GPIO.BOARD)
RPi.GPIO.setup(outputList, RPi.GPIO.OUT, initial=uit)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = "App"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.showFullScreen()

        pb_thermometer = QtWidgets.QToolButton(self)
        pb_thermometer.setIcon(QtGui.QIcon("IconThermometer.png"))
        pb_thermometer.setIconSize(iconsize)
        pb_thermometer.clicked.connect(self.button_temperature_window)

        pb_light = QtWidgets.QToolButton(self)
        pb_light.setIcon(QtGui.QIcon("IconLight.png"))
        pb_light.setIconSize(iconsize)
        pb_light.clicked.connect(self.button_light_window)

        pb_water = QtWidgets.QToolButton(self)
        pb_water.setIcon(QtGui.QIcon("IconWater.png"))
        pb_water.setIconSize(iconsize)
        pb_water.clicked.connect(self.button_water_window)

        pb_clock = QtWidgets.QToolButton(self)
        pb_clock.setIcon(QtGui.QIcon("IconClock.png"))
        pb_clock.setIconSize(iconsize)
        pb_clock.clicked.connect(self.button_clock_window)

        pb_settings = QtWidgets.QToolButton(self)
        pb_settings.setIcon(QtGui.QIcon("IconSettings.png"))
        pb_settings.setIconSize(iconsize)
        pb_settings.clicked.connect(self.button_settings_window)

        pb_shutdown = QtWidgets.QToolButton(self)
        pb_shutdown.setIcon(QtGui.QIcon("IconShutdown.png"))
        pb_shutdown.setIconSize(iconsize)
        pb_shutdown.clicked.connect(self.shutdown)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(pb_thermometer, QtCore.Qt.AlignRight)
        vbox.addWidget(pb_light, QtCore.Qt.AlignRight)
        vbox.addWidget(pb_water, QtCore.Qt.AlignRight)
        vbox.addWidget(pb_clock, QtCore.Qt.AlignRight)
        vbox.addWidget(pb_settings, QtCore.Qt.AlignRight)
        vbox.addStretch(1)
        vbox.addWidget(pb_shutdown, QtCore.Qt.AlignRight)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

        self.show()

    def button_temperature_window(self):
        self.cams = TemperatureWindow(self)
        self.cams.show()
        self.close()

    def button_light_window(self):
        self.cams = LightWindow(self)
        self.cams.show()
        self.close()

    def button_water_window(self):
        self.cams = WaterWindow(self)
        self.cams.show()
        self.close()

    def button_clock_window(self):
        self.cams = ClockWindow(self)
        self.cams.show()
        self.close()

    def button_settings_window(self):
        self.cams = SettingsWindow(self)
        self.cams.show()
        self.close()

    def shutdown(self):
        self.cams = ShutdownWindow(self)
        self.cams.show()


class TemperatureWindow(QtWidgets.QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Temperature Window')
        self.showFullScreen()

# REMOVE
        # self.toggle_button = QtWidgets.QPushButton("Airstone", self)
        # self.toggle_button.setCheckable(True)
        # self.toggle_button.toggle()
        # self.toggle_button.clicked.connect(self.btn_action_pump)
        # self.toggle_button.setFixedSize(100, 50)

        pb_home = QtWidgets.QToolButton(self)
        pb_home.setIcon(QtGui.QIcon("IconHome.png"))
        pb_home.setIconSize(iconsize)
        pb_home.clicked.connect(self.go_main_window)

        pb_delete = QtWidgets.QToolButton(self)
        pb_delete.setIcon(QtGui.QIcon("IconRecycle.png"))
        pb_delete.setIconSize(iconsize)
        pb_delete.clicked.connect(self.delete_data)

        plotwidget = PlotWindow()

        hbox = QtWidgets.QHBoxLayout()
        # REMOVE hbox.addWidget(self.toggle_button)
        hbox.addWidget(pb_delete)
        hbox.addStretch()
        hbox.addWidget(pb_home)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(plotwidget)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()

# REMOVE
    # def btn_action_pump(self):
    #     if self.toggle_button.isChecked():
    #         RPi.GPIO.output(31, aan)
    #         print("button pressed")
    #     else:
    #         RPi.GPIO.output(31, uit)
    #         print("button released")

    def delete_data(self):
        pb_reply = QtWidgets.QMessageBox.question(self, 'Warning!',
                                                  "Delete all data?",
                                                  QtWidgets.QMessageBox.Yes |
                                                  QtWidgets.QMessageBox.No,
                                                  QtWidgets.QMessageBox.No)
        if pb_reply == QtWidgets.QMessageBox.Yes:
            # Initialise sqlite
            con = sqlite3.connect('data.db')
            cur = con.cursor()

            # Create table
            cur.execute('''CREATE TABLE IF NOT EXISTS temperature
                        (timestamp real, temperature1 real, temperature2 real, 
                        temperature3 real, temperature4 real, temperature5 real)''')

            # Delete all data
            cur.execute("DELETE FROM temperature")

            # Save (commit) the changes
            con.commit()

            # Close connection
            con.close()
        else:
            pass


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
        x_timestamp = []
        y_temp_1 = []
        y_temp_2 = []
        y_temp_3 = []
        y_temp_4 = []
        y_temp_5 = []
        x2data = []
        y_av_temp1 = []
        y_av_temp2 = []
        y_av_temp3 = []
        y_av_temp4 = []
        y_av_temp5 = []

        # Select all data ordered and append lists
        cur.execute(
            "SELECT * FROM temperature ORDER BY timestamp DESC LIMIT 1440")
        data = cur.fetchall()
        for row in data:
            x_timestamp.append(row[0])
            y_temp_1.append(row[1])
            y_temp_2.append(row[2])
            y_temp_3.append(row[3])
            y_temp_4.append(row[4])
            y_temp_5.append(row[5])

        # Average value
        average_1 = sum(y_temp_1) / float(len(y_temp_1))
        for i in y_temp_1:
            y_av_temp1.append(average_1)
        average_2 = sum(y_temp_2) / float(len(y_temp_2))
        for i in y_temp_2:
            y_av_temp2.append(average_2)
        average_3 = sum(y_temp_3) / float(len(y_temp_3))
        for i in y_temp_3:
            y_av_temp3.append(average_3)
        average_4 = sum(y_temp_4) / float(len(y_temp_4))
        for i in y_temp_4:
            y_av_temp4.append(average_4)
        average_5 = sum(y_temp_5) / float(len(y_temp_5))
        for i in y_temp_5:
            y_av_temp5.append(average_5)

        x2data = x_timestamp

        # Add the Date-time axis
        axis = pg_time_axis.DateAxisItem(orientation='bottom')
        axis.attachToPlotItem(self.getPlotItem())

        # Plot data
        self.plot(x=x_timestamp, y=y_temp_1, pen="r", name="Top °C")
        self.plot(x=x2data, y=y_av_temp1, pen="r", name="Av Top °C")
        self.plot(x=x_timestamp, y=y_temp_2, pen="y", name="Middle °C")
        self.plot(x=x2data, y=y_av_temp2, pen="y", name="Av Middle °C")
        self.plot(x=x_timestamp, y=y_temp_3, pen="g", name="Bottom °C")
        self.plot(x=x2data, y=y_av_temp3, pen="g", name="Av Bottom °C")
        self.plot(x=x_timestamp, y=y_temp_4, pen="b", name="Tank °C")
        self.plot(x=x2data, y=y_av_temp4, pen="b", name="Av Tank °C")
        self.plot(x=x_timestamp, y=y_temp_5, pen="m", name="Room °C")
        self.plot(x=x2data, y=y_av_temp5, pen="m", name="Av Room °C")

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()


class LightWindow(QtWidgets.QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Light Window')
        self.showFullScreen()

        self.toggle_button = QtWidgets.QPushButton("Lamp", self)
        self.toggle_button.setCheckable(True)
        self.toggle_button.toggle()
        self.toggle_button.clicked.connect(self.btn_action)
        self.toggle_button.setFixedSize(100, 50)

        push_button = QtWidgets.QToolButton(self)
        push_button.setIcon(QtGui.QIcon("IconHome.png"))
        push_button.setIconSize(iconsize)
        push_button.clicked.connect(self.go_main_window)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.toggle_button)
        hbox.addStretch(0)
        hbox.addWidget(push_button)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(0)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()

    def btn_action(self):
        if self.toggle_button.isChecked():
            RPi.GPIO.output(29, aan)
            print("button pressed")
        else:
            RPi.GPIO.output(29, uit)
            print("button released")


class WaterWindow(QtWidgets.QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Water Window')
        self.showFullScreen()

        self.tb_pomp = QtWidgets.QPushButton("Pomp", self)
        self.tb_pomp.setCheckable(True)
        self.tb_pomp.toggle()
        self.tb_pomp.clicked.connect(self.btn_action_pump)
        self.tb_pomp.setFixedSize(100, 50)

        self.tb_airstone = QtWidgets.QPushButton("Airstone", self)
        self.tb_airstone.setCheckable(True)
        self.tb_airstone.toggle()
        self.tb_airstone.clicked.connect(self.btn_action_airstone)
        self.tb_airstone.setFixedSize(100, 50)

        push_button = QtWidgets.QToolButton(self)
        push_button.setIcon(QtGui.QIcon("IconHome.png"))
        push_button.setIconSize(iconsize)
        push_button.clicked.connect(self.go_main_window)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.tb_pomp)
        hbox.addWidget(self.tb_airstone)
        hbox.addStretch(0)
        hbox.addWidget(push_button)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(0)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()

# TODO make btn_action compatible with multiple buttons
    def btn_action_pump(self):
        if self.tb_pomp.isChecked():
            RPi.GPIO.output(33, aan)
            print("button pressed")
        else:
            RPi.GPIO.output(33, uit)
            print("button released")

    def btn_action_airstone(self):
        if self.tb_airstone.isChecked():
            RPi.GPIO.output(31, aan)
            print("button pressed")
        else:
            RPi.GPIO.output(31, uit)
            print("button released")


class ClockWindow(QtWidgets.QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Clock Window')
        self.showFullScreen()

        # Create comboBox values
        hour_list = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
                     "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
                     "20", "21", "22", "23"]
        min_list = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
                    "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
                    "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
                    "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
                    "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
                    "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"]

        push_button = QtWidgets.QToolButton(self)
        push_button.setIcon(QtGui.QIcon("IconHome.png"))
        push_button.setIconSize(iconsize)
        push_button.clicked.connect(self.go_main_window)

        lbl_light = QtWidgets.QLabel("Timer Licht", self)
        lbl_start_light = QtWidgets.QLabel("Start om", self)
        lbl_stop_light = QtWidgets.QLabel("Stopt om", self)
        lbl_hour_light = QtWidgets.QLabel("uur", self)
        lbl_min_light = QtWidgets.QLabel("minuten", self)
        self.lbl_light_on_setting = QtWidgets.QLabel(self)
        # REMOVE self.lbl_light_on_setting.setText(self.update_text("light on"))

        cbx_h_light_on = QtWidgets.QComboBox(self)
        cbx_h_light_on.addItems(hour_list)
        cbx_m_light_on = QtWidgets.QComboBox(self)
        cbx_m_light_on.addItems(min_list)
        cbx_h_light_off = QtWidgets.QComboBox(self)
        cbx_h_light_off.addItems(hour_list)
        cbx_m_light_off = QtWidgets.QComboBox(self)
        cbx_m_light_off.addItems(min_list)

        pb_set_light_on = QtWidgets.QPushButton("Set", self)
        pb_set_light_on.clicked.connect(
            lambda: self.update_settings("light on",
                                         cbx_h_light_on.currentText(),
                                         cbx_m_light_on.currentText()))
        pb_set_light_on.clicked.connect(self.update_widget)
        pb_set_light_off = QtWidgets.QPushButton("Set", self)
        pb_set_light_off.clicked.connect(
            lambda: self.update_settings("light off",
                                         cbx_h_light_off.currentText(),
                                         cbx_m_light_off.currentText()))
        pb_set_light_off.clicked.connect(self.update_widget)

        lbl_pump = QtWidgets.QLabel("Timer Pomp", self)
        lbl_start_pump = QtWidgets.QLabel("Start om", self)
        lbl_stop_pump = QtWidgets.QLabel("Stopt om", self)
        lbl_hour_pump = QtWidgets.QLabel("uur", self)
        lbl_min_pump = QtWidgets.QLabel("minuten", self)

        cbx_h_pump_on = QtWidgets.QComboBox(self)
        cbx_h_pump_on.addItems(hour_list)
        cbx_m_pump_on = QtWidgets.QComboBox(self)
        cbx_m_pump_on.addItems(min_list)
        cbx_h_pump_off = QtWidgets.QComboBox(self)
        cbx_h_pump_off.addItems(hour_list)
        cbx_m_pump_off = QtWidgets.QComboBox(self)
        cbx_m_pump_off.addItems(min_list)

        pb_set_pump_on = QtWidgets.QPushButton("Set", self)
        pb_set_pump_on.clicked.connect(
            lambda: self.update_settings("pump on", cbx_h_pump_on.currentText(),
                                         cbx_m_pump_on.currentText()))
        pb_set_pump_off = QtWidgets.QPushButton("Set", self)
        pb_set_pump_off.clicked.connect(
            lambda: self.update_settings("pump off",
                                         cbx_h_pump_off.currentText(),
                                         cbx_m_pump_off.currentText()))

        lbl_air = QtWidgets.QLabel("Timer Airstone", self)
        lbl_start_air = QtWidgets.QLabel("Start om", self)
        lbl_stop_air = QtWidgets.QLabel("Stopt om", self)
        lbl_hour_air = QtWidgets.QLabel("uur", self)
        lbl_min_air = QtWidgets.QLabel("minuten", self)

        cbx_h_air_on = QtWidgets.QComboBox(self)
        cbx_h_air_on.addItems(hour_list)
        cbx_m_air_on = QtWidgets.QComboBox(self)
        cbx_m_air_on.addItems(min_list)
        cbx_h_air_off = QtWidgets.QComboBox(self)
        cbx_h_air_off.addItems(hour_list)
        cbx_m_air_off = QtWidgets.QComboBox(self)
        cbx_m_air_off.addItems(min_list)

        pb_set_air_on = QtWidgets.QPushButton("Set", self)
        pb_set_air_on.clicked.connect(
            lambda: self.update_settings("air on", cbx_h_air_on.currentText(),
                                         cbx_m_air_on.currentText()))
        pb_set_air_off = QtWidgets.QPushButton("Set", self)
        pb_set_air_off.clicked.connect(
            lambda: self.update_settings("air off", cbx_h_air_off.currentText(),
                                         cbx_m_air_off.currentText()))

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(lbl_light, 0, 0)
        grid.addWidget(lbl_start_light, 1, 0)
        grid.addWidget(cbx_h_light_on, 1, 1)
        grid.addWidget(lbl_hour_light, 1, 2)
        grid.addWidget(cbx_m_light_on, 1, 3)
        grid.addWidget(lbl_min_light, 1, 4)
        grid.addWidget(pb_set_light_on, 1, 5)
        grid.addWidget(self.lbl_light_on_setting, 1, 6)
        grid.addWidget(lbl_stop_light, 2, 0)
        grid.addWidget(cbx_h_light_off, 2, 1)
        grid.addWidget(lbl_hour_light, 2, 2)
        grid.addWidget(cbx_m_light_off, 2, 3)
        grid.addWidget(lbl_min_light, 2, 4)
        grid.addWidget(pb_set_light_off, 2, 5)

        grid.addWidget(lbl_pump, 4, 0)
        grid.addWidget(lbl_start_pump, 5, 0)
        grid.addWidget(cbx_h_pump_on, 5, 1)
        grid.addWidget(lbl_hour_pump, 5, 2)
        grid.addWidget(cbx_m_pump_on, 5, 3)
        grid.addWidget(lbl_min_pump, 5, 4)
        grid.addWidget(pb_set_pump_on, 5, 5)
        grid.addWidget(lbl_stop_pump, 6, 0)
        grid.addWidget(cbx_h_pump_off, 6, 1)
        grid.addWidget(lbl_hour_pump, 6, 2)
        grid.addWidget(cbx_m_pump_off, 6, 3)
        grid.addWidget(lbl_min_pump, 6, 4)
        grid.addWidget(pb_set_pump_off, 6, 5)

        grid.addWidget(lbl_air, 8, 0)
        grid.addWidget(lbl_start_air, 9, 0)
        grid.addWidget(cbx_h_air_on, 9, 1)
        grid.addWidget(lbl_hour_air, 9, 2)
        grid.addWidget(cbx_m_air_on, 9, 3)
        grid.addWidget(lbl_min_air, 9, 4)
        grid.addWidget(pb_set_air_on, 9, 5)
        grid.addWidget(lbl_stop_air, 10, 0)
        grid.addWidget(cbx_h_air_off, 10, 1)
        grid.addWidget(lbl_hour_air, 10, 2)
        grid.addWidget(cbx_m_air_off, 10, 3)
        grid.addWidget(lbl_min_air, 10, 4)
        grid.addWidget(pb_set_air_off, 10, 5)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(0)
        hbox.addWidget(push_button)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addStretch(0)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()

    def update_settings(self, timer, hour, minute):
        # Initialise sqlite
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Fill data
        data = (hour, minute, timer)

# TESTEN
        # Print data
        # print(data)

# TODO create timers when initialising database
        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS time
                    (timer TEXT, hour INTEGER, minute INTEGER)''')

        # Update data
        cur.execute("UPDATE time SET hour = ?, minute = ? WHERE timer = ?",
                    data)

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()


    def update_text(self, timer):
        # Initialise sqlite
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS time
                            (timer TEXT, hour INTEGER, minute INTEGER)''')

        # Read data
        cur.execute("SELECT hour, minute FROM time WHERE timer = ?", (timer,))
        data = cur.fetchone()
        hour = data[0]
        minute = data[1]

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()

        # Update label_text
        label_text = ("Current setting = " + str(hour) + "h : " + str(
            minute) + "m")
        return str(label_text)

    def update_widget(self):
        self.lbl_light_on_setting.repaint()
        # self.update()


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings Window')
        self.showFullScreen()

        push_button = QtWidgets.QToolButton(self)
        push_button.setIcon(QtGui.QIcon("IconHome.png"))
        push_button.setIconSize(iconsize)
        push_button.clicked.connect(self.go_main_window)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(0)
        hbox.addWidget(push_button)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(0)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()


class ShutdownWindow(QtWidgets.QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Shutdown Window')
        self.minimumSizeHint()
        self.showFullScreen()

        button_exit = QtWidgets.QPushButton("Exit", self)
        button_exit.minimumSizeHint()
        button_exit.setAutoDefault(False)
        button_exit.clicked.connect(self.exit)
        button_reboot = QtWidgets.QPushButton("Reboot", self)
        button_reboot.minimumSizeHint()
        button_reboot.setAutoDefault(False)
        button_reboot.clicked.connect(self.reboot)
        button_shutdown = QtWidgets.QPushButton("Shutdown", self)
        button_shutdown.minimumSizeHint()
        button_shutdown.setAutoDefault(False)
        button_shutdown.clicked.connect(self.shutdown)
        button_cancel = QtWidgets.QPushButton("Cancel", self)
        button_cancel.minimumSizeHint()
        button_cancel.clicked.connect(self.go_main_window)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(button_exit)
        hbox.addWidget(button_reboot)
        hbox.addWidget(button_shutdown)
        hbox.addWidget(button_cancel)
        hbox.addStretch(1)
        self.setLayout(hbox)

    def exit(self):
        RPi.GPIO.cleanup()
        sys.exit()

    def reboot(self):
        RPi.GPIO.cleanup()
        os.system("sudo shutdown -r now")

    def shutdown(self):
        RPi.GPIO.cleanup()
        os.system("sudo shutdown -P now")

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())