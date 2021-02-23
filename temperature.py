#!/usr/bin/env python3
import sqlite3
import time
from w1thermsensor import W1ThermSensor


# Initialise sqlite
con = sqlite3.connect('data.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS temperature
            (timestamp real, temperature real)''')

# Setup sensor adress
sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "80000026d9bf")

# Make timestamp
now = time.time()

# Read temperature
temp = sensor.get_temperature()

# Insert a row of data
cur.execute("INSERT INTO temperature VALUES (?, ?)", (now, temp))

# Save (commit) the changes
con.commit()

# Close connection
con.close()

#raise SystemExit()
