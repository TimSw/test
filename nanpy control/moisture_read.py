#!/usr/bin/env python3
import logging
import logging.handlers
import logging.config
import sqlite3
import nanpy
import time

# Logging
# Open logging configuration
#logging.config.fileConfig("logging.conf")
# create logger
#logger = logging.getLogger("root")

# Define data.db directory
data_db = "/home/pi/growPiProject/data.db"

# Initialise sqlite
con = sqlite3.connect(data_db)
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS moisture
            (timestamp REAL, moisture REAL)''')

# Initialise arduino connection
connection = nanpy.SerialManager(device="/dev/ttyUSB0")
arduino = nanpy.ArduinoApi(connection=connection)

# Define pin
A0 = 14     # D14 - A0 - PC0 - ADC[0]

# Read moisture level
time.sleep(2)
moisture = arduino.analogRead(A0)  # Analog input
#logger.debug("Moisture level = %s", moisture)

# Make timestamp
now = time.time()

# Insert a row of data
cur.execute("INSERT INTO moisture VALUES (?, ?)",
            (now, moisture))

# Save (commit) the changes
con.commit()

# Close connection
con.close()

# TODO raise SystemExit()
