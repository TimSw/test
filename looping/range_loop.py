#!/usr/bin/python3
import datetime

start_hour = 8
start_min = 30
stop_hour = 17
stop_min = 15

start_light = datetime.time(start_hour, start_min)
stop_light = datetime.time(stop_hour, stop_min)
print("start_light = ", start_light)
print("stop_light = ", stop_light)

date = datetime.date(1, 1, 1)
datetime_start = datetime.datetime.combine(date, start_light)
datetime_stop = datetime.datetime.combine(date, stop_light)
time_light_on = datetime_stop - datetime_start
print("time_light_on = ", time_light_on)

pump_repeat = int(input("Please enter a number of times the pump should "
                        "repeat: "))
print("pump_repeat = ", pump_repeat)

pump_during = 10
print("pump_during = ", pump_during)

time_pump_on = datetime.time(00, pump_during)
print("time_pump_on = ", time_pump_on)

pump_interval = time_light_on // pump_repeat
print("pump_interval = ", pump_interval)

start_times = []
print("start_times 1 = ", start_times)

while pump_repeat > 1:
    start_times.append(time_light_on + (pump_interval * pump_repeat))
    pump_repeat = pump_repeat - 1

print("start_times 2 = ", start_times)
start_times.reverse()
print("start_times 3 = ", start_times)

start_times.insert(0, datetime_start)
print("start_times 4 = ", start_times)

for times in start_times:
    print(times)

subtract = start_times[1] - start_times[0]
print(subtract)