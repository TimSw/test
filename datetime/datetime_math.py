#!/usr/bin/python3
import datetime

start_hour = 8
start_min = 30
stop_hour = 17
stop_min = 15

date = datetime.date(1, 1, 1)

start_light = datetime.time(start_hour, start_min)
stop_light = datetime.time(stop_hour, stop_min)
print("start_light = ", start_light)
print("stop_light = ", stop_light)

datetime_start = datetime.datetime.combine(date, start_light)
datetime_stop = datetime.datetime.combine(date, stop_light)
time_light_on = datetime_stop - datetime_start
print("datetime_start = ", datetime_start)
print("datetime_stop = ", datetime_stop)
print("time_light_on = ", time_light_on)

pump_repeat = 4
print("pump_repeat = ", pump_repeat)

pump_interval = time_light_on // pump_repeat
print("pump_interval = ", pump_interval)
# datetime_pump_interval = datetime.datetime.combine(date, pump_interval)

start_times = []
print("start_times 1 = ", start_times)