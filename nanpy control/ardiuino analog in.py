#!/usr/bin/env python
# Read values from Analogue pin A0
# 10K ohm potentiometer on A0
import time
import nanpy
# from nanpy import (ArduinoApi, SerialManager)
# from time import sleep

connection = nanpy.SerialManager()
a = nanpy.ArduinoApi(connection=connection)

A1 = 14  # Pot on A0 - Anaglog input

print("Turn the pot - Analogue input - 10 bit")
for i in range(0, 40):
    val = a.analogRead(A1)  # Analog input
    print(val)
    time.sleep(0.3)
