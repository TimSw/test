#!/usr/bin/python3
import datetime

pump_repeat = int(input("Please enter a number of times the pump should "
                        "repeat: "))
pump_during = 10
time_pump_on = datetime.time(00, pump_during)
print("time_pump_on = ", time_pump_on)

pump_start_times = []

repeats = 1

try:
    while repeats < pump_repeat:
        pump_during = pump_during * repeats
        pump_start_times.append(pump_during)
        repeats = repeats + 1
        print("repeats= ", repeats)
        print("pump_during = ", pump_during)
except Exception as e:
    print(e)

print("pump_start_times = ", pump_start_times)


