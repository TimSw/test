#!/usr/bin/env python
# Read values from Analogue pin A0
# 10K ohm potentiometer on A0
import time
import nanpy
# from nanpy import (ArduinoApi, SerialManager)
# from time import sleep

connection = nanpy.SerialManager(device="/dev/ttyUSB0")
a = nanpy.ArduinoApi(connection=connection)

A0 = 14     # D14 - A0 - PC0 - ADC[0]

print("Turn the pot - Analogue input - 10 bit")
for i in range(0, 40):
    val = a.analogRead(A0)  # Analog input
    print(val)
    time.sleep(0.3)
