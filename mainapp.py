#!/usr/bin/python3
import sys
import os
import time
import datetime
import threading
# import logging
import logging.handlers
import RPi.GPIO
import sqlite3
import pyqtgraph
import pg_time_axis
from PyQt5 import QtWidgets, QtCore, QtGui

# Initialise logger
# create logger with 'mainapp'
logger = logging.getLogger("mainapp")
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
rfh = logging.handlers.RotatingFileHandler("mainapp.log", "a", 2560000, 3)
rfh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(lineno)d: %(message)s")
#  "%(asctime)s - %(filename)s - %(name)s - %(levelname)s - %(message)s")
rfh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(rfh)
logger.addHandler(ch)

# Define data.db directory
data_db = 'data.db'

# Initialise icon_size
icon_size = QtCore.QSize()
icon_size.setWidth(40)
icon_size.setHeight(40)

# Initialise RPi.GPIO
uit = RPi.GPIO.HIGH
aan = RPi.GPIO.LOW
outputList = (29, 31, 33, 35)
RPi.GPIO.setmode(RPi.GPIO.BOARD)
RPi.GPIO.setup(outputList, RPi.GPIO.OUT, initial=uit)


class LightTimer:
    def __init__(self):
        pass

    start_hour = 0
    start_min = 0
    stop_hour = 0
    stop_min = 0
    start_light = 0
    stop_light = 0
    time_light_on = 0

    def process_light_timer(self):
        while True:
            # Initialise sqlite
            con = sqlite3.connect(data_db)
            cur = con.cursor()

            try:
                # Select start time from table
                timer_on = ("light_on",)
                cur.execute("SELECT * FROM timers WHERE setting = ?", timer_on)
                data_timer_on = cur.fetchone()
                LightTimer.start_hour = data_timer_on[1]
                LightTimer.start_min = data_timer_on[2]
                LightTimer.start_light = datetime.time(LightTimer.start_hour,
                                                 LightTimer.start_min)

                # Select stop time from table
                timer_off = ("light_off",)
                cur.execute("SELECT * FROM timers WHERE setting = ?",
                            timer_off)
                data_timer_off = cur.fetchone()
                LightTimer.stop_hour = data_timer_off[1]
                LightTimer.stop_min = data_timer_off[2]
                LightTimer.stop_light = datetime.time(LightTimer.stop_hour, LightTimer.stop_min)

                # Initialise current time
                now = datetime.datetime.now().time()
                date = datetime.date(1, 1, 1)
                datetime_start = datetime.datetime.combine(date,
                                                           LightTimer.start_light)
                datetime_stop = datetime.datetime.combine(date,
                                                          LightTimer.stop_light)
                LightTimer.time_light_on = datetime_stop - datetime_start

                logger.debug("Het is %s uur en %s minuten", now.hour,
                             now.minute)
                logger.debug("Lamp gaat aan om %s", LightTimer.start_light)
                logger.debug("Lamp gaat uit om %s", LightTimer.stop_light)
                logger.debug("Licht is aan gedurende %s", LightTimer.time_light_on)

                # Light
                if LightTimer.start_light < now < LightTimer.stop_light:
                    LightOutput.light_output = 1
                    logger.debug("LightOutput.light_output = %s",
                                 LightOutput.light_output)
                    logger.info("TIMER LIGHT ON")
                else:
                    LightOutput.light_output = 0
                    logger.debug("LightOutput.light_output = %s",
                                 LightOutput.light_output)
                    logger.info("TIMER LIGHT OFF")

                time.sleep(10)

            except Exception as e:
                logger.exception(e)
                # Close sql connection
                con.close()

    def run(self):
        thread_1 = threading.Thread(target=self.process_light_timer,
                                    daemon=True)
        thread_1.start()


class PumpTimer:
    def __init__(self):
        pass

    pump_repeat = 1
    pump_during = 0
    time_pump_on = 0
    time_btwn_pumping = 0
    print("pump_repeat in PumpTimer = ",
          pump_repeat)

    def process_pump_timer(self):
        while True:
            # Initialise sqlite
            con = sqlite3.connect(data_db)
            cur = con.cursor()

            try:
                # Select pump settings from table
                pump_setting = ("pump_during",)
                cur.execute("SELECT * FROM timers WHERE setting = ?",
                            pump_setting)
                data_pump_setting = cur.fetchone()
                PumpTimer.pump_repeat = data_pump_setting[1]
                PumpTimer.pump_during = data_pump_setting[2]
                PumpTimer.time_pump_on = datetime.time(00, PumpTimer.pump_during)

                PumpTimer.time_btwn_pumping = \
                    LightTimer.time_light_on // PumpTimer.pump_repeat

                logger.debug("Pomp werkt gedurende %s en gaat %s keer aan om "
                             "de %s",
                             PumpTimer.time_pump_on, PumpTimer.pump_repeat,
                             PumpTimer.time_btwn_pumping)

                time.sleep(10)

            except Exception as e:
                logger.exception(e)
                # Close sql connection
                con.close()

    def run(self):
        thread_1 = threading.Thread(target=self.process_pump_timer,
                                    daemon=True)
        thread_1.start()


class AirstoneTimer:
    def __init__(self):
        pass

    air_on = 0

    def process_airstone_timer(self):
        while True:
            # Initialise sqlite
            con = sqlite3.connect(data_db)
            cur = con.cursor()

            try:
                # Select airstone settings from table
                air_setting = ("air_on",)
                cur.execute("SELECT * FROM timers WHERE setting = ?",
                            air_setting)
                data_air_setting = cur.fetchone()
                AirstoneTimer.air_on = data_air_setting[1]
                time_air_on = datetime.time(00, AirstoneTimer.air_on)

                logger.debug("Airstone gaat %s voor de pomp aan",
                             time_air_on)

                time.sleep(10)

            except Exception as e:
                logger.exception(e)
                # Close sql connection
                con.close()

    def run(self):
        thread_1 = threading.Thread(target=self.process_airstone_timer,
                                    daemon=True)
        thread_1.start()


