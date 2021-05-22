#!/usr/bin/env python3
import nanpy
import time

# Initialise arduino connection
connection = nanpy.SerialManager(device="/dev/ttyUSB0")
arduino = nanpy.ArduinoApi(connection=connection)

# Define pin
A0 = 14     # D14 - A0 - PC0 - ADC[0]

moisture = 0.00000

# Read moisture level
time.sleep(3)
moisture = arduino.analogRead(A0)  # Analog input

print(moisture)
