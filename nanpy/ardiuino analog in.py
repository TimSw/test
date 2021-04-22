#!/usr/bin/env python
# Read values from Analogue pin A0
# 10K ohm potentiometer on A0
from nanpy import (ArduinoApi, SerialManager)
from time import sleep

connection = SerialManager()
a = ArduinoApi(connection=connection)

pot = 14  # Pot on A0 - Anaglog input

print("Turn the pot - Analogue input - 10 bit")
for i in range(0, 40):
    val = a.analogRead(pot)  # Analog input
    print(val)
    sleep(0.3)