class ProcessTimers:
    def __init__(self):
        pass

    def process(self):
        while True:
            # Initialise variables
            repeats = PumpTimer.pump_repeat
            print("PumpTimer.pump_repeat in ProcessTimers = ",
                  PumpTimer.pump_repeat)

            # Initialise current time
            now = datetime.datetime.now().time()
            date = datetime.date(1, 1, 1)

            # Convert times
            # Light
            start_light = datetime.time(LightTimer.start_hour,
                                        LightTimer.start_min)
            stop_light = datetime.time(LightTimer.stop_hour,
                                       LightTimer.stop_min)
            datetime_start = datetime.datetime.combine(date, start_light)
            datetime_stop = datetime.datetime.combine(date, stop_light)
            time_light_on = datetime_stop - datetime_start
            timedelta_start_light = datetime.timedelta(
                hours=LightTimer.start_hour, minutes=LightTimer.start_min)
            # Air
            timedelta_air_on = datetime.timedelta(
                hours=00, minutes=AirstoneTimer.air_on)
            # Pump
            timedelta_pump_on = datetime.timedelta(
                hours=00, minutes=PumpTimer.pump_during)
            print("PumpTimer.pump_repeat in ProcessTimers = ",
                  PumpTimer.pump_repeat)
            pump_interval = time_light_on // PumpTimer.pump_repeat

            # Initialise lists
            pump_start_times = []
            pump_stop_times = []
            air_start_times = []

            # Determine first list
            while repeats > 1:
                pump_start_times.append(time_light_on + (pump_interval *
                                                         repeats))
                repeats = repeats - 1
            pump_start_times.reverse()
            pump_start_times.insert(0, timedelta_start_light)

            # Determine other lists depending on first
            for times in pump_start_times:
                pump_stop_times.append(times + timedelta_pump_on)
                air_start_times.append(times - timedelta_air_on)
            for i in pump_start_times:
                logger.debug(i)
            for i in pump_stop_times:
                logger.debug(i)
            for i in air_start_times:
                logger.debug(i)

    def run(self):
        thread_1 = threading.Thread(target=self.process, daemon=True)
        thread_1.start()


class LightOutput:
    def __init__(self):
        pass

    light_output = 0
    logger.debug("light_output in LightOutput class = %s", light_output)

    def set_light_output(self):
        while True:
            if self.light_output == 1 and LightSetting.light_setting == 1:
                logger.debug("self.light_output = %s", self.light_output)
                RPi.GPIO.output(29, aan)
                logger.info("OUTPUT LIGHT ON")
                time.sleep(10)
            else:
                logger.debug("self.light_output = %s", self.light_output)
                RPi.GPIO.output(29, uit)
                logger.info("OUTPUT LIGHT OFF")
                time.sleep(10)

    def run(self):
        thread_1 = threading.Thread(target=self.set_light_output, daemon=True)
        thread_1.start()


class PumpOutput:
    def __init__(self):
        pass

    pump_output = 0
    logger.debug("pump_output in PumpOutput class = %s", pump_output)

    def set_pump_output(self):
        while True:
            if self.pump_output == 1 and PumpSetting.pump_setting == 1:
                logger.debug("self.pump_output = %s", self.pump_output)
                RPi.GPIO.output(33, aan)
                logger.info("OUTPUT PUMP ON")
                time.sleep(10)
            else:
                logger.debug("self.pump_output = %s", self.pump_output)
                RPi.GPIO.output(33, uit)
                logger.info("OUTPUT PUMP OFF")
                time.sleep(10)

    def run(self):
        t1 = threading.Thread(target=self.set_pump_output, daemon=True)
        t1.start()


class AirstoneOutput:
    def __init__(self):
        pass

    airstone_output = 0
    logger.debug("airstone_output in AirstoneOutput class = %s",
                 airstone_output)

    def set_airstone_output(self):
        while True:
            if self.airstone_output == 1 and \
                    AirstoneSetting.airstone_setting == 1:
                logger.debug("self.airstone_output = %s", self.airstone_output)
                RPi.GPIO.output(31, aan)
                logger.info("OUTPUT AIRSTONE ON")
                time.sleep(10)
            else:
                logger.debug("self.airstone_output = %s", self.airstone_output)
                RPi.GPIO.output(31, uit)
                logger.info("OUTPUT AIRSTONE OFF")
                time.sleep(10)

    def run(self):
        t1 = threading.Thread(target=self.set_airstone_output, daemon=True)
        t1.start()


class LightSetting:
    def __init__(self):
        pass

    # Initialise sqlite
    con = sqlite3.connect(data_db)
    cur = con.cursor()

    try:
        # Select light setting from table
        light = ("light",)
        cur.execute("SELECT * FROM settings WHERE setting = ?", light)
        data_light = cur.fetchone()
        logger.debug("data_light = %s", data_light)
        light_on_off = data_light[1]
        logger.debug("Setting light_on_off = %s", light_on_off)

    except Exception as e:
        logger.exception(e)
        # Close sql connection
        con.close()

    light_setting = light_on_off
    logger.info("light_setting in LightSetting class = %s", light_setting)


