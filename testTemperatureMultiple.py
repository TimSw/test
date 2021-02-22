#!/usr/bin/env python3
import sqlite3
import time
from w1thermsensor import W1ThermSensor


# Initialise sqlite
con = sqlite3.connect('data.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS temperature
            (timestamp real, temperature1 real, temperature2 real, 
            temperature3 real, temperature4 real, temperature5 real)''')

# Setup sensor address
try:
    sensor1 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "800000265db7")
except Exception as e:
    print(e)
try:
    sensor2 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "041662e87fff")
except Exception as e:
    print(e)
try:
    sensor3 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "80000026d9bf")
except Exception as e:
    print(e)
try:
    sensor4 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "04166084f8ff")
except Exception as e:
    print(e)
try:
    sensor5 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "041662af5bff")
except Exception as e:
    print(e)

# Initialise temperatures:
temp1 = 0
temp2 = 0
temp3 = 0
temp4 = 0
temp5 = 0

# Make timestamp
now = time.time()

# Read temperature
try:
    temp1 = sensor1.get_temperature()
except Exception as e:
    print(e)
try:
    temp2 = sensor2.get_temperature()
except Exception as e:
    print(e)
try:
    temp3 = sensor3.get_temperature()
except Exception as e:
    print(e)
try:
    temp4 = sensor4.get_temperature()
except Exception as e:
    print(e)
try:
    temp5 = sensor5.get_temperature()
except Exception as e:
    print(e)

# Insert a row of data
cur.execute("INSERT INTO temperature VALUES (?, ?, ?, ?, ?, ?)",
            (now, temp1, temp2, temp3, temp4, temp5))

# Save (commit) the changes
con.commit()

# Close connection
con.close()

# TODO raise SystemExit()
