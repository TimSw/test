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
cur.execute('''CREATE TABLE IF NOT EXISTS current
            (timestamp REAL, current REAL)''')

# Initialise arduino connection
connection = nanpy.SerialManager(device="/dev/ttyUSB1")
arduino = nanpy.ArduinoApi(connection=connection)

# Define pin
A0 = 14     # D14 - A0 - PC0 - ADC[0]

# Read analog input
time.sleep(2)
current = arduino.analogRead(A0)  # Analog input

# Make timestamp
now = time.time()

# Insert a row of data
cur.execute("INSERT INTO current VALUES (?, ?)",
            (now, current))

# Save (commit) the changes
con.commit()

# Close connection
con.close()

# TODO raise SystemExit()