class PumpSetting:
    def __init__(self):
        pass

    # Initialise sqlite
    con = sqlite3.connect(data_db)
    cur = con.cursor()

    try:
        # Select pump setting from table
        pump = ("pump",)
        cur.execute("SELECT * FROM settings WHERE setting = ?", pump)
        data_pump = cur.fetchone()
        logger.debug("data_pump = %s", data_pump)
        pump_on_off = data_pump[1]
        logger.debug("Setting pump_on_off = %s", pump_on_off)

    except Exception as e:
        logger.exception(e)
        # Close sql connection
        con.close()

    pump_setting = pump_on_off
    logger.info("pump_setting in PumpSetting class = %s", pump_setting)


class AirstoneSetting:
    def __init__(self):
        pass

    # Initialise sqlite
    con = sqlite3.connect(data_db)
    cur = con.cursor()

    try:
        # Select airstone setting from table
        airstone = ("airstone",)
        cur.execute("SELECT * FROM settings WHERE setting = ?", airstone)
        data_airstone = cur.fetchone()
        logger.debug("data_airstone = %s", data_airstone)
        airstone_on_off = data_airstone[1]
        logger.debug("Setting airstone_on_off = %s", airstone_on_off)

    except Exception as e:
        logger.exception(e)
        # Close sql connection
        con.close()

    airstone_setting = airstone_on_off
    logger.info("airstone_setting in AirstoneSetting class = %s",
                airstone_setting)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = "App"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.showFullScreen()

        pb_thermometer = QtWidgets.QToolButton(self)
        pb_thermometer.setIcon(QtGui.QIcon("icons/IconThermometer.png"))
        pb_thermometer.setIconSize(icon_size)
        pb_thermometer.clicked.connect(self.button_temperature_window)

        pb_light = QtWidgets.QToolButton(self)
        pb_light.setIcon(QtGui.QIcon("icons/IconLight.png"))
        pb_light.setIconSize(icon_size)
        pb_light.clicked.connect(self.button_light_window)

        pb_water = QtWidgets.QToolButton(self)
        pb_water.setIcon(QtGui.QIcon("icons/IconWater.png"))
        pb_water.setIconSize(icon_size)
        pb_water.clicked.connect(self.button_water_window)

        pb_clock = QtWidgets.QToolButton(self)
        pb_clock.setIcon(QtGui.QIcon("icons/IconClock.png"))
        pb_clock.setIconSize(icon_size)
        pb_clock.clicked.connect(self.button_clock_window)

        pb_settings = QtWidgets.QToolButton(self)
        pb_settings.setIcon(QtGui.QIcon("icons/IconSettings.png"))
        pb_settings.setIconSize(icon_size)
        pb_settings.clicked.connect(self.button_settings_window)

        pb_shutdown = QtWidgets.QToolButton(self)
        pb_shutdown.setIcon(QtGui.QIcon("icons/IconShutdown.png"))
        pb_shutdown.setIconSize(icon_size)
        pb_shutdown.clicked.connect(self.shutdown)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(pb_thermometer, QtCore.Qt.AlignRight)
        v_box.addWidget(pb_light, QtCore.Qt.AlignRight)
        v_box.addWidget(pb_water, QtCore.Qt.AlignRight)
        v_box.addWidget(pb_clock, QtCore.Qt.AlignRight)
        v_box.addWidget(pb_settings, QtCore.Qt.AlignRight)
        v_box.addStretch(1)
        v_box.addWidget(pb_shutdown, QtCore.Qt.AlignRight)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch(1)
        h_box.addLayout(v_box)

        self.setLayout(h_box)

        self.show()

        logger.info("End %s", self)

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

        pb_home = QtWidgets.QToolButton(self)
        pb_home.setIcon(QtGui.QIcon("icons/IconHome.png"))
        pb_home.setIconSize(icon_size)
        pb_home.clicked.connect(self.go_main_window)

        pb_delete_all = QtWidgets.QToolButton(self)
        pb_delete_all.setIcon(QtGui.QIcon("icons/IconRecycle.png"))
        pb_delete_all.setIconSize(icon_size)
        pb_delete_all.clicked.connect(self.delete_all_data)

        pb_delete_bad = QtWidgets.QToolButton(self)
        pb_delete_bad.setIcon(QtGui.QIcon("icons/IconRecycle.png"))
        pb_delete_bad.setIconSize(icon_size)
        pb_delete_bad.clicked.connect(self.delete_bad_data)

        lbl_delete_all = QtWidgets.QLabel("All", self)
        lbl_delete_bad = QtWidgets.QLabel("Bad", self)

        plot_widget = PlotWindow()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(pb_delete_all)
        h_box.addWidget(lbl_delete_all)
        h_box.addWidget(pb_delete_bad)
        h_box.addWidget(lbl_delete_bad)
        h_box.addStretch()
        h_box.addWidget(pb_home)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(plot_widget)
        v_box.addLayout(h_box)

        self.setLayout(v_box)

        logger.info("End %s", self)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()

    def delete_all_data(self):
        pb_reply = QtWidgets.QMessageBox.question(self, 'Warning!',
                                                  "Delete all data?",
                                                  QtWidgets.QMessageBox.Yes |
                                                  QtWidgets.QMessageBox.No,
                                                  QtWidgets.QMessageBox.No)
        if pb_reply == QtWidgets.QMessageBox.Yes:
            # Initialise sqlite
            con = sqlite3.connect(data_db)
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

    def delete_bad_data(self):
        pb_reply = QtWidgets.QMessageBox.question(self, 'Warning!',
                                                  "Delete bad readings?",
                                                  QtWidgets.QMessageBox.Yes |
                                                  QtWidgets.QMessageBox.No,
                                                  QtWidgets.QMessageBox.No)
        if pb_reply == QtWidgets.QMessageBox.Yes:
            # Initialise sqlite
            con = sqlite3.connect(data_db)
            cur = con.cursor()

            # Create table
            cur.execute('''CREATE TABLE IF NOT EXISTS temperature
                        (timestamp real, temperature1 real, temperature2 real, 
                        temperature3 real, temperature4 real, temperature5 real)''')

            # Delete all data
            cur.execute('''DELETE FROM temperature WHERE temperature1 = 0 OR 
                        temperature2 = 0 OR temperature3 = 0 OR
                        temperature4 = 0 OR temperature5 = 0''')

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
        con = sqlite3.connect(data_db)
        cur = con.cursor()

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

        logger.info("End %s", self)


class LightWindow(QtWidgets.QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Light Window')
        self.showFullScreen()

        self.tb_light = QtWidgets.QPushButton("Lamp", self)
        self.tb_light.setCheckable(True)
        self.tb_light.toggle()
        self.tb_light.clicked.connect(self.btn_action)
        self.tb_light.setFixedSize(100, 50)

        pb_home = QtWidgets.QToolButton(self)
        pb_home.setIcon(QtGui.QIcon("icons/IconHome.png"))
        pb_home.setIconSize(icon_size)
        pb_home.clicked.connect(self.go_main_window)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.tb_light)
        h_box.addStretch(0)
        h_box.addWidget(pb_home)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch(0)
        v_box.addLayout(h_box)

        self.setLayout(v_box)

        logger.info("End %s", self)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()

    def btn_action(self):
        if self.tb_light.isChecked():
            LightOutput.light_output = 1
            logger.debug("LightOutput.light_output = %s",
                         LightOutput.light_output)
            logger.info("BUTTON LIGHTWINDOW ON")
        else:
            LightOutput.light_output = 0
            logger.debug("LightOutput.light_output = %s",
                         LightOutput.light_output)
            logger.info("BUTTON LIGHTWINDOW OFF")


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

        pb_home = QtWidgets.QToolButton(self)
        pb_home.setIcon(QtGui.QIcon("icons/IconHome.png"))
        pb_home.setIconSize(icon_size)
        pb_home.clicked.connect(self.go_main_window)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.tb_pomp)
        h_box.addWidget(self.tb_airstone)
        h_box.addStretch(0)
        h_box.addWidget(pb_home)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch(0)
        v_box.addLayout(h_box)

        self.setLayout(v_box)

        logger.info("End %s", self)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()

    # TODO make btn_action compatible with multiple buttons
    def btn_action_pump(self):
        if self.tb_pomp.isChecked():
            PumpOutput.pump_output = 1
            logger.debug("PumpOutput.pump_output = %s",
                         PumpOutput.pump_output)
            logger.info("BUTTON PUMP WATERWINDOW ON")
        else:
            PumpOutput.pump_output = 0
            logger.debug("PumpOutput.pump_output = %s",
                         PumpOutput.pump_output)
            logger.info("BUTTON PUMP WATERWINDOW OFF")

    def btn_action_airstone(self):
        if self.tb_airstone.isChecked():
            AirstoneOutput.airstone_output = 1
            logger.debug("AirstoneOutput.airstone_output = %s",
                         AirstoneOutput.airstone_output)
            logger.info("BUTTON AIRSTONE WATERWINDOW ON")
        else:
            AirstoneOutput.airstone_output = 0
            logger.debug("AirstoneOutput.airstone_output = %s",
                         AirstoneOutput.airstone_output)
            logger.info("BUTTON AIRSTONE WATERWINDOW OFF")


class ClockWindow(QtWidgets.QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Clock Window')
        self.showFullScreen()

        # Create comboBox values
        hour_list = ["00", "01", "02", "03", "04", "05", "06", "07", "08",
                     "09", "10", "11", "12", "13", "14", "15", "16", "17",
                     "18", "19", "20", "21", "22", "23"]
        min_list = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
                    "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
                    "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
                    "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
                    "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
                    "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"]
        min_list_no_zero = ["01", "02", "03", "04", "05", "06", "07", "08",
                            "09", "10", "11", "12", "13", "14", "15", "16",
                            "17", "18", "19", "20", "21", "22", "23", "24",
                            "25", "26", "27", "28", "29", "30", "31", "32",
                            "33", "34", "35", "36", "37", "38", "39", "40",
                            "41", "42", "43", "44", "45", "46", "47", "48",
                            "49", "50", "51", "52", "53", "54", "55", "56",
                            "57", "58", "59"]

        pb_home = QtWidgets.QToolButton(self)
        pb_home.setIcon(QtGui.QIcon("icons/IconHome.png"))
        pb_home.setIconSize(icon_size)
        pb_home.clicked.connect(self.go_main_window)

        # Light labels
        lbl_light = QtWidgets.QLabel("Timer Licht", self)
        lbl_start_light = QtWidgets.QLabel("Start om", self)
        lbl_stop_light = QtWidgets.QLabel("Stopt om", self)
        lbl_hour_light = QtWidgets.QLabel("uur", self)
        lbl_min_light = QtWidgets.QLabel("minuten", self)
        lbl_light_on_setting = QtWidgets.QLabel(self)

        # Light combobox
        cbx_h_light_on = QtWidgets.QComboBox(self)
        cbx_h_light_on.addItems(hour_list)
        cbx_m_light_on = QtWidgets.QComboBox(self)
        cbx_m_light_on.addItems(min_list)
        cbx_h_light_off = QtWidgets.QComboBox(self)
        cbx_h_light_off.addItems(hour_list)
        cbx_m_light_off = QtWidgets.QComboBox(self)
        cbx_m_light_off.addItems(min_list)

        # Light pushbutton
        pb_set_light_on = QtWidgets.QPushButton("Set", self)
        pb_set_light_on.clicked.connect(
            lambda: self.update_settings("light_on",
                                         cbx_h_light_on.currentText(),
                                         cbx_m_light_on.currentText()))
        pb_set_light_on.clicked.connect(lambda: self.update_text())

        pb_set_light_off = QtWidgets.QPushButton("Set", self)
        pb_set_light_off.clicked.connect(
            lambda: self.update_settings("light_off",
                                         cbx_h_light_off.currentText(),
                                         cbx_m_light_off.currentText()))
        pb_set_light_off.clicked.connect(lambda: self.update_text())

        # Pump labels
        lbl_pump = QtWidgets.QLabel("Timer Pomp", self)
        lbl_times = QtWidgets.QLabel("maal", self)
        lbl_during = QtWidgets.QLabel("minuten", self)

        # Pump combobox
        cbx_times = QtWidgets.QComboBox(self)
        cbx_times.addItems(min_list_no_zero)
        cbx_during = QtWidgets.QComboBox(self)
        cbx_during.addItems(min_list_no_zero)
        cbx_every_u = QtWidgets.QComboBox(self)
        cbx_every_u.addItems(min_list)
        cbx_every_m = QtWidgets.QComboBox(self)
        cbx_every_m.addItems(min_list)

        # Pump pushbutton
        pb_pump_times_during = QtWidgets.QPushButton("Set", self)
        pb_pump_times_during.clicked.connect(
            lambda: self.update_settings("pump_during",
                                         cbx_times.currentText(),
                                         cbx_during.currentText()))
        pb_pump_times_during.clicked.connect(lambda: self.update_text())

        # Airstone labels
        lbl_air = QtWidgets.QLabel("Timer Airstone", self)
        lbl_air_start = QtWidgets.QLabel("Start", self)
        lbl_air_min_voor = QtWidgets.QLabel("minuten voor de pomp", self)

        # Airstone combobox
        cbx_air_on_min = QtWidgets.QComboBox(self)
        cbx_air_on_min.addItems(min_list_no_zero)

        # Airstone pushbutton
        pb_set_air_on = QtWidgets.QPushButton("Set", self)
        pb_set_air_on.clicked.connect(
            lambda: self.update_settings("air_on",
                                         cbx_air_on_min.currentText(),
                                         cbx_air_on_min.currentText()))
        pb_set_air_on.clicked.connect(lambda: self.update_text())

        # Labels TimerSettings
        self.lbl_line_1_1 = QtWidgets.QLabel("Het is", self)
        self.lbl_line_1_2 = QtWidgets.QLabel("xx", self)
        self.lbl_line_1_3 = QtWidgets.QLabel("uur en", self)
        self.lbl_line_1_4 = QtWidgets.QLabel("xx", self)
        self.lbl_line_1_5 = QtWidgets.QLabel("minuten", self)
        self.lbl_line_1_6 = QtWidgets.QLabel(" ", self)
        self.lbl_line_2_1 = QtWidgets.QLabel("Lamp gaat aan om", self)
        self.lbl_line_2_2 = QtWidgets.QLabel("xx", self)
        self.lbl_line_2_3 = QtWidgets.QLabel("uur en gaat uit om", self)
        self.lbl_line_2_4 = QtWidgets.QLabel("xx", self)
        self.lbl_line_2_5 = QtWidgets.QLabel("uur", self)
        self.lbl_line_2_6 = QtWidgets.QLabel(" ", self)
        self.lbl_line_3_1 = QtWidgets.QLabel("Lamp is aan gedurende", self)
        self.lbl_line_3_2 = QtWidgets.QLabel("xx", self)
        self.lbl_line_3_3 = QtWidgets.QLabel(" ", self)
        self.lbl_line_3_4 = QtWidgets.QLabel(" ", self)
        self.lbl_line_3_5 = QtWidgets.QLabel(" ", self)
        self.lbl_line_3_6 = QtWidgets.QLabel(" ", self)
        self.lbl_line_4_1 = QtWidgets.QLabel("Pomp werkt gedurende", self)
        self.lbl_line_4_2 = QtWidgets.QLabel("xx", self)
        self.lbl_line_4_3 = QtWidgets.QLabel("minuten en gaat", self)
        self.lbl_line_4_4 = QtWidgets.QLabel("xx", self)
        self.lbl_line_4_5 = QtWidgets.QLabel("keer aan om de ", self)
        self.lbl_line_4_6 = QtWidgets.QLabel("xx", self)
        self.lbl_line_5_1 = QtWidgets.QLabel("Airstone gaat", self)
        self.lbl_line_5_2 = QtWidgets.QLabel("xx", self)
        self.lbl_line_5_3 = QtWidgets.QLabel("minuten voor de pomp aan", self)
        self.lbl_line_5_4 = QtWidgets.QLabel(" ", self)
        self.lbl_line_5_5 = QtWidgets.QLabel(" ", self)
        self.lbl_line_5_6 = QtWidgets.QLabel(" ", self)

        pb_update = QtWidgets.QToolButton(self)
        pb_update.setIcon(QtGui.QIcon("icons/IconUpdate.png"))
        pb_update.setIconSize(icon_size)
        pb_update.clicked.connect(lambda: self.update_text())

        # TimerWindow layout
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(lbl_light, 0, 0)
        grid.addWidget(lbl_start_light, 1, 0)
        grid.addWidget(cbx_h_light_on, 1, 1)
        grid.addWidget(lbl_hour_light, 1, 2)
        grid.addWidget(cbx_m_light_on, 1, 3)
        grid.addWidget(lbl_min_light, 1, 4)
        grid.addWidget(pb_set_light_on, 1, 5)
        grid.addWidget(lbl_light_on_setting, 1, 6)
        grid.addWidget(lbl_stop_light, 2, 0)
        grid.addWidget(cbx_h_light_off, 2, 1)
        grid.addWidget(lbl_hour_light, 2, 2)
        grid.addWidget(cbx_m_light_off, 2, 3)
        grid.addWidget(lbl_min_light, 2, 4)
        grid.addWidget(pb_set_light_off, 2, 5)

        grid.addWidget(lbl_pump, 4, 0)
        grid.addWidget(cbx_times, 5, 1)
        grid.addWidget(lbl_times, 5, 2)
        grid.addWidget(cbx_during, 5, 3)
        grid.addWidget(lbl_during, 5, 4)
        grid.addWidget(pb_pump_times_during, 5, 5)
        grid.addWidget(lbl_air, 8, 0)
        grid.addWidget(lbl_air_start, 9, 0)
        grid.addWidget(cbx_air_on_min, 9, 1)
        grid.addWidget(lbl_air_min_voor, 9, 2)
        grid.addWidget(pb_set_air_on, 9, 5)

        grid.addWidget(self.lbl_line_1_1, 10, 0)
        grid.addWidget(self.lbl_line_1_2, 10, 1)
        grid.addWidget(self.lbl_line_1_3, 10, 2)
        grid.addWidget(self.lbl_line_1_4, 10, 3)
        grid.addWidget(self.lbl_line_1_5, 10, 4)
        grid.addWidget(self.lbl_line_1_6, 10, 5)

        grid.addWidget(self.lbl_line_2_1, 11, 0)
        grid.addWidget(self.lbl_line_2_2, 11, 1)
        grid.addWidget(self.lbl_line_2_3, 11, 2)
        grid.addWidget(self.lbl_line_2_4, 11, 3)
        grid.addWidget(self.lbl_line_2_5, 11, 4)
        grid.addWidget(self.lbl_line_2_6, 11, 5)

        grid.addWidget(self.lbl_line_3_1, 12, 0)
        grid.addWidget(self.lbl_line_3_2, 12, 1)
        grid.addWidget(self.lbl_line_3_3, 12, 2)
        grid.addWidget(self.lbl_line_3_4, 12, 3)
        grid.addWidget(self.lbl_line_3_5, 12, 4)
        grid.addWidget(self.lbl_line_3_6, 12, 5)

        grid.addWidget(self.lbl_line_4_1, 13, 0)
        grid.addWidget(self.lbl_line_4_2, 13, 1)
        grid.addWidget(self.lbl_line_4_3, 13, 2)
        grid.addWidget(self.lbl_line_4_4, 13, 3)
        grid.addWidget(self.lbl_line_4_5, 13, 4)
        grid.addWidget(self.lbl_line_4_6, 13, 5)

        grid.addWidget(self.lbl_line_5_1, 14, 0)
        grid.addWidget(self.lbl_line_5_2, 14, 1)
        grid.addWidget(self.lbl_line_5_3, 14, 2)
        grid.addWidget(self.lbl_line_5_4, 14, 3)
        grid.addWidget(self.lbl_line_5_5, 14, 4)
        grid.addWidget(self.lbl_line_5_6, 14, 5)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(pb_update)
        h_box.addStretch(0)
        h_box.addWidget(pb_home)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(grid)
        v_box.addStretch(0)
        v_box.addLayout(h_box)

        self.setLayout(v_box)

        logger.info("End %s", self)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()

    def update_settings(self, setting, data_1, data_2):
        # Initialise sqlite
        con = sqlite3.connect(data_db)
        cur = con.cursor()

        # Fill data
        data = (data_1, data_2, setting)

        # Update data
        cur.execute('''UPDATE timers SET data_1 = ?, data_2 = ? 
                    WHERE setting = ?''', data)

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()

    def update_text(self):
        # Initialise sqlite
        con = sqlite3.connect(data_db)
        cur = con.cursor()

        # Select start time from table
        # Initialise timer
        timer_on = ("light_on",)
        # Select data
        cur.execute("SELECT * FROM timers WHERE setting = ?", timer_on)
        data_timer_on = cur.fetchone()
        start_hour = data_timer_on[1]
        start_min = data_timer_on[2]
        start_light = datetime.time(start_hour, start_min)

        # Select stop time from table
        # Initialise timer
        timer_off = ("light_off",)
        # Select data
        cur.execute("SELECT * FROM timers WHERE setting = ?", timer_off)
        data_timer_off = cur.fetchone()
        stop_hour = data_timer_off[1]
        stop_min = data_timer_off[2]
        stop_light = datetime.time(stop_hour, stop_min)

        # Select pump settings from table
        # Initialise timer
        pump_setting = ("pump_during",)
        # Select data
        cur.execute("SELECT * FROM timers WHERE setting = ?", pump_setting)
        data_pump_setting = cur.fetchone()
        pump_repeat = data_pump_setting[1]
        pump_during = data_pump_setting[2]
        pump_time = datetime.time(00, pump_during)

        # Select airstone settings from table
        # Initialise timer
        air_setting = ("air_on",)
        # Select data
        cur.execute("SELECT * FROM timers WHERE setting = ?", air_setting)
        data_air_setting = cur.fetchone()
        air_on = data_pump_setting[1]
        time_air_on = datetime.time(00, air_on)

        # Initialise current time
        now = datetime.datetime.now().time()

        date = datetime.date(1, 1, 1)
        datetime_start = datetime.datetime.combine(date, start_light)
        datetime_stop = datetime.datetime.combine(date, stop_light)

        time_light_on = datetime_stop - datetime_start

        time_btwn_pumping = time_light_on // pump_repeat

        logger.debug("Het is %s uur en %s minuten", now.hour, now.minute)
        logger.debug("Lamp gaat aan om %s", start_light)
        logger.debug("Lamp gaat uit om %s", stop_light)
        logger.debug("Licht is aan gedurende %s", time_light_on)
        logger.debug("Pomp werkt gedurende %s en gaat %s keer aan om de %s",
                     pump_time, pump_repeat, time_btwn_pumping)
        logger.debug("Airstone gaat %s voor de pomp aan", time_air_on)

        # Update texts
        self.lbl_line_1_2.setText(str(now.hour))
        self.lbl_line_1_2.adjustSize()
        self.lbl_line_1_4.setText(str(now.minute))
        self.lbl_line_1_4.adjustSize()
        self.lbl_line_2_2.setText(str(start_light))
        self.lbl_line_2_2.adjustSize()
        self.lbl_line_2_4.setText(str(stop_light))
        self.lbl_line_2_4.adjustSize()
        self.lbl_line_3_2.setText(str(time_light_on))
        self.lbl_line_3_2.adjustSize()
        self.lbl_line_4_2.setText(str(pump_time))
        self.lbl_line_4_2.adjustSize()
        self.lbl_line_4_4.setText(str(pump_repeat))
        self.lbl_line_4_4.adjustSize()
        self.lbl_line_4_6.setText(str(time_btwn_pumping))
        self.lbl_line_4_6.adjustSize()
        self.lbl_line_5_2.setText(str(time_air_on))
        self.lbl_line_5_2.adjustSize()


class SettingsWindow(QtWidgets.QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings Window')
        self.showFullScreen()

        pb_home = QtWidgets.QToolButton(self)
        pb_home.setIcon(QtGui.QIcon("icons/IconHome.png"))
        pb_home.setIconSize(icon_size)
        pb_home.clicked.connect(self.go_main_window)

        # Light labels
        self.lbl_light = QtWidgets.QLabel("Licht is")
        self.lbl_light_on_off = QtWidgets.QLabel()
        if LightSetting.light_setting == 1:
            self.lbl_light_on_off.setText("ingeschakeld")
        else:
            self.lbl_light_on_off.setText("uitgeschakeld")
        # Light buttons
        pb_set_light = QtWidgets.QPushButton("AAN / UIT", self)
        pb_set_light.setCheckable(True)
        pb_set_light.toggle()
        pb_set_light.setFixedSize(100, 50)
        pb_set_light.clicked.connect(self.light_on_off)

        # Water labels
        self.lbl_water = QtWidgets.QLabel("Pomp is")
        self.lbl_water_on_off = QtWidgets.QLabel()
        if PumpSetting.pump_setting == 1:
            self.lbl_water_on_off.setText("ingeschakeld")
        else:
            self.lbl_water_on_off.setText("uitgeschakeld")
        # Water buttons
        pb_set_water = QtWidgets.QPushButton("AAN / UIT", self)
        pb_set_water.setCheckable(True)
        pb_set_water.toggle()
        pb_set_water.setFixedSize(100, 50)
        pb_set_water.clicked.connect(self.water_on_off)

        # Airstone labels
        self.lbl_airstone = QtWidgets.QLabel("Airstone is")
        self.lbl_airstone_on_off = QtWidgets.QLabel()
        if AirstoneSetting.airstone_setting == 1:
            self.lbl_airstone_on_off.setText("ingeschakeld")
        else:
            self.lbl_airstone_on_off.setText("uitgeschakeld")
        # Airstone buttons
        pb_set_airstone = QtWidgets.QPushButton("AAN / UIT", self)
        pb_set_airstone.setCheckable(True)
        pb_set_airstone.toggle()
        pb_set_airstone.setFixedSize(100, 50)
        pb_set_airstone.clicked.connect(self.airstone_on_off)

        # SettingsWindow layout
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.lbl_light, 0, 0)
        grid.addWidget(self.lbl_light_on_off, 0, 1)
        grid.addWidget(pb_set_light, 0, 2)
        grid.addWidget(self.lbl_water, 1, 0)
        grid.addWidget(self.lbl_water_on_off, 1, 1)
        grid.addWidget(pb_set_water, 1, 2)
        grid.addWidget(self.lbl_airstone, 2, 0)
        grid.addWidget(self.lbl_airstone_on_off, 2, 1)
        grid.addWidget(pb_set_airstone, 2, 2)

        h_box_1 = QtWidgets.QHBoxLayout()
        h_box_1.addStretch(0)
        h_box_1.addWidget(pb_home)

        h_box_2 = QtWidgets.QHBoxLayout()
        h_box_2.addLayout(grid)
        h_box_2.addStretch(0)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box_2)
        v_box.addStretch(0)
        v_box.addLayout(h_box_1)

        self.setLayout(v_box)

        logger.info("End %s", self)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()

    def light_on_off(self):
        if LightSetting.light_setting == 1:
            LightSetting.light_setting = 0
            self.lbl_light_on_off.setText("uitgeschakeld")
            self.lbl_light_on_off.adjustSize()

            # Initialise sqlite
            con = sqlite3.connect(data_db)
            cur = con.cursor()

            # Fill data
            setting = "light"
            data = (LightSetting.light_setting, setting)
            logger.debug("light_on_off.data = %s", data)

            # Create table
            cur.execute('''CREATE TABLE IF NOT EXISTS settings
                        (setting TEXT, data_1 INTEGER)''')

            # Update data
            cur.execute('''UPDATE settings SET data_1 = ? WHERE setting = ?''',
                        data)

            # Save (commit) the changes
            con.commit()

            # Close connection
            con.close()

        else:
            LightSetting.light_setting = 1
            self.lbl_light_on_off.setText("ingeschakeld")
            self.lbl_light_on_off.adjustSize()

            # Initialise sqlite
            con = sqlite3.connect(data_db)
            cur = con.cursor()

            # Fill data
            setting = "light"
            data = (LightSetting.light_setting, setting)
            logger.debug("light_on_off.data = %s", data)

            # Create table
            cur.execute('''CREATE TABLE IF NOT EXISTS settings
                        (setting TEXT, data_1 INTEGER)''')

            # Update data
            cur.execute('''UPDATE settings SET data_1 = ? WHERE setting = ?''',
                        data)

            # Save (commit) the changes
            con.commit()

            # Close connection
            con.close()

    def water_on_off(self):
        if PumpSetting.pump_setting == 1:
            PumpSetting.pump_setting = 0
            self.lbl_water_on_off.setText("uitgeschakeld")
            self.lbl_water_on_off.adjustSize()

            # Initialise sqlite
            con = sqlite3.connect(data_db)
            cur = con.cursor()

            # Fill data
            setting = "pump"
            data = (PumpSetting.pump_setting, setting)
            logger.debug("water_on_off.data = %s", data)

            # Create table
            cur.execute('''CREATE TABLE IF NOT EXISTS settings
                        (setting TEXT, data_1 INTEGER)''')

            # Update data
            cur.execute('''UPDATE settings SET data_1 = ? WHERE setting = ?''',
                        data)

            # Save (commit) the changes
            con.commit()

            # Close connection
            con.close()

        else:
            PumpSetting.pump_setting = 1
            self.lbl_water_on_off.setText("ingeschakeld")
            self.lbl_water_on_off.adjustSize()

            # Initialise sqlite
            con = sqlite3.connect(data_db)
            cur = con.cursor()

            # Fill data
            setting = "pump"
            data = (PumpSetting.pump_setting, setting)
            logger.debug("water_on_off.data = %s", data)

            # Create table
            cur.execute('''CREATE TABLE IF NOT EXISTS settings
                        (setting TEXT, data_1 INTEGER)''')

            # Update data
            cur.execute('''UPDATE settings SET data_1 = ? WHERE setting = ?''',
                        data)

            # Save (commit) the changes
            con.commit()

            # Close connection
            con.close()

    def airstone_on_off(self):
        if AirstoneSetting.airstone_setting == 1:
            AirstoneSetting.airstone_setting = 0
            self.lbl_airstone_on_off.setText("uitgeschakeld")
            self.lbl_airstone_on_off.adjustSize()

            # Initialise sqlite
            con = sqlite3.connect(data_db)
            cur = con.cursor()

            # Fill data
            setting = "airstone"
            data = (AirstoneSetting.airstone_setting, setting)
            logger.debug("airstone_on_off.data = %s", data)

            # Create table
            cur.execute('''CREATE TABLE IF NOT EXISTS settings
                        (setting TEXT, data_1 INTEGER)''')

            # Update data
            cur.execute('''UPDATE settings SET data_1 = ? WHERE setting = ?''',
                        data)

            # Save (commit) the changes
            con.commit()

            # Close connection
            con.close()

        else:
            AirstoneSetting.airstone_setting = 1
            self.lbl_airstone_on_off.setText("ingeschakeld")
            self.lbl_airstone_on_off.adjustSize()

            # Initialise sqlite
            con = sqlite3.connect(data_db)
            cur = con.cursor()

            # Fill data
            setting = "airstone"
            data = (AirstoneSetting.airstone_setting, setting)
            logger.debug("airstone_on_off.data = %s", data)

            # Create table
            cur.execute('''CREATE TABLE IF NOT EXISTS settings
                        (setting TEXT, data_1 INTEGER)''')

            # Update data
            cur.execute('''UPDATE settings SET data_1 = ? WHERE setting = ?''',
                        data)

            # Save (commit) the changes
            con.commit()

            # Close connection
            con.close()


class ShutdownWindow(QtWidgets.QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Shutdown Window')
        self.minimumSizeHint()
        self.showFullScreen()

        pb_exit = QtWidgets.QPushButton("Exit", self)
        pb_exit.minimumSizeHint()
        pb_exit.setAutoDefault(False)
        pb_exit.clicked.connect(self.exit)
        pb_reboot = QtWidgets.QPushButton("Reboot", self)
        pb_reboot.minimumSizeHint()
        pb_reboot.setAutoDefault(False)
        pb_reboot.clicked.connect(self.reboot)
        pb_shutdown = QtWidgets.QPushButton("Shutdown", self)
        pb_shutdown.minimumSizeHint()
        pb_shutdown.setAutoDefault(False)
        pb_shutdown.clicked.connect(self.shutdown)
        pb_cancel = QtWidgets.QPushButton("Cancel", self)
        pb_cancel.minimumSizeHint()
        pb_cancel.clicked.connect(self.go_main_window)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch(1)
        h_box.addWidget(pb_exit)
        h_box.addWidget(pb_reboot)
        h_box.addWidget(pb_shutdown)
        h_box.addWidget(pb_cancel)
        h_box.addStretch(1)

        self.setLayout(h_box)

        logger.info("End %s", self)

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
    # Graphical User Interface
    app = QtWidgets.QApplication(sys.argv)
    ex = Window()

    # LightTimer class
    lt = LightTimer()
    lt.run()
    # LightTimer class
    pt = PumpTimer()
    pt.run()
    # AirstoneTimer class
    at = AirstoneTimer()
    at.run()

    # ProcessTimers class
    prt = ProcessTimers()
    prt.run()

    # LightOutput class
    lo = LightOutput()
    lo.run()
    # PumpOutput class
    po = PumpOutput()
    po.run()
    # AirstoneOutput class
    ao = AirstoneOutput()
    ao.run()

    # Threading
    # logger.info("Voor creëren thread process_timers")
    # thread_1 = threading.Thread(target=process_timers, daemon=True)
    # logger.info("Voor creëren thread process_timers")
    # thread_1.start()

    sys.exit(app.exec_())
